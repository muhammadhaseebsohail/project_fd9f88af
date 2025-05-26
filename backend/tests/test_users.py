Here are the unit tests for the FastAPI endpoints using pytest and FastAPI's TestClient:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base
from app.schemas import UserCreate, MessageCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = get_db_override
    with TestClient(app) as client:
        yield client

def get_db_override():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user(client):
    user = UserCreate(name="Alice", email="alice@example.com")
    response = client.post("/users/", json=user.dict())
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == user.name
    assert data["email"] == user.email
    assert "id" in data

def test_read_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["id"] == 1

def test_read_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "User not found"}

def test_create_message_for_user(client):
    message = MessageCreate(content="Hello, World!")
    response = client.post("/users/1/messages/", json=message.dict())
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] == message.content
    assert data["author_id"] == 1
    assert "id" in data
    assert "created_at" in data

def test_read_messages(client):
    response = client.get("/messages/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["content"] == "Hello, World!"
    assert data[0]["author_id"] == 1
    assert "id" in data[0]
    assert "created_at" in data[0]
```

This includes tests for success cases where we expect the API to return a 200 status code and for the case where we expect a 404 error. It also tests that the data returned by the API is as expected.

The get_db_override function is used to override the actual database session with a test session. The client fixture is used to provide a TestClient instance for the tests.

Note: You should remove or reset the test database after running the tests to ensure a clean state for each test run.