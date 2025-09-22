from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

class FormUser(BaseModel):
    name: str
    balance: float

class FormPay(BaseModel):
    payer: int
    amount: float
    receiver: int
    reason: str

app = FastAPI()

@app.post('/create-user')
async def create_user(data: Annotated[FormUser, Form()]):
    user = User(name=data.name, balance=data.balance)
    user.save()
    return data


@app.get('/pay')
async def pay(data: Annotated[FormPay, Form()]):
    payer = User.get(User.id == data.payer)
    receiver = User.get(User.id == data.receiver)
    return payer.pay(data.amount, receiver, data.reason)
