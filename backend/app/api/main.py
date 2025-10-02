from fastapi import APIRouter

from app.api.routes import gateway, login, private, users, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)

# API Gateway - proxy requests to microservices
api_router.include_router(gateway.router)

# Original routes (commented out - now using microservices via gateway)
# from app.api.routes import appointments, items
# api_router.include_router(items.router)
# api_router.include_router(appointments.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
