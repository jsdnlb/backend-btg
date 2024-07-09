from datetime import datetime
from uuid import uuid4
from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key
from models.client import Client, ClientCreate

table = dynamodb.Table("clients")


def create_client(client: ClientCreate):
    try:
        client_id = str(uuid4())
        created_at = datetime.now().isoformat()
        new_client = {
            "id": client_id,
            "name": client["name"],
            "email": client["email"],
            "phone": client["phone"],
            "balance": client["balance"],
            "created_at": created_at,
        }
        table.put_item(Item=new_client)
        return new_client
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_client(id: str):
    try:
        response = table.query(KeyConditionExpression=Key("id").eq(id))
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_clients():
    try:
        response = table.scan(Limit=5)
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
