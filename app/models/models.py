from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


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


class StoryBase(SQLModel):
    """Base model for story data."""
    title: str
    content: str
    author: Optional[str] = None
    category: Optional[str] = None
    published: bool = False


class Story(StoryBase, table=True):
    """Story database model."""
    id: Optional[int] = Field(default=None, primary_key=True)


class StoryCreate(StoryBase):
    """Schema for creating new story records."""
    pass


class StoryUpdate(SQLModel):
    """Schema for updating story records."""
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    published: Optional[bool] = None


class StoryResponse(StoryBase):
    """Schema for story responses."""
    id: int