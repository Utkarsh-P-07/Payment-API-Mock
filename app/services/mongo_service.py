from pymongo import MongoClient
from app.config import MONGODB_URI, MONGODB_DB_NAME, USE_MOCK_DB

class MongoService:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            if USE_MOCK_DB or not MONGODB_URI:
                # Use mongomock for in-memory database
                import mongomock
                cls._client = mongomock.MongoClient()
            else:
                # Use real MongoDB connection
                cls._client = MongoClient(MONGODB_URI)
        return cls._client

    @classmethod
    def get_db(cls):
        return cls.get_client()[MONGODB_DB_NAME]

    @classmethod
    def payment_intents_collection(cls):
        return cls.get_db()["payment_intents"]

    @classmethod
    def record_payment_intent(cls, data):
        return cls.payment_intents_collection().insert_one(data).inserted_id
