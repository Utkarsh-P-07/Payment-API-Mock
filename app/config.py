import os
from dotenv import load_dotenv

load_dotenv()

def _env_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    # Handle empty string as False
    if not value:
        return False
    return value.lower() in {"1", "true", "yes", "on"}

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
# Normalize STRIPE_MODE: empty string or invalid values default to "mock"
_stripe_mode_raw = os.getenv("STRIPE_MODE", "mock").lower().strip()
STRIPE_MODE = _stripe_mode_raw if _stripe_mode_raw else "mock"

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
