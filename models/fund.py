from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime


class FundBase(BaseModel):
    name: str
    min_amount: Decimal
    category: str


class FundCreate(FundBase):
    pass


class Fund(FundBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
