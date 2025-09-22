from typing import Annotated, List, Dict, Any
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from models import User, CreditCard, Feed
from database import create_tables, close_connection, db, Friendship
from minivenmo import MiniVenmo
from typing import List


class FormUser(BaseModel):
    name: str
    balance: float


class FormPay(BaseModel):
    payer: int
    amount: float
    receiver: int
    reason: str


class FriendRequest(BaseModel):
    user_id: int
    friend_id: int


# Pydantic models
class UserResponse(BaseModel):
    id: int
    name: str
    balance: float
    created_at: str = None


class ActivityResponse(BaseModel):
    id: int
    type: str
    user_id: int
    user_name: str
    detail: str
    created_at: str
    related_user_id: int = None
    related_user_name: str = None


app = FastAPI()


# Initialize database tables on startup
@app.on_event("startup")
def startup():
    create_tables()


# Close database connection on shutdown
@app.on_event("shutdown")
def shutdown():
    close_connection()


@app.post("/create-user")
async def create_user(user_data: FormUser):
    try:
        with db.atomic():
            user = User.create(name=user_data.name, balance=user_data.balance)
            return {"id": user.id, "name": user.name, "balance": user.balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/pay")
async def pay(data: FormPay):
    try:
        payer = User.get(User.id == data.payer)
        receiver = User.get(User.id == data.receiver)
        result = payer.pay(data.amount, receiver, data.reason)
        return result
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# List all users
@app.get("/users", response_model=List[UserResponse])
async def list_users():
    """
    Get a list of all users with their basic information
    """
    try:
        users = []
        for user in User.select():
            user_data = {
                "id": user.id,
                "name": user.name,
                "balance": user.balance,
            }
            if hasattr(user, "created_at"):
                user_data["created_at"] = user.created_at.isoformat()
            users.append(user_data)
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get user activity
@app.get("/users/{user_id}/activity", response_model=List[Dict[str, Any]])
async def get_user_activity(user_id: int):
    try:
        user = User.get(User.id == user_id)
        activities = user.retrieve_activity()

        formatted_activities = []
        for activity in activities:
            activity_data = {
                "id": activity.id,
                "type": activity.feed_type,
                "user_id": activity.user.id,
                "user_name": activity.user.name,
                "detail": activity.detail,
                "created_at": activity.created_at.isoformat(),
            }

            if activity.related_user:
                activity_data.update(
                    {
                        "related_user_id": activity.related_user.id,
                        "related_user_name": activity.related_user.name,
                    }
                )

            formatted_activities.append(activity_data)

        return formatted_activities

    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/users/add-friend")
async def add_friend(friend_request: FriendRequest):
    """
    Add a friend for the specified user

    - **user_id**: ID of the user who wants to add a friend
    - **friend_id**: ID of the user to be added as a friend (from request body)
    """
    try:
        user = User.get(User.id == friend_request.user_id)
        friend = User.get(User.id == friend_request.friend_id)

        result = user.add_friend(friend)
        return result

    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
