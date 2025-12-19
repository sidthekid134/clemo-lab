import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.models import Placeholder


def test_create_placeholder(client: TestClient, session: Session):
    """Test creating a placeholder."""
    response = client.post(
        "/placeholders/",
        json={"title": "Test Placeholder", "description": "Test description"},
    )
    data = response.json()
    
    assert response.status_code == 201
    assert data["title"] == "Test Placeholder"
    assert data["description"] == "Test description"
    assert data["status"] == "active"
    assert "id" in data


def test_read_placeholders(client: TestClient, session: Session):
    """Test reading all placeholders."""
    # Create test placeholder
    placeholder = Placeholder(title="Test Placeholder")
    session.add(placeholder)
    session.commit()
    
    response = client.get("/placeholders/")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Test Placeholder"
    assert data[0]["id"] == placeholder.id


def test_read_placeholder(client: TestClient, session: Session):
    """Test reading a specific placeholder."""
    placeholder = Placeholder(title="Test Placeholder")
    session.add(placeholder)
    session.commit()
    
    response = client.get(f"/placeholders/{placeholder.id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data["title"] == "Test Placeholder"
    assert data["id"] == placeholder.id


def test_update_placeholder(client: TestClient, session: Session):
    """Test updating a placeholder."""
    placeholder = Placeholder(title="Old Title")
    session.add(placeholder)
    session.commit()
    
    response = client.put(
        f"/placeholders/{placeholder.id}",
        json={"title": "New Title", "description": "Updated description"},
    )
    data = response.json()
    
    assert response.status_code == 200
    assert data["title"] == "New Title"
    assert data["description"] == "Updated description"


def test_delete_placeholder(client: TestClient, session: Session):
    """Test deleting a placeholder."""
    placeholder = Placeholder(title="Test Placeholder")
    session.add(placeholder)
    session.commit()
    
    response = client.delete(f"/placeholders/{placeholder.id}")
    
    assert response.status_code == 204
    
    # Verify placeholder is deleted
    get_response = client.get(f"/placeholders/{placeholder.id}")
    assert get_response.status_code == 404