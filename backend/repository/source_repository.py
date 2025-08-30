import os
from typing import Any, AsyncGenerator, Dict, List
import dotenv
from bson.objectid import ObjectId
from pymongo import AsyncMongoClient

dotenv.load_dotenv()
mongodb_uri = os.getenv("MONGO_URI")


class SourceRepositoryAsync:
    def __init__(self, db_name: str, collection_name: str):
        self.client = AsyncMongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    async def get_sources(self) -> list[dict]:
        sources = await self.collection.find().to_list(length=None)
        for source in sources:
            if "_id" in source:
                source["id"] = str(source.pop("_id"))
        return sources

    async def get_sources_via_ids(self, source_ids: List[str]) -> list[dict]:
        sources = await self.collection.find(
            {"_id": {"$in": [ObjectId(source_id) for source_id in source_ids]}}
        ).to_list(length=None)
        for source in sources:
            if "_id" in source:
                source["id"] = str(source.pop("_id"))
        return sources

    async def add_source(self, source) -> str:
        new_source = {**source}
        if source.get("id"):
            new_source["_id"] = ObjectId(source["id"])
        new_source.pop("id", None)
        result = await self.collection.insert_one(new_source)
        return str(result.inserted_id)

    async def update_source(self, source_id: str, update_data: dict) -> bool:
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(source_id)}, {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating source: {e}")
            return False

    async def remove_source(self, source_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(source_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error removing source: {e}")
            return False

    async def get_source_count(self) -> int:
        try:
            return await self.collection.count_documents({})
        except Exception as e:
            print(f"Error getting source count: {e}")
            return 0

    async def stream_sources(self) -> AsyncGenerator[Dict[str, Any], None]:
        try:
            pipeline = [
                {
                    "$match": {
                        "operationType": {"$in": ["insert", "update", "replace"]},
                        "fullDocument": {"$exists": True},
                    }
                }
            ]

            change_stream = await self.collection.watch(
                pipeline, full_document="updateLookup"
            )

            try:
                async for change in change_stream:
                    full_document = change["fullDocument"].copy()
                    if "_id" in full_document:
                        full_document["id"] = str(full_document.pop("_id"))

                    change_data = {
                        "operation_type": change["operationType"],
                        "source_id": full_document["id"],
                        "updated_document": full_document,
                        "timestamp": change["clusterTime"],
                        "resume_token": change["_id"],
                    }

                    yield change_data

            except Exception as stream_error:
                print(f"❌ Error during source streaming: {stream_error}")
                raise
            finally:
                try:
                    await change_stream.close()
                except Exception:
                    pass

        except Exception as e:
            print(f"❌ Error setting up source change stream: {e}")
            print(f"   Error type: {type(e).__name__}")
            raise
