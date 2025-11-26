"""
Structured logging configuration using loguru
"""
import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings


def setup_logging():
    """Configure structured logging with loguru"""
    
    # Remove default handler
    logger.remove()
    
    # Console handler with colors
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=getattr(settings, "LOG_LEVEL", "INFO"),
        colorize=True
    )
    
    # File handler with rotation
    log_path = Path(getattr(settings, "LOG_FILE_PATH", "logs/app.log"))
    log_path.parent.mkdir(exist_ok=True)
    
    logger.add(
        log_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=getattr(settings, "LOG_LEVEL", "INFO"),
        rotation=f"{getattr(settings, 'LOG_ROTATION_SIZE_MB', 500)} MB",
        retention="30 days",
        compression="zip",
        serialize=False
    )
    
    # Error file handler
    error_log_path = log_path.parent / "error.log"
    logger.add(
        error_log_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="100 MB",
        retention="60 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    return logger


# Initialize logger
app_logger = setup_logging()


def log_request(method: str, path: str, status_code: int, duration: float):
    """Log HTTP request"""
    app_logger.info(
        f"{method} {path} - Status: {status_code} - Duration: {duration:.2f}ms"
    )


def log_error(error: Exception, context: dict = None):
    """Log error with context"""
    app_logger.error(
        f"Error: {str(error)} | Context: {context or {}}"
    )


def log_auth_event(event: str, username: str, ip_address: str, success: bool):
    """Log authentication events"""
    level = "info" if success else "warning"
    getattr(app_logger, level)(
        f"Auth Event: {event} | User: {username} | IP: {ip_address} | Success: {success}"
    )


def log_database_operation(operation: str, table: str, record_id: int = None):
    """Log database operations"""
    app_logger.debug(
        f"DB Operation: {operation} | Table: {table} | ID: {record_id}"
    )
