from decimal import Decimal
from pydantic import BaseModel, EmailStr
from datetime import datetime


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    balance: Decimal


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
