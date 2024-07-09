from fastapi import APIRouter
from controllers.client import create_client, get_client, get_clients
from models.client import Client, ClientCreate


routes_client = APIRouter()


@routes_client.post("/create", response_model=Client)
def create(user: ClientCreate):
    return create_client(user.dict())


@routes_client.get("/get/{id}")
def get_by_id(id: str):
    return get_client(id)


@routes_client.get("/all")
def get_all():
    return get_clients()
