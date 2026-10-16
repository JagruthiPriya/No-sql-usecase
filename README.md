# Event-Driven Data Ingestion System Using AWS

## 1. Project Overview

This project implements an event-driven data ingestion pipeline using Python and AWS services to process order events reliably. It demonstrates asynchronous communication, message queuing, NoSQL data storage, and optional real-time streaming.

The system generates order events, publishes them through Amazon SNS, buffers messages in Amazon SQS, and stores processed event records in Amazon DynamoDB. Amazon Kinesis Data Streams can be used as an additional streaming destination.

## 2. Objectives

- Build an event-driven data ingestion architecture.
- Decouple event producers from downstream consumers.
- Process events asynchronously using managed AWS services.
- Store structured event records in a NoSQL database.
- Handle duplicate messages and processing failures.
- Apply testing, logging, and secure configuration practices.

## 3. Architecture

```text
                  Python Event Producer
                           |
               +-----------+-----------+
               |                       |
               v                       v
        Amazon SNS Topic       Amazon Kinesis
               |                (Optional)
               v
           Amazon SQS
               |
               v
        Python SQS Consumer
               |
               v
        Amazon DynamoDB
```

### Data Flow

1. **Event Producer:** Generates order events containing a unique event ID, customer ID, event type, amount, and UTC timestamp.
2. **Amazon SNS:** Publishes events to subscribed endpoints.
3. **Amazon SQS:** Buffers events for asynchronous consumption.
4. **SQS Consumer:** Retrieves messages, validates the event structure, and processes each event.
5. **Amazon DynamoDB:** Stores processed event records using `event_id` as the partition key.
6. **Amazon Kinesis Data Streams (Optional):** Receives events for downstream streaming applications.

## 4. AWS Services Used

| Service | Responsibility |
|---|---|
| Amazon SNS | Event publishing and message fan-out |
| Amazon SQS | Message buffering and asynchronous processing |
| Amazon DynamoDB | NoSQL storage for processed events |
| Amazon Kinesis Data Streams | Optional streaming ingestion |
| AWS IAM | Access control and permissions |
| Amazon CloudWatch | Optional logs, metrics, and monitoring |

## 5. Project Structure

```text
No-sql-usecase/
├── src/
│   ├── __init__.py
│   ├── producer.py
│   ├── sns_publisher.py
│   ├── sqs_consumer.py
│   ├── dynamodb_writer.py
│   ├── stream_processor.py
│   └── main.py
├── tests/
│   └── test_pipeline.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── architecture.md
```

## 6. Technology Stack

- Python 3.14
- Boto3 — AWS SDK for Python
- Amazon SNS
- Amazon SQS
- Amazon DynamoDB
- Amazon Kinesis Data Streams (optional)
- pytest
- Visual Studio Code
- Git and GitHub

## 7. Implementation Details

### Event Generation
The producer generates uniquely identified order events with timestamps in UTC and validates input values.

### Event Publishing
The SNS publisher sends JSON-serialized events to the configured SNS topic.

### Message Consumption
The SQS consumer retrieves messages, supports SNS-wrapped notifications, validates required fields, and removes messages only after successful processing or confirmed duplicate detection.

### NoSQL Persistence
The DynamoDB writer stores event records using a unique `event_id` partition key and conditional writes to prevent duplicate overwrites.

### Streaming Integration
The optional Kinesis component sends event records to a configured data stream using the customer ID as the partition key.

### Testing
Unit tests validate event creation, rejection of negative amounts, and handling of invalid message structures.

## 8. Prerequisites

- Python installed on the development machine.
- An AWS account with access to the required services.
- AWS CLI configured with appropriate credentials.
- An SNS topic, SQS queue, and DynamoDB table.
- An SNS subscription connecting the topic to the queue.
- An optional Kinesis data stream.
- IAM permissions appropriate for the configured resources.

## 9. Setup and Execution

### Step 1: Clone the Repository

```bash
git clone https://github.com/JagruthiPriya/No-sql-usecase.git
cd No-sql-usecase
```

### Step 2: Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure AWS Credentials

Configure credentials through an approved AWS CLI profile or another supported credentials provider.

```powershell
aws configure
aws sts get-caller-identity
```

Never commit AWS access keys, secret keys, session tokens, or your local `.env` file to GitHub.

### Step 5: Configure Environment Variables

Create a local `.env` file using `.env.example` as a template.

```dotenv
AWS_REGION=ap-south-1
SNS_TOPIC_ARN=your-sns-topic-arn
SQS_QUEUE_URL=your-sqs-queue-url
DYNAMODB_TABLE_NAME=EventRecords
KINESIS_STREAM_NAME=
```

Replace the example SNS ARN and SQS URL with your actual AWS resource identifiers. Leave the Kinesis stream name empty if streaming is not configured.

### Step 6: Run Unit Tests

```powershell
python -m pytest -v
```

The initial local test suite contains three tests covering event creation, negative amount validation, and invalid message rejection.

### Step 7: Run the Application

```powershell
python -m src.main
```

When AWS resources, credentials, environment variables, and permissions are correctly configured, the application attempts to publish an event, optionally send it to Kinesis, and poll SQS for messages.

## 10. Reliability and Error Handling

- SQS provides message buffering and asynchronous consumption.
- Failed message processing leaves the message available for retry.
- DynamoDB conditional writes prevent overwriting an existing record with the same event ID.
- Unique event IDs help identify individual events.
- Invalid messages are rejected by validation.
- A dead-letter queue should be configured to isolate messages that repeatedly fail.

**Delivery semantics:** This implementation does not provide end-to-end exactly-once processing. A message may be delivered more than once. Conditional DynamoDB writes help protect against duplicate records, but production systems should also consider partial failures, retry policies, visibility timeouts, and idempotent downstream operations.

## 11. Security and Monitoring

- Use least-privilege IAM policies.
- Restrict access to SNS topics, SQS queues, DynamoDB tables, and Kinesis streams.
- Keep credentials out of source code and version control.
- Use CloudWatch metrics and logs to monitor failures, queue depth, and processing activity.
- Configure appropriate message retention, retry policies, and alarms.

## 12. Validation and Results

The local Python unit tests passed successfully during development.

The event producer was also executed locally and generated an order event with an event ID, customer ID, amount, event type, and UTC timestamp.

Live AWS integration should be validated by confirming that:
- The SNS topic accepts the published event.
- The subscribed SQS queue receives the notification.
- The consumer processes the message.
- The event record appears in DynamoDB.
- The optional Kinesis stream receives the event when configured.

Record actual AWS test results and screenshots here after verifying the end-to-end flow.

## 13. Future Enhancements

- Implement a continuous SQS worker or AWS Lambda consumer.
- Configure an SQS dead-letter queue and redrive policy.
- Add schema validation and stronger event contracts.
- Add automated infrastructure provisioning using AWS CloudFormation or AWS CDK.
- Implement Kinesis consumers and downstream analytics.
- Add CloudWatch dashboards, alarms, and operational metrics.
- Introduce integration tests and load testing.

## 14. Conclusion

This project demonstrates how managed AWS messaging and database services can be combined to build a loosely coupled event-driven ingestion pipeline. It covers event generation, asynchronous message delivery, validation, NoSQL persistence, duplicate protection, and optional streaming integration.

The architecture provides a foundation for scalable data processing systems and can be extended with managed consumers, infrastructure as code, monitoring, and production-grade reliability controls.

## Author

**Jagruthi Priya**

GitHub Repository: https://github.com/JagruthiPriya/No-sql-usecase
