from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import register_routers
from repository.feature_repository import FeatureRepositoryAsync
from services.feature_service import FeatureService
from repository.source_repository import SourceRepositoryAsync
from services.source_service import SourceService
from repository.source_content_repository import SourceContentRepositoryAsync
from services.source_content_service import SourceContentService
from services.knowledge_base_service import KnowledgeBaseService
from services.compliance_analysis_service import ComplianceAnalysisService

from repository.audit_report_repository import AuditReportRepositoryAsync
from services.audit_report_service import AuditReportService
from services.compliance_action_service import ComplianceActionService

from agents.compliance_analyzer_agent import ComplianceAnalyzerAgent

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


def setup_routes(app: FastAPI, feature_service: FeatureService, source_service: SourceService, source_content_service: SourceContentService, knowledge_base_service: KnowledgeBaseService, compliance_analysis_service: ComplianceAnalysisService, audit_report_service: AuditReportService, compliance_action_service: ComplianceActionService):
    """Register API routes with their dependencies."""
    register_routers(app, feature_service=feature_service,
                     source_service=source_service,
                     source_content_service=source_content_service,
                     knowledge_base_service=knowledge_base_service,
                     compliance_analysis_service=compliance_analysis_service,
                     audit_report_service=audit_report_service,
                     compliance_action_service=compliance_action_service)


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

    source_content_repository = SourceContentRepositoryAsync(
        db_name="hacktok",
        collection_name="source_contents"
    )

    source_content_service = SourceContentService(
        source_content_repository=source_content_repository)

    knowledge_base_service = KnowledgeBaseService(
        source_service=source_service,
        source_content_service=source_content_service
    )

    compliance_analysis_service = ComplianceAnalysisService(
        source_service=source_service,
        source_content_service=source_content_service,
        feature_service=feature_service,
        compliance_analyzer_agent=ComplianceAnalyzerAgent()
    )

    audit_report_repository = AuditReportRepositoryAsync(
        db_name="hacktok",
        collection_name="audit_reports"
    )

    audit_report_service = AuditReportService(
        audit_report_repository=audit_report_repository
    )

    compliance_action_service = ComplianceActionService(
        audit_report_service=audit_report_service,
        feature_service=feature_service
    )

    setup_routes(app, feature_service=feature_service,
                 source_service=source_service,
                 source_content_service=source_content_service,
                 knowledge_base_service=knowledge_base_service,
                 compliance_analysis_service=compliance_analysis_service,
                 audit_report_service=audit_report_service,
                 compliance_action_service=compliance_action_service)

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
