# Event-Driven Data Ingestion System

## Overview
A Python-based event-driven data ingestion pipeline using Amazon SNS, Amazon SQS, Amazon DynamoDB, and optional Amazon Kinesis Data Streams.

## Architecture
Event Producer → SNS Topic → SQS Queue → Message Consumer → DynamoDB

Optional streaming path: Event Producer → Kinesis Data Streams.

## Features
- Event generation with unique IDs and UTC timestamps
- SNS event publishing
- SQS message consumption and retry-friendly error handling
- DynamoDB persistence with duplicate protection
- Optional Kinesis event streaming
- Python unit tests using pytest
- Configuration through environment variables

## Technologies
Python, Boto3, Amazon SNS, Amazon SQS, Amazon DynamoDB, Amazon Kinesis Data Streams, pytest.

## Execution
1. Configure AWS credentials using the AWS CLI.
2. Create the required AWS resources and configure the SNS-to-SQS subscription.
3. Fill in `.env` with the resource identifiers.
4. Install dependencies using `python -m pip install -r requirements.txt`.
5. Run the tests using `python -m pytest -v`.
6. Run the pipeline using `python -m src.main`.

## Reliability
The consumer deletes messages only after successful processing or confirmed duplicate detection. Other failures leave messages available for retry. Production deployment should include a dead-letter queue, monitoring, least-privilege IAM permissions, and an appropriate retention policy.