"""
Rate limiting configuration using slowapi
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse


# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60/minute"],
    storage_uri="memory://"
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """Custom handler for rate limit exceeded errors"""
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please try again later.",
            "error_code": "RATE_LIMIT_EXCEEDED",
            "path": str(request.url)
        },
        headers={
            "Retry-After": str(exc.detail)
        }
    )


# Rate limit configurations for different endpoints
RATE_LIMITS = {
    "login": "5/minute",
    "register": "3/minute",
    "forgot_password": "3/minute",
    "reset_password": "5/minute",
    "upload": "10/minute",
    "general": "60/minute",
    "strict": "30/minute"
}
