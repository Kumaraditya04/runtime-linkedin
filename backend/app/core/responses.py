from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    meta: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: list[Any] = []

def success_response(message: str, data: Any = None, meta: Dict[str, Any] = None) -> StandardResponse:
    return StandardResponse(success=True, message=message, data=data, meta=meta)

def error_response(message: str, errors: list[Any] = None) -> ErrorResponse:
    return ErrorResponse(success=False, message=message, errors=errors or [])
