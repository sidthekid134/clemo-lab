import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.models import Story


def test_create_story(client: TestClient, session: Session):
    """Test creating a story."""
    response = client.post(
        "/stories/",
        json={
            "title": "Test Story",
            "content": "This is a test story content.",
            "author": "Test Author",
            "category": "Test"
        },
    )
    data = response.json()
    
    assert response.status_code == 201
    assert data["title"] == "Test Story"
    assert data["content"] == "This is a test story content."
    assert data["author"] == "Test Author"
    assert data["category"] == "Test"
    assert data["published"] == False
    assert "id" in data


def test_read_stories(client: TestClient, session: Session):
    """Test reading all stories."""
    # Create test story
    story = Story(
        title="Test Story",
        content="This is a test story content.",
        author="Test Author"
    )
    session.add(story)
    session.commit()
    
    response = client.get("/stories/")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Test Story"
    assert data[0]["id"] == story.id


def test_read_story(client: TestClient, session: Session):
    """Test reading a specific story."""
    story = Story(
        title="Test Story",
        content="This is a test story content."
    )
    session.add(story)
    session.commit()
    
    response = client.get(f"/stories/{story.id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data["title"] == "Test Story"
    assert data["content"] == "This is a test story content."
    assert data["id"] == story.id


def test_update_story(client: TestClient, session: Session):
    """Test updating a story."""
    story = Story(
        title="Old Title",
        content="Old content"
    )
    session.add(story)
    session.commit()
    
    response = client.patch(
        f"/stories/{story.id}",
        json={"title": "New Title", "content": "Updated content"}
    )
    data = response.json()
    
    assert response.status_code == 200
    assert data["title"] == "New Title"
    assert data["content"] == "Updated content"


def test_publish_story(client: TestClient, session: Session):
    """Test publishing a story."""
    story = Story(
        title="Test Story",
        content="Test content",
        published=False
    )
    session.add(story)
    session.commit()
    
    response = client.put(f"/stories/{story.id}/publish")
    data = response.json()
    
    assert response.status_code == 200
    assert data["published"] == True


def test_unpublish_story(client: TestClient, session: Session):
    """Test unpublishing a story."""
    story = Story(
        title="Test Story",
        content="Test content",
        published=True
    )
    session.add(story)
    session.commit()
    
    response = client.put(f"/stories/{story.id}/unpublish")
    data = response.json()
    
    assert response.status_code == 200
    assert data["published"] == False


def test_delete_story(client: TestClient, session: Session):
    """Test deleting a story."""
    story = Story(
        title="Test Story",
        content="Test content"
    )
    session.add(story)
    session.commit()
    
    response = client.delete(f"/stories/{story.id}")
    
    assert response.status_code == 204
    
    # Verify story is deleted
    get_response = client.get(f"/stories/{story.id}")
    assert get_response.status_code == 404


def test_filter_stories_by_published(client: TestClient, session: Session):
    """Test filtering stories by published status."""
    # Add published story
    published_story = Story(
        title="Published Story",
        content="Published content",
        published=True
    )
    session.add(published_story)
    
    # Add unpublished story
    unpublished_story = Story(
        title="Unpublished Story",
        content="Unpublished content",
        published=False
    )
    session.add(unpublished_story)
    session.commit()
    
    # Get published stories
    response = client.get("/stories/?published=true")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Published Story"
    
    # Get unpublished stories
    response = client.get("/stories/?published=false")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Unpublished Story"


def test_filter_stories_by_category(client: TestClient, session: Session):
    """Test filtering stories by category."""
    # Add story with category 'fiction'
    fiction_story = Story(
        title="Fiction Story",
        content="Fiction content",
        category="fiction"
    )
    session.add(fiction_story)
    
    # Add story with category 'non-fiction'
    non_fiction_story = Story(
        title="Non-Fiction Story",
        content="Non-fiction content",
        category="non-fiction"
    )
    session.add(non_fiction_story)
    session.commit()
    
    # Get fiction stories
    response = client.get("/stories/?category=fiction")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Fiction Story"
    
    # Get non-fiction stories
    response = client.get("/stories/?category=non-fiction")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Non-Fiction Story"