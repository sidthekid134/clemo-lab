from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ..database.database import get_session
from ..models.models import Story, StoryCreate, StoryResponse, StoryUpdate

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=StoryResponse, status_code=status.HTTP_201_CREATED)
def create_story(story: StoryCreate, session: Session = Depends(get_session)):
    """Create a new story."""
    db_story = Story.from_orm(story)
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story


@router.get("/", response_model=List[StoryResponse])
def read_stories(
    skip: int = 0, 
    limit: int = 100, 
    published: Optional[bool] = None,
    category: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """Get all stories with optional filtering."""
    query = select(Story)
    
    # Apply filters if provided
    if published is not None:
        query = query.where(Story.published == published)
    
    if category:
        query = query.where(Story.category == category)
    
    stories = session.exec(query.offset(skip).limit(limit)).all()
    return stories


@router.get("/{story_id}", response_model=StoryResponse)
def read_story(story_id: int, session: Session = Depends(get_session)):
    """Get a story by ID."""
    story = session.get(Story, story_id)
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.patch("/{story_id}", response_model=StoryResponse)
def update_story(
    story_id: int, story_update: StoryUpdate, session: Session = Depends(get_session)
):
    """Update a story."""
    db_story = session.get(Story, story_id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    
    story_data = story_update.dict(exclude_unset=True)
    for key, value in story_data.items():
        setattr(db_story, key, value)
    
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story


@router.put("/{story_id}/publish", response_model=StoryResponse)
def publish_story(story_id: int, session: Session = Depends(get_session)):
    """Publish a story."""
    db_story = session.get(Story, story_id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    
    db_story.published = True
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story


@router.put("/{story_id}/unpublish", response_model=StoryResponse)
def unpublish_story(story_id: int, session: Session = Depends(get_session)):
    """Unpublish a story."""
    db_story = session.get(Story, story_id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    
    db_story.published = False
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(story_id: int, session: Session = Depends(get_session)):
    """Delete a story."""
    story = session.get(Story, story_id)
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    
    session.delete(story)
    session.commit()
    return None