
import pytest
from src.producer import create_event
from src.sqs_consumer import process_message


def test_event_has_required_fields():
    event = create_event(101, 2500)
    assert event["event_type"] == "ORDER_CREATED"
    assert event["customer_id"] == "101"
    assert event["amount"] == 2500.0
    assert event["event_id"]
    assert event["timestamp"]


def test_negative_amount_is_rejected():
    with pytest.raises(ValueError):
        create_event(101, -100)


def test_invalid_message_is_rejected():
    with pytest.raises(ValueError):
        process_message('{"wrong_field": "value"}')
