from fastapi import APIRouter

from controllers.fund import create_fund, get_fund, get_funds
from models.fund import Fund, FundCreate


routes_fund = APIRouter()


@routes_fund.post("/create", response_model=Fund)
def create(fund: FundCreate):
    return create_fund(fund.dict())


@routes_fund.get("/get/{id}")
def get_by_id(id: str):
    return get_fund(id)


@routes_fund.get("/all")
def get_all():
    return get_funds()
