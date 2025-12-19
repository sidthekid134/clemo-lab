import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database.database import get_session
from app.models.models import Placeholder


@pytest.fixture(name="client")
def client_fixture():
    """Create FastAPI test client."""
    client = TestClient(app)
    return client


@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory database session for testing."""
    # Create in-memory database for testing
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Override the get_session dependency
        def get_session_override():
            return session
        
        app.dependency_overrides[get_session] = get_session_override
        
        yield session
        
    # Clean up
    app.dependency_overrides.clear()