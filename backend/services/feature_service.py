import json
from typing import AsyncGenerator
from model.feature import Feature, FeatureCreateRequest, FeatureUpdateRequest, FeatureStatus
from repository.feature_repository import FeatureRepositoryAsync
from datetime import datetime
from agents.feature_tagging_agent import FeatureTaggingAgent


class FeatureService:
    def __init__(self, feature_repository: FeatureRepositoryAsync, feature_tagging_agent: FeatureTaggingAgent):
        self.feature_repository = feature_repository
        self.feature_tagging_agent = feature_tagging_agent

    async def get_features_async(self) -> list[Feature]:
        try:
            features_data = await self.feature_repository.get_features_async()
            features = []
            for feature_data in features_data:
                feature = Feature(**feature_data)
                features.append(feature)
            return features
        except Exception as e:
            raise e

    async def get_feature_async(self, feature_id: str) -> Feature:
        try:
            feature_data = await self.feature_repository.get_feature_async(feature_id)
            return Feature(**feature_data)
        except Exception as e:
            raise e

    async def create_feature_async(self, feature_request: FeatureCreateRequest) -> str:
        try:
            # Generate feature tags using the tagging agent
            feature_tags_response = await self.feature_tagging_agent.generate_feature_tags(feature_request)
            feature = Feature(
                name=feature_request.name,
                description=feature_request.description,
                tags=feature_tags_response.tags,
                status=FeatureStatus.PENDING,
                created_at=datetime.utcnow(),
                updated_at=None
            )
            feature_id = await self.feature_repository.add_feature_async(feature.model_dump())
            return feature_id
        except Exception as e:
            raise e

    async def update_feature_async(self, feature_id: str, update_request: FeatureUpdateRequest) -> bool:
        try:
            update_data = {}
            if update_request.name is not None:
                update_data["name"] = update_request.name
            if update_request.description is not None:
                update_data["description"] = update_request.description
            if update_request.status is not None:
                update_data["status"] = update_request.status.value

            if update_data:
                update_data["updated_at"] = datetime.utcnow()

            return await self.feature_repository.update_feature_async(feature_id, update_data)
        except Exception as e:
            raise e

    async def stream_features_async(self) -> AsyncGenerator[str, None]:
        try:
            initial_features = await self.get_features_async()

            features_data = []
            for feature in initial_features:
                feature_dict = feature.model_dump()

                if "created_at" in feature_dict and feature_dict["created_at"]:
                    feature_dict["created_at"] = feature_dict["created_at"].isoformat()
                if "updated_at" in feature_dict and feature_dict["updated_at"]:
                    feature_dict["updated_at"] = feature_dict["updated_at"].isoformat()

                features_data.append(feature_dict)

            initial_message = {
                "type": "initial_data",
                "data": {
                    "features": features_data
                }
            }

            yield f"data: {json.dumps(initial_message)}\n\n"
            yield f": heartbeat\n\n"

            async for change in self.feature_repository.stream_features():
                updated_doc = change["updated_document"].copy()

                if "created_at" in updated_doc and updated_doc["created_at"]:
                    updated_doc["created_at"] = updated_doc["created_at"].isoformat()
                if "updated_at" in updated_doc and updated_doc["updated_at"]:
                    updated_doc["updated_at"] = updated_doc["updated_at"].isoformat()

                change_message = {
                    "type": "feature_update",
                    "data": {
                        "operation_type": change["operation_type"],
                        "feature_id": change["feature_id"],
                        "feature_data": updated_doc,
                        "timestamp": change["timestamp"].as_datetime().isoformat()
                    }
                }

                yield f"data: {json.dumps(change_message)}\n\n"

        except Exception as e:
            error_message = {
                "type": "error",
                "data": {
                    "message": f"Streaming error: {str(e)}"
                }
            }
            yield f"data: {json.dumps(error_message)}\n\n"

    async def get_feature_count_async(self) -> int:
        try:
            return await self.feature_repository.get_feature_count()
        except Exception as e:
            raise e
