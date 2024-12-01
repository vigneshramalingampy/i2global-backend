from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import (
    JSONResponse,
)  # Import this to create proper HTTP responses
from starlette.requests import Request

from src.i2global_backend.api.auth.jwt_token_generator import verify_token

excluded_path = [
    "/docs",
	"/redoc",
    "/user/login",
    "/openapi.json",
    "/user/signin",
	]


class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            print("/docs" in excluded_path)
            if request.url.path in excluded_path:
                print("hi")
                return await call_next(request)

            # Get Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    status_code=401,
                    content={
                        "status": "error",
                        "message": "Authorization header is missing or invalid",
                    },
                )

            # Extract and verify token
            token_id = auth_header.split("Bearer ")[-1]
            payload = verify_token(token_id)

            if not payload:
                return JSONResponse(
                    status_code=401,
                    content={"status": "error", "message": "Invalid or expired token"},
                )

            # If token is valid, proceed with the request
            return await call_next(request)

        except Exception as exception:
            return JSONResponse(
                status_code=500, content={"status": "error", "message": str(exception)}
            )