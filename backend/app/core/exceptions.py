from typing import Any, Optional, Dict

class VyoraBaseException(Exception):
    """Base exception class for all domain-specific errors."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details

class EntityNotFoundError(VyoraBaseException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(
            message=f"{entity_name} with identifier '{entity_id}' was not found.",
            code="ENTITY_NOT_FOUND",
            details={"entity": entity_name, "id": entity_id}
        )

class AuthenticationError(VyoraBaseException):
    def __init__(self, message: str = "Invalid authentication credentials."):
        super().__init__(message=message, code="AUTHENTICATION_FAILED")

class AuthorizationError(VyoraBaseException):
    def __init__(self, message: str = "You do not have permission to perform this action."):
        super().__init__(message=message, code="PERMISSION_DENIED")

class ValidationError(VyoraBaseException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message=message, code="VALIDATION_FAILED", details=details)

class ConflictError(VyoraBaseException):
    def __init__(self, message: str):
        super().__init__(message=message, code="CONFLICT")

class InsufficientEvidenceError(VyoraBaseException):
    def __init__(self, coverage_percentage: float):
        super().__init__(
            message=f"Insufficient data evidence ({coverage_percentage:.1f}%) to calculate composite score.",
            code="INSUFFICIENT_EVIDENCE",
            details={"coverage_percentage": coverage_percentage}
        )
