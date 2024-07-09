from datetime import datetime
from uuid import uuid4
from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key
from models.fund import FundCreate

table = dynamodb.Table("funds")


def create_fund(fund: FundCreate):
    try:
        fund_id = str(uuid4())
        created_at = datetime.now().isoformat()
        new_fund = {
            "id": fund_id,
            "name": fund["name"],
            "min_amount": fund["min_amount"],
            "category": fund["category"],
            "created_at": created_at,
        }

        table.put_item(Item=new_fund)
        return new_fund
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_fund(id: str):
    try:
        response = table.query(KeyConditionExpression=Key("id").eq(id))
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_funds():
    try:
        response = table.scan(Limit=5)
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
