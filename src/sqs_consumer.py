
import json
import os
import boto3
from botocore.exceptions import ClientError
from src.dynamodb_writer import save_event


def process_message(body):
    payload = json.loads(body)

    # SNS-to-SQS subscriptions normally wrap the event in "Message".
    if isinstance(payload, dict) and "Message" in payload:
        payload = json.loads(payload["Message"])

    required = {"event_id", "event_type", "customer_id", "amount", "timestamp"}
    if not isinstance(payload, dict) or not required.issubset(payload):
        raise ValueError("Message is missing required event fields")

    try:
        save_event(payload)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print("Duplicate event skipped:", payload["event_id"])
        else:
            raise

    return payload


def consume_messages(max_messages=5, wait_seconds=10):
    queue_url = os.getenv("SQS_QUEUE_URL")
    if not queue_url:
        raise ValueError("SQS_QUEUE_URL is not configured")

    sqs = boto3.client(
        "sqs", region_name=os.getenv("AWS_REGION", "ap-south-1")
    )

    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=min(max_messages, 10),
        WaitTimeSeconds=min(wait_seconds, 20),
    )

    messages = response.get("Messages", [])

    for message in messages:
        try:
            process_message(message["Body"])
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message["ReceiptHandle"],
            )
            print("Message processed and removed from queue.")
        except Exception as exc:
            # Do not delete failed messages; SQS can redeliver them.
            print("Processing failed; message retained for retry:", exc)

    return len(messages)
