
# Architecture and Design

## Data Flow
1. Producer generates an order event.
2. SNS publishes the event to subscribers.
3. SQS buffers the event for reliable consumption.
4. Consumer validates the message.
5. DynamoDB stores the event using event_id as the partition key.
6. Optional Kinesis delivery supports streaming workloads.

## Reliability
- SQS buffers messages during processing delays.
- Failed messages are retained for retry.
- DynamoDB conditional writes prevent duplicate overwrites.
- A dead-letter queue should be configured for repeatedly failing messages.

## Scalability
- SQS decouples event production from processing.
- Consumers can be scaled horizontally.
- DynamoDB capacity and Kinesis throughput must be monitored and configured for workload requirements.

## Security
- Use IAM roles or named AWS CLI profiles.
- Do not commit credentials or .env files.
- Restrict access to queues, topics, tables and streams.
