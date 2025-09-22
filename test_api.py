import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from main import app
from models import User, Feed, CreditCard, Friendship
from database import db

# Test data
test_user1 = {"name": "Test User 1", "balance": 1000.0}
test_user2 = {"name": "Test User 2", "balance": 500.0}

@pytest.fixture(scope="module")
def client():
    # Setup test database
    db.connect()
    db.create_tables([User, Feed, CreditCard, Friendship], safe=True)
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Teardown - drop tables in the correct order to avoid foreign key constraint errors
    db.drop_tables([Friendship, Feed, CreditCard, User], safe=True)
    db.close()

def test_create_user(client):
    # Test successful user creation
    response = client.post("/create-user", json=test_user1)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_user1["name"]
    assert data["balance"] == test_user1["balance"]
    assert "id" in data
    test_user1["id"] = data["id"]

    # Test creating another user with same name (should create new user)
    response = client.post("/create-user", json=test_user1)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_user1["name"]
    assert data["id"] != test_user1["id"]  # Should be a new user with new ID

def test_list_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0
    assert any(user["name"] == test_user1["name"] for user in users)

def test_add_friend(client):
    # Create second user if not exists
    if "id" not in test_user2:
        response = client.post("/create-user", json=test_user2)
        test_user2["id"] = response.json()["id"]

    # Add friend
    friend_request = {"user_id": test_user1["id"], "friend_id": test_user2["id"]}
    response = client.post("/users/add-friend", json=friend_request)
    assert response.status_code == 200
    assert "Successfully added" in response.json()["message"]

    # Test adding duplicate friend
    response = client.post("/users/add-friend", json=friend_request)
    assert response.status_code == 400
    assert "is already your friend" in response.json()["detail"]

def test_get_activity(client):
    response = client.get(f"/users/{test_user1['id']}/activity")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, list)

def test_payment(client):
    # Make sure both users exist
    if "id" not in test_user1:
        response = client.post("/create-user", json=test_user1)
        test_user1["id"] = response.json()["id"]
    if "id" not in test_user2:
        response = client.post("/create-user", json=test_user2)
        test_user2["id"] = response.json()["id"]
    
    payment_data = {
        "payer": test_user1["id"],
        "amount": 100.0,
        "receiver": test_user2["id"],
        "reason": "Test payment"
    }
    response = client.post("/pay", json=payment_data)
    assert response.status_code == 200
    # assert "paid" in response.json()["message"].lower()

    # # Test insufficient balance
    # payment_data["amount"] = 10000.0
    # response = client.post("/pay", json=payment_data)
    # assert response.status_code == 200
    # response_data = response.json()
    # assert "error" in response_data
    # assert "not enough balance" in response_data["error"].lower()