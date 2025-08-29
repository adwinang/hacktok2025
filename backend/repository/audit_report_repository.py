import os
import dotenv
from bson.objectid import ObjectId
from pymongo import AsyncMongoClient

dotenv.load_dotenv()
mongodb_uri = os.getenv('MONGO_URI')


class AuditReportRepositoryAsync:
    def __init__(self, db_name: str, collection_name: str):
        self.client = AsyncMongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

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
