import asyncio
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import AsyncMongoClient


async def reset_database():
    load_dotenv()

    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI is not set in environment")

    client = AsyncMongoClient(mongo_uri)
    db = client["hacktok"]

    # Collections
    features = db["features"]
    sources = db["sources"]
    source_contents = db["source_contents"]
    audit_reports = db["audit_reports"]

    # Use a single timestamp for consistency
    now = datetime.now(timezone.utc)

    # 1) Delete audit reports, source contents, and sources
    await audit_reports.delete_many({})
    await source_contents.delete_many({})
    await sources.delete_many({})

    # 2) Reset all features to pending with current timestamps
    await features.update_many(
        {},
        {
            "$set": {
                "status": "pending",
                "updated_at": now,
            },
            "$setOnInsert": {
                "created_at": now,
            },
        },
    )

    # Ensure created_at exists; if any documents miss it, set to now
    await features.update_many(
        {"created_at": {"$exists": False}}, {"$set": {"created_at": now}}
    )

    # Close client
    await client.close()


if __name__ == "__main__":
    asyncio.run(reset_database())
