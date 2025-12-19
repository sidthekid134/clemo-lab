from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database.database import get_session
from ..models.models import Placeholder, PlaceholderCreate, PlaceholderResponse

router = APIRouter(
    prefix="/placeholders",
    tags=["placeholders"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=PlaceholderResponse, status_code=status.HTTP_201_CREATED)
def create_placeholder(placeholder: PlaceholderCreate, session: Session = Depends(get_session)):
    """Create a new placeholder."""
    db_placeholder = Placeholder.from_orm(placeholder)
    session.add(db_placeholder)
    session.commit()
    session.refresh(db_placeholder)
    return db_placeholder


@router.get("/", response_model=List[PlaceholderResponse])
def read_placeholders(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """Get all placeholders."""
    placeholders = session.exec(select(Placeholder).offset(skip).limit(limit)).all()
    return placeholders


@router.get("/{placeholder_id}", response_model=PlaceholderResponse)
def read_placeholder(placeholder_id: int, session: Session = Depends(get_session)):
    """Get a placeholder by ID."""
    placeholder = session.get(Placeholder, placeholder_id)
    if placeholder is None:
        raise HTTPException(status_code=404, detail="Placeholder not found")
    return placeholder


@router.put("/{placeholder_id}", response_model=PlaceholderResponse)
def update_placeholder(
    placeholder_id: int, placeholder: PlaceholderCreate, session: Session = Depends(get_session)
):
    """Update a placeholder."""
    db_placeholder = session.get(Placeholder, placeholder_id)
    if db_placeholder is None:
        raise HTTPException(status_code=404, detail="Placeholder not found")
    
    placeholder_data = placeholder.dict(exclude_unset=True)
    for key, value in placeholder_data.items():
        setattr(db_placeholder, key, value)
    
    session.add(db_placeholder)
    session.commit()
    session.refresh(db_placeholder)
    return db_placeholder


@router.delete("/{placeholder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_placeholder(placeholder_id: int, session: Session = Depends(get_session)):
    """Delete a placeholder."""
    placeholder = session.get(Placeholder, placeholder_id)
    if placeholder is None:
        raise HTTPException(status_code=404, detail="Placeholder not found")
    
    session.delete(placeholder)
    session.commit()
    return None