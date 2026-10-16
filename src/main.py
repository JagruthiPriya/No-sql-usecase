
from dotenv import load_dotenv
from src.producer import create_event
from src.sns_publisher import publish_event
from src.sqs_consumer import consume_messages
from src.stream_processor import send_to_stream


def main():
    load_dotenv()

    event = create_event(customer_id=101, amount=2500.00)
    print("Created event:", event)

    publish_event(event)
    send_to_stream(event)

    print("Checking SQS for messages...")
    consume_messages(max_messages=10, wait_seconds=10)


if __name__ == "__main__":
    main()
