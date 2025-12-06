import os
from dotenv import load_dotenv

load_dotenv()

def _env_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_MODE = os.getenv("STRIPE_MODE", "mock").lower()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "payment_api")
USE_MOCK_DB = _env_bool(os.getenv("USE_MOCK_DB"), default=not bool(MONGODB_URI))

def is_mock_mode() -> bool:
    """
    Returns True if Stripe should run in mock mode.
    Mock mode is enabled when:
    - STRIPE_MODE is not set to "live", OR
    - STRIPE_SECRET_KEY is not provided
    """
    return STRIPE_MODE != "live" or not STRIPE_SECRET_KEY
