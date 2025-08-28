from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import register_routers
from repository.feature_repository import FeatureRepositoryAsync
from services.feature_service import FeatureService
from repository.source_repository import SourceRepositoryAsync
from services.source_service import SourceService
from services.knowledge_base_service import KnowledgeBaseService
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

accessible_endpoints = [
    "http://127.0.0.1:5000",  # Backend
    "http://localhost:5000",  # Backend
    "http://localhost:3000",  # Frontend
]


def create_app():
    app = FastAPI(title="Hacktok API", version="0.1.0")

    cors_origins = [
        *accessible_endpoints,
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def setup_routes(app: FastAPI, feature_service: FeatureService, source_service: SourceService, knowledge_base_service: KnowledgeBaseService):
    """Register API routes with their dependencies."""
    register_routers(app, feature_service=feature_service,
                     source_service=source_service,
                     knowledge_base_service=knowledge_base_service)


def create_asgi_app():
    app = create_app()

    feature_repository = FeatureRepositoryAsync(
        db_name="hacktok",
        collection_name="features"
    )

    feature_service = FeatureService(feature_repository=feature_repository)

    source_repository = SourceRepositoryAsync(
        db_name="hacktok",
        collection_name="sources"
    )

    source_service = SourceService(source_repository=source_repository)

    knowledge_base_service = KnowledgeBaseService()

    setup_routes(app, feature_service=feature_service,
                 source_service=source_service,
                 knowledge_base_service=knowledge_base_service)

    return app


app = create_asgi_app()


def main():
    """Main application entry point"""

    print("\n" + "="*50)
    print("🚀 FastAPI Application starting up!")
    print(f"🌐 CORS: Allowing requests from {accessible_endpoints}")
    print("="*50 + "\n")

    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000,
                log_level="info", reload=True)


if __name__ == "__main__":
    main()
