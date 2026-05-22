from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

class APIEnvelope(BaseModel, Generic[T]):
    """Standard generic wrapper representing consistent API output schema."""
    success: bool
    data: Optional[T] = None
    error: Optional[Any] = None
    timestamp: str
