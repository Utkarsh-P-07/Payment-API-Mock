import os
from dotenv import load_dotenv

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_MODE = os.getenv("STRIPE_MODE", "mock").lower()


def is_mock_mode() -> bool:
    """Return True when Stripe calls should be mocked."""
    return STRIPE_MODE != "live" or not STRIPE_SECRET_KEY
