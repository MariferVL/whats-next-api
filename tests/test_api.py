import json
import pytest
from datetime import datetime
from app import create_app
from app.extensions import db
from app.utils.validators import is_valid_session_schedule


@pytest.fixture(scope="module")
def test_client():
    """
    Creates a Flask test client using an in-memory SQLite database.
    The JWT secret and testing configuration are also set here.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test_secret_key"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def get_auth_token(client):
    """
    Helper function to register a user and obtain a JWT token.
    """
    user_data = {"email": "testuser@example.com", "password": "securepassword"}
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    response_json = login_response.get_json()
    return response_json.get("token")


# -----------------------------
# Authentication Endpoint Tests
# -----------------------------

def test_register_missing_fields(test_client):
    """
    Test registration endpoint returns error when required fields are missing.
    """
    response = test_client.post("/auth/register", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data


def test_register_existing_user(test_client):
    """
    Test registering an already registered user returns a proper error.
    """
    user_data = {"email": "existinguser@example.com", "password": "mypassword"}
    first_response = test_client.post("/auth/register", json=user_data)
    assert first_response.status_code == 201

    second_response = test_client.post("/auth/register", json=user_data)
    assert second_response.status_code == 400
    data = second_response.get_json()
    assert "message" in data


def test_login_invalid_credentials(test_client):
    """
    Test that login with invalid credentials fails.
    """
    user_data = {"email": "invalid@example.com", "password": "wrongpassword"}
    response = test_client.post("/auth/login", json=user_data)
    assert response.status_code == 401
    data = response.get_json()
    assert "message" in data


def test_login_valid(test_client):
    """
    Test that a valid login returns a JWT token.
    """
    user_data = {"email": "validuser@example.com", "password": "validpassword"}
    test_client.post("/auth/register", json=user_data)
    response = test_client.post("/auth/login", json=user_data)
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data


# -----------------------------
# Class Sessions Endpoint Tests
# -----------------------------

def test_get_classes_empty(test_client):
    """
    Test GET /api/classes returns an empty list when there are no class sessions.
    """
    response = test_client.get("/api/classes")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_create_class_session(test_client):
    """
    Test creating a new class session with valid data.
    """
    token = get_auth_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    class_data = {
        "title": "Test Class Session",
        "date": "25-03-2025",         
        "start_time": "10:00",
        "end_time": "11:00",
        "professor_id": 1,
        "session_type": "class"
    }
    response = test_client.post("/api/classes", json=class_data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert "data" in data
    assert "id" in data["data"]


def test_create_class_session_missing_field(test_client):
    """
    Test creating a class session with a missing required field.
    """
    token = get_auth_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    incomplete_data = {
        "title": "Incomplete Class Session",
        "start_time": "10:00",
        "end_time": "11:00",
        "professor_id": 1,
        "session_type": "class"
    }
    response = test_client.post("/api/classes", json=incomplete_data, headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_get_class_by_id(test_client):
    """
    Test retrieval of a specific class session by its ID.
    """
    token = get_auth_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    class_data = {
        "title": "Retrieve Class Session",
        "date": "25-03-2025",
        "start_time": "10:00",
        "end_time": "11:00",
        "professor_id": 1,
        "session_type": "class"
    }
    creation_response = test_client.post("/api/classes", json=class_data, headers=headers)
    session_id = creation_response.get_json()["data"]["id"]

    response = test_client.get(f"/api/classes/{session_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == session_id


def test_update_class_session(test_client):
    """
    Test updating an existing class session.
    """
    token = get_auth_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    class_data = {
        "title": "Original Class Session",
        "date": "25-03-2025",
        "start_time": "10:00",
        "end_time": "11:00",
        "professor_id": 1,
        "session_type": "class"
    }
    creation_response = test_client.post("/api/classes", json=class_data, headers=headers)
    session_id = creation_response.get_json()["data"]["id"]

    update_data = {
        "title": "Updated Class Session",
        "date": "26-03-2025",         # Change date (still an allowed day)
        "start_time": "10:30",
        "end_time": "11:30",
        "professor_id": 2,
        "session_type": "class"
    }
    response = test_client.put(f"/api/classes/{session_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


def test_delete_class_session(test_client):
    """
    Test deletion of an existing class session.
    """
    token = get_auth_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    class_data = {
        "title": "Session to Delete",
        "date": "25-03-2025",
        "start_time": "10:00",
        "end_time": "11:00",
        "professor_id": 1,
        "session_type": "class"
    }
    creation_response = test_client.post("/api/classes", json=class_data, headers=headers)
    session_id = creation_response.get_json()["data"]["id"]

    response = test_client.delete(f"/api/classes/{session_id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data

    
# -----------------------------
# Schedule Endpoint Tests
# -----------------------------

def test_get_schedule_missing_date(test_client):
    """
    Test that the schedule endpoint returns an error when the 'date' query parameter is missing.
    """
    response = test_client.get("/api/schedule")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_get_schedule_invalid_date(test_client):
    """
    Test that the schedule endpoint returns an error for an invalid date format.
    """
    response = test_client.get("/api/schedule?date=invalid-date")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_get_schedule_valid(test_client):
    """
    Test that the schedule endpoint returns a list of sessions for a valid date.
    """
    token = get_auth_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    session_date = "25-03-2025"
    class_data = {
        "title": "Schedule Test Session",
        "date": session_date,
        "start_time": "10:00",
        "end_time": "11:00",
        "professor_id": 1,
        "session_type": "class"
    }
    test_client.post("/api/classes", json=class_data, headers=headers)
    response = test_client.get(f"/api/schedule?date={session_date}")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


# -----------------------------
# Main Route Test
# -----------------------------

def test_main_welcome(test_client):
    """
    Test that the main route ("/") renders the welcome page successfully.
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data or b"Welcome" in response.data


# -----------------------------
# Unit Tests for Validators
# -----------------------------

def test_valid_schedule_class():
    """
    Unit test for a valid 'class' session schedule.
    """
    valid, message = is_valid_session_schedule("class", "25-03-2025", "10:00", "11:00")
    assert valid, f"Expected valid schedule, got error: {message}"


def test_invalid_schedule_class_wrong_day():
    """
    Unit test for an invalid 'class' session scheduled on an unsupported day.
    (Assumes that 29-03-2025 is not between Monday and Thursday.)
    """
    valid, message = is_valid_session_schedule("class", "29-03-2025", "10:00", "11:00")
    assert not valid, "Expected invalid schedule due to wrong day"


def test_valid_schedule_qa():
    """
    Unit test for a valid Q&A session scheduled on Friday.
    (Assumes that the given date is a Friday.)
    """
    valid, message = is_valid_session_schedule("qa", "04-04-2025", "10:00", "11:00")
    assert valid, f"Expected valid QA session schedule, got error: {message}"


def test_invalid_schedule_qa_wrong_day():
    """
    Unit test for an invalid Q&A session scheduled on a non-Friday.
    """
    valid, message = is_valid_session_schedule("qa", "25-03-2025", "10:00", "11:00")
    assert not valid, "Expected invalid QA session schedule due to wrong day"
