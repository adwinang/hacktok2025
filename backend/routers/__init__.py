"""
FastAPI Routers package for organizing application endpoints.

This module provides a centralized router registration system following
enterprise patterns and FastAPI best practices, equivalent to Flask blueprints.
"""

from fastapi import FastAPI
from .health import health_router
from .features import feature_router
from .sources import source_router
from .chat import chat_router
from .knowledge_base import knowledge_base_router


def register_routers(app: FastAPI, **services):
    """
    Register all application routers with their dependencies.

    Args:
        app: FastAPI application instance
        **services: Service dependencies to inject into routers
    """
    # Register health routes (no dependencies)
    app.include_router(health_router)

    # Register feature routes
    feature_router.feature_service = services["feature_service"]
    app.include_router(feature_router)

    # Register source routes
    source_router.source_service = services["source_service"]
    app.include_router(source_router)

    # Register chat routes with dependencies
    app.include_router(chat_router)

    # Register knowledge base routes
    app.include_router(knowledge_base_router)


__all__ = ['register_routers']
