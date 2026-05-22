from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class DealBaseSchema(BaseModel):
    name: str = Field(..., max_length=255, description="Deal title or client name")
    value: Decimal = Field(Decimal("0.00"), ge=Decimal("0.00"), description="Deal value size")
    stage: str = Field("PROSPECTING", description="Pipeline stage of the deal (e.g. PROSPECTING, CLOSED_WON)")
    probability: int = Field(10, ge=0, le=100, description="Win likelihood probability percent")
    close_date: Optional[date] = Field(None, description="Expected close date")


class DealCreateSchema(DealBaseSchema):
    """Input payload schema for creating a new Deal."""
    pass


class DealUpdateSchema(BaseModel):
    """Input payload schema for updating an existing Deal."""
    name: Optional[str] = Field(None, max_length=255)
    value: Optional[Decimal] = Field(None, ge=Decimal("0.00"))
    stage: Optional[str] = None
    probability: Optional[int] = Field(None, ge=0, le=100)
    close_date: Optional[date] = None


class DealSchema(DealBaseSchema):
    """Output serializable representation of a Deal."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 configuration to load from Django DB ORM objects
