from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException
from controllers.transaction import get_transaction
from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key
from models.fund import Cancellation, FundCreate, Subscription
from utils.utils_controller import general_validation

funds_table = dynamodb.Table("funds")
clients_table = dynamodb.Table("clients")
transactions_table = dynamodb.Table("transactions")


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

        funds_table.put_item(Item=new_fund)
        return new_fund
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_fund(id: str):
    try:
        response = funds_table.query(KeyConditionExpression=Key("id").eq(id))
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_funds():
    try:
        response = funds_table.scan(Limit=5)
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def subscribe(subscription: Subscription):
    # Validate that the client exists and that the notification time is correct
    client = general_validation(subscription.notification, subscription.client_id)
    try:
        fund = get_fund(subscription.fund_id)[0]
    except:
        raise HTTPException(status_code=404, detail="Fund not found")

    # Check if the subscription amount meets the minimum requirement
    if subscription.amount < fund["min_amount"]:
        raise HTTPException(
            status_code=400,
            detail="Subscription amount is less than the minimum required",
        )

    # Check if the client has enough balance
    if client["balance"] < subscription.amount:
        raise HTTPException(
            status_code=400,
            detail=f"No balance available to be linked to the fund {fund['name']}",
        )

    # Deduct the amount from client's balance
    new_balance = client["balance"] - subscription.amount
    clients_table.update_item(
        Key={"id": subscription.client_id},
        UpdateExpression="SET balance = :new_balance",
        ExpressionAttributeValues={":new_balance": new_balance},
    )

    # Create a new transaction
    transaction_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()
    new_transaction = {
        "id": transaction_id,
        "type": "Subscription",
        "date": created_at,
        "amount": subscription.amount,
        "client_id": subscription.client_id,
        "fund_id": subscription.fund_id,
        "notification": subscription.notification,
        "created_at": created_at,
    }
    transactions_table.put_item(Item=new_transaction)

    return new_transaction


def cancel_fund(cancellation: Cancellation):
    # Validate that the client exists and that the notification time is correct
    client = general_validation(cancellation.notification, cancellation.client_id)

    try:
        transaction = get_transaction(cancellation.transaction_id)[0]
    except:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Check if the transaction belongs to the client and is a subscription
    if (
        transaction["client_id"] != cancellation.client_id
        or transaction["type"] != "Subscription"
    ):
        raise HTTPException(
            status_code=400, detail="Invalid transaction for cancellation"
        )

    subscription_amount = transaction["amount"]
    fund_id = transaction["fund_id"]

    # Add the amount back to the client's balance
    new_balance = client["balance"] + subscription_amount
    clients_table.update_item(
        Key={"id": cancellation.client_id},
        UpdateExpression="SET balance = :new_balance",
        ExpressionAttributeValues={":new_balance": new_balance},
    )

    # Create a new transaction for the cancellation
    transaction_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()
    new_transaction = {
        "id": transaction_id,
        "type": "Cancellation",
        "date": created_at,
        "amount": subscription_amount,
        "client_id": cancellation.client_id,
        "fund_id": fund_id,
        "notification": cancellation.notification,
        "created_at": created_at,
    }
    transactions_table.put_item(Item=new_transaction)

    return new_transaction
