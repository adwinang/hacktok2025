"""
Health check and system status routes.

This module contains routes for application health monitoring and basic
system information endpoints.
"""

from fastapi import APIRouter

# Create router for health-related routes
health_router = APIRouter(tags=["health"])


@health_router.get("/")
async def hello_world():
    """
    Basic health check endpoint.

    Returns:
        str: Simple greeting message indicating the service is running
    """
    return 'Hello, World!'
