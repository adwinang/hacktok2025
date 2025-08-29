import os
from typing import List
import dotenv
from bson.objectid import ObjectId
from pymongo import AsyncMongoClient

dotenv.load_dotenv()
mongodb_uri = os.getenv('MONGO_URI')


class SourceContentRepositoryAsync:
    def __init__(self, db_name: str, collection_name: str):
        self.client = AsyncMongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    async def get_source_contents_async(self) -> list[dict]:
        source_contents = await self.collection.find().to_list(length=None)
        for source_content in source_contents:
            if "_id" in source_content:
                source_content["id"] = str(source_content.pop("_id"))
        return source_contents

    async def get_source_content_by_source_url_async(self, source_url: str) -> List[dict]:
        source_contents = await self.collection.find({"source_url": source_url}).to_list(length=None)
        for source_content in source_contents:
            if "_id" in source_content:
                source_content["id"] = str(source_content.pop("_id"))
        return source_contents

    async def get_source_content_by_source_urls_async(self, source_urls: List[str]) -> List[dict]:
        source_contents = await self.collection.find({"source_url": {"$in": source_urls}}).to_list(length=None)
        for source_content in source_contents:
            if "_id" in source_content:
                source_content["id"] = str(source_content.pop("_id"))
        return source_contents

    async def add_source_content_async(self, source_content) -> str:
        new_source_content = {**source_content}
        if source_content.get("id"):
            new_source_content["_id"] = ObjectId(source_content["id"])
        new_source_content.pop("id", None)
        result = await self.collection.insert_one(new_source_content)
        return str(result.inserted_id)
