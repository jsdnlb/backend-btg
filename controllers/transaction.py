from datetime import datetime
from uuid import uuid4
from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key
from models.transaction import TransactionCreate

table = dynamodb.Table("transactions")


def create_transaction(transaction: TransactionCreate):
    try:
        transaction_id = str(uuid4())
        created_at = datetime.now().isoformat()
        new_transaction = {
            "id": transaction_id,
            "type": transaction["type"],
            "date": transaction["date"].isoformat(),
            "amount": transaction["amount"],
            "client_id": transaction["client_id"],
            "fund_id": transaction["fund_id"],
            "notification": transaction["notification"],
            "created_at": created_at,
        }

        table.put_item(Item=new_transaction)
        return new_transaction
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_transaction(id: str):
    try:
        response = table.query(KeyConditionExpression=Key("id").eq(id))
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_transactions():
    try:
        response = table.scan(Limit=100)
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
