from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime


class TransactionBase(BaseModel):
    type: str
    date: datetime
    amount: Decimal
    client_id: str
    fund_id: str
    notification: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
