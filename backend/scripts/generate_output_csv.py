import asyncio
import csv
import os
from datetime import timezone
from typing import Dict, List

from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import AsyncMongoClient


async def fetch_feature_names(db) -> Dict[str, str]:
    features = db["features"]
    cursor = features.find({}, {"_id": 1, "name": 1})
    docs = await cursor.to_list(length=None)
    return {str(doc["_id"]): doc.get("name", "") for doc in docs}


async def fetch_source_urls(db, ids: List[str]) -> Dict[str, str]:
    sources = db["sources"]
    object_ids = []
    for sid in ids:
        try:
            object_ids.append(ObjectId(sid))
        except Exception:
            # skip invalid ObjectId strings
            pass
    if not object_ids:
        return {}
    cursor = sources.find({"_id": {"$in": object_ids}}, {"_id": 1, "source_url": 1})
    docs = await cursor.to_list(length=None)
    return {str(doc["_id"]): doc.get("source_url", "") for doc in docs}


async def generate_audit_reports_csv(output_path: str = "audit_reports_export.csv"):
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI is not set in environment")

    client = AsyncMongoClient(mongo_uri)
    db = client["hacktok"]

    audit_reports_col = db["audit_reports"]

    # Fetch all audit reports
    audit_reports = (
        await audit_reports_col.find().sort("created_at", 1).to_list(length=None)
    )

    # Collect feature and source ids
    feature_id_to_name = await fetch_feature_names(db)
    all_source_ids: List[str] = []
    for report in audit_reports:
        all_source_ids.extend([str(sid) for sid in report.get("source_ids", [])])

    source_id_to_url = await fetch_source_urls(db, list(set(all_source_ids)))

    # Determine max number of sources across reports for padding
    max_sources = 0
    for report in audit_reports:
        max_sources = max(max_sources, len(report.get("source_ids", [])))

    # Prepare CSV header
    base_headers = [
        "audit_report_id",
        "feature_id",
        "feature_name",
        "needs_action",
        "original_status",
        "status_change_to",
        "reason",
        "confidence",
        "status",
        "created_at",
        "updated_at",
    ]
    source_headers: List[str] = []
    for i in range(1, max_sources + 1):
        source_headers.extend([f"source_id_{i}", f"source_url_{i}"])
    headers = base_headers + source_headers

    # Write CSV
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for report in audit_reports:
            rid = str(report.get("_id", ""))
            feature_id = str(report.get("feature_id", ""))
            feature_name = feature_id_to_name.get(feature_id, "")
            needs_action = report.get("needs_action", "")
            original_status = report.get("original_status", "")
            status_change_to = report.get("status_change_to", "")
            reason = report.get("reason", "")
            confidence = report.get("confidence", "")
            status = report.get("status", "")

            created_at = report.get("created_at")
            updated_at = report.get("updated_at")

            def fmt(dt):
                if not dt:
                    return ""
                try:
                    # Ensure timezone-aware ISO string
                    return dt.astimezone(timezone.utc).isoformat()
                except Exception:
                    return str(dt)

            row = [
                rid,
                feature_id,
                feature_name,
                needs_action,
                original_status,
                status_change_to,
                reason,
                confidence,
                status,
                fmt(created_at),
                fmt(updated_at),
            ]

            # Add source id/url pairs with padding
            source_ids = [str(sid) for sid in report.get("source_ids", [])]
            for i in range(max_sources):
                if i < len(source_ids):
                    sid = source_ids[i]
                    surl = source_id_to_url.get(sid, "")
                    row.extend([sid, surl])
                else:
                    row.extend(["", ""])  # pad

            writer.writerow(row)

    await client.close()


if __name__ == "__main__":
    asyncio.run(generate_audit_reports_csv())
