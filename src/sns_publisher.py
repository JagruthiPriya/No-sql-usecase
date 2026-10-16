
import json
import os
import boto3


def publish_event(event):
    topic_arn = os.getenv("SNS_TOPIC_ARN")
    if not topic_arn:
        raise ValueError("SNS_TOPIC_ARN is not configured")

    sns = boto3.client(
        "sns", region_name=os.getenv("AWS_REGION", "ap-south-1")
    )

    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(event),
        Subject="Order Event",
        MessageAttributes={
            "event_type": {
                "DataType": "String",
                "StringValue": event["event_type"],
            }
        },
    )
    print("Published SNS message:", response["MessageId"])
    return response
