
import json
import os
import boto3


def send_to_stream(event):
    stream_name = os.getenv("KINESIS_STREAM_NAME")
    if not stream_name:
        print("Kinesis not configured; skipping stream delivery.")
        return None

    kinesis = boto3.client(
        "kinesis",
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
    )

    response = kinesis.put_record(
        StreamName=stream_name,
        Data=json.dumps(event).encode("utf-8"),
        PartitionKey=str(event["customer_id"]),
    )
    print("Sent to Kinesis:", response["SequenceNumber"])
    return response
