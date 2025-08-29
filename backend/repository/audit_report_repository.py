import os
import dotenv
from typing import Any, AsyncGenerator, Dict
from bson.objectid import ObjectId
from pymongo import AsyncMongoClient

from model.audit_report import AuditReportStatus

dotenv.load_dotenv()
mongodb_uri = os.getenv('MONGO_URI')


class AuditReportRepositoryAsync:
    def __init__(self, db_name: str, collection_name: str):
        self.client = AsyncMongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    async def get_audit_reports_async(self) -> list[dict]:
        try:
            audit_reports = await self.collection.find().to_list(length=None)
            for audit_report in audit_reports:
                if "_id" in audit_report:
                    audit_report["id"] = str(audit_report.pop("_id"))
            return audit_reports
        except Exception as e:
            print(f"Error getting audit reports: {e}")
            return []

    async def get_audit_report_async(self, audit_report_id: str):
        audit_report = await self.collection.find_one({"_id": ObjectId(audit_report_id)})
        if audit_report:
            audit_report["id"] = str(audit_report.pop("_id"))
        return audit_report

    async def create_audit_report_async(self, audit_report):
        new_audit_report = {**audit_report}
        if audit_report.get("id"):
            new_audit_report["_id"] = ObjectId(audit_report["id"])
        new_audit_report.pop("id", None)
        result = await self.collection.insert_one(new_audit_report)
        return str(result.inserted_id)

    async def update_audit_report_async(self, audit_report_id: str, audit_report):
        try:
            result = await self.collection.update_one({"_id": ObjectId(audit_report_id)}, {"$set": audit_report})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating audit report: {e}")
            return False

    async def get_audit_report_for_feature_async(self, feature_id: str, status: AuditReportStatus = None):
        try:
            query = {"feature_id": feature_id}
            if status is not None:
                query["status"] = status.value
            result = await self.collection.find_one(query)
            if result:
                result["id"] = str(result.pop("_id"))
            return result
        except Exception as e:
            print(f"Error getting audit report for feature: {e}")
            return None

    async def stream_audit_reports(self) -> AsyncGenerator[Dict[str, Any], None]:
        try:
            # Pipeline to match insert, update, replace, and delete operations
            pipeline = [
                {
                    "$match": {
                        "operationType": {"$in": ["insert", "update", "replace", "delete"]}
                    }
                }
            ]

            # Use updateLookup to get full document for updates, inserts will have fullDocument by default
            change_stream = await self.collection.watch(pipeline, full_document="updateLookup")

            try:
                async for change in change_stream:
                    operation_type = change["operationType"]

                    # Handle different operation types
                    if operation_type == "delete":
                        # For delete operations, fullDocument is not available
                        audit_report_id = str(change["documentKey"]["_id"])
                        change_data = {
                            "operation_type": operation_type,
                            "audit_report_id": audit_report_id,
                            "updated_document": None,  # No document for delete
                            "timestamp": change["clusterTime"],
                            "resume_token": change["_id"]
                        }
                    else:
                        # For insert, update, replace operations
                        full_document = change["fullDocument"].copy()
                        if "_id" in full_document:
                            full_document["id"] = str(full_document.pop("_id"))

                        change_data = {
                            "operation_type": operation_type,
                            "audit_report_id": full_document["id"],
                            "updated_document": full_document,
                            "timestamp": change["clusterTime"],
                            "resume_token": change["_id"]
                        }

                    yield change_data

            except Exception as stream_error:
                print(f"❌ Error during audit report streaming: {stream_error}")
                raise
            finally:
                try:
                    await change_stream.close()
                except:
                    pass

        except Exception as e:
            print(f"❌ Error setting up audit report change stream: {e}")
            print(f"   Error type: {type(e).__name__}")
            raise
