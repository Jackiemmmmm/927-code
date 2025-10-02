import os
import httpx
from fastapi import APIRouter, HTTPException, Request, Response
from typing import Any

router = APIRouter()

# Microservices configuration
# Use environment variables for Docker, fallback to localhost for local development
APPOINTMENTS_SERVICE_URL = os.getenv(
    "APPOINTMENTS_SERVICE_URL",
    "http://localhost:8001/api/v1/appointments"
)
ITEMS_SERVICE_URL = os.getenv(
    "ITEMS_SERVICE_URL",
    "http://localhost:8002/api/v1/items"
)


async def proxy_request(
    service_url: str,
    path: str,
    request: Request,
) -> Response:
    """
    Proxy HTTP request to microservice
    """
    # Build target URL
    target_url = f"{service_url}{path}"

    # Get request body if exists
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()

    # Forward request to microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                headers={
                    key: value
                    for key, value in request.headers.items()
                    if key.lower() not in ["host", "content-length"]
                },
                content=body,
                timeout=30.0,
            )

            # Return response from microservice
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type"),
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail=f"Service unavailable. Please ensure the microservice is running.",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# Appointments Service Gateway Routes
@router.api_route(
    "/appointments/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    tags=["appointments-gateway"],
)
async def appointments_gateway(path: str, request: Request) -> Any:
    """
    Gateway to Appointments Service
    """
    return await proxy_request(APPOINTMENTS_SERVICE_URL, f"/{path}", request)


@router.api_route(
    "/appointments",
    methods=["GET", "POST"],
    tags=["appointments-gateway"],
)
async def appointments_root(request: Request) -> Any:
    """
    Gateway to Appointments Service root
    """
    return await proxy_request(APPOINTMENTS_SERVICE_URL, "", request)


# Items Service Gateway Routes
@router.api_route(
    "/items/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    tags=["items-gateway"],
)
async def items_gateway(path: str, request: Request) -> Any:
    """
    Gateway to Items Service
    """
    return await proxy_request(ITEMS_SERVICE_URL, f"/{path}", request)


@router.api_route(
    "/items",
    methods=["GET", "POST"],
    tags=["items-gateway"],
)
async def items_root(request: Request) -> Any:
    """
    Gateway to Items Service root
    """
    return await proxy_request(ITEMS_SERVICE_URL, "", request)
