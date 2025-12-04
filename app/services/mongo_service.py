from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from pymongo import MongoClient

try:
    import mongomock
except ImportError:  # pragma: no cover - optional dependency in live mode
    mongomock = None

from app.config import MONGODB_DB_NAME, MONGODB_URI, USE_MOCK_DB
from app.utils.logger import logger


class MongoService:
    """Simple helper around MongoDB to persist API data."""

    _client: MongoClient | None = None

    @classmethod
    def _build_client(cls) -> MongoClient:
        if USE_MOCK_DB:
            if not mongomock:
                raise RuntimeError(
                    "mongomock is required when USE_MOCK_DB is enabled but is not installed."
                )
            logger.info("Using in-memory MongoDB via mongomock.")
            return mongomock.MongoClient()

        if not MONGODB_URI:
            raise RuntimeError(
                "MONGODB_URI must be configured when USE_MOCK_DB is disabled."
            )

        logger.info("Connecting to MongoDB cluster.")
        return MongoClient(MONGODB_URI)

    @classmethod
    def get_client(cls) -> MongoClient:
        if cls._client is None:
            cls._client = cls._build_client()
        return cls._client

    @classmethod
    def get_db(cls):
        return cls.get_client()[MONGODB_DB_NAME]

    @classmethod
    def payment_intents_collection(cls):
        return cls.get_db()["payment_intents"]

    @classmethod
    def record_payment_intent(cls, data: Dict[str, Any]) -> str:
        document = {
            "payment_intent_id": data.get("payment_intent_id"),
            "amount": data.get("amount"),
            "currency": data.get("currency"),
            "status": data.get("status", "created"),
            "mode": data.get("mode", "mock"),
            "client_secret": data.get("client_secret"),
            "metadata": data.get("metadata", {}),
            "created_at": data.get("created_at", datetime.now(timezone.utc)),
        }
        result = cls.payment_intents_collection().insert_one(document)
        return str(result.inserted_id)

    @classmethod
    def drop_mock_database(cls):
        """Utility for tests – clears the in-memory DB when mocking."""
        if not USE_MOCK_DB or cls._client is None:
            return
        cls._client.drop_database(MONGODB_DB_NAME)
        cls._client = None

