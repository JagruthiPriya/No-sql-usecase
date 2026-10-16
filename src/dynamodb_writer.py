
import os
import boto3


def save_event(event):
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("DYNAMODB_TABLE_NAME is not configured")

    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
    )
    table = dynamodb.Table(table_name)

    table.put_item(
        Item=event,
        ConditionExpression="attribute_not_exists(event_id)",
    )
    print("Saved event:", event["event_id"])
