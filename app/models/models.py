from typing import Optional
from sqlmodel import Field, SQLModel


class PlaceholderBase(SQLModel):
    """Base model for placeholder data."""
    title: str
    description: Optional[str] = None
    status: str = "active"


class Placeholder(PlaceholderBase, table=True):
    """Placeholder database model."""
    id: Optional[int] = Field(default=None, primary_key=True)


class PlaceholderCreate(PlaceholderBase):
    """Schema for creating new placeholder records."""
    pass


class PlaceholderResponse(PlaceholderBase):
    """Schema for placeholder responses."""
    id: int