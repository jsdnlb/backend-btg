from fastapi import APIRouter

from controllers.transaction import (
    create_transaction,
    get_transaction,
    get_transactions,
)
from models.transaction import Transaction, TransactionCreate


routes_transaction = APIRouter()


@routes_transaction.post("/create", response_model=Transaction)
def create(transaction: TransactionCreate):
    return create_transaction(transaction.dict())


@routes_transaction.get("/get/{id}")
def get_by_id(id: str):
    return get_transaction(id)


@routes_transaction.get("/all")
def get_all():
    return get_transactions()
