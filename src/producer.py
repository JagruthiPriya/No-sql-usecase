
import uuid
from datetime import datetime, timezone


def create_event(customer_id=101, amount=2500.00):
    if customer_id is None or amount < 0:
        raise ValueError("Invalid customer ID or amount")

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "ORDER_CREATED",
        "customer_id": str(customer_id),
        "amount": float(amount),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    print(create_event())
