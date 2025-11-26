"""
Custom exception classes and centralized error handling
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional


class BaseAPIException(HTTPException):
    """Base exception for API errors"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code or f"ERR_{status_code}"


class UserNotFoundException(BaseAPIException):
    """Raised when user is not found"""
    def __init__(self, detail: str = "User not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="USER_NOT_FOUND"
        )


class UserAlreadyExistsException(BaseAPIException):
    """Raised when user already exists"""
    def __init__(self, detail: str = "User already exists"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="USER_ALREADY_EXISTS"
        )


class InvalidCredentialsException(BaseAPIException):
    """Raised when credentials are invalid"""
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="INVALID_CREDENTIALS",
            headers={"WWW-Authenticate": "Bearer"}
        )


class TokenExpiredException(BaseAPIException):
    """Raised when token has expired"""
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="TOKEN_EXPIRED",
            headers={"WWW-Authenticate": "Bearer"}
        )


class InsufficientPermissionsException(BaseAPIException):
    """Raised when user doesn't have required permissions"""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="INSUFFICIENT_PERMISSIONS"
        )


class RoleNotFoundException(BaseAPIException):
    """Raised when role is not found"""
    def __init__(self, detail: str = "Role not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="ROLE_NOT_FOUND"
        )


class PermissionNotFoundException(BaseAPIException):
    """Raised when permission is not found"""
    def __init__(self, detail: str = "Permission not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="PERMISSION_NOT_FOUND"
        )


class FileUploadException(BaseAPIException):
    """Raised when file upload fails"""
    def __init__(self, detail: str = "File upload failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="FILE_UPLOAD_ERROR"
        )


class DatabaseException(BaseAPIException):
    """Raised when database operation fails"""
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR"
        )


async def base_api_exception_handler(request: Request, exc: BaseAPIException):
    """Handler for custom API exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.error_code,
            "path": str(request.url)
        },
        headers=exc.headers
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler for standard HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "path": str(request.url)
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handler for unhandled exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "path": str(request.url)
        }
    )
