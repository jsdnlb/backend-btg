from fastapi import APIRouter

from controllers.fund import cancel_fund, create_fund, get_fund, get_funds, subscribe
from models.fund import Cancellation, Fund, FundCreate, Subscription


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


@routes_fund.post("/subscribe/")
def subscribe_fund(subscription: Subscription):
    return subscribe(subscription)


@routes_fund.post("/cancel/")
def cancel_subscription(cancellation: Cancellation):
    return cancel_fund(cancellation)
