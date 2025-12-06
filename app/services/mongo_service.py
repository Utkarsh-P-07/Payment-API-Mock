from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ConnectionFailure, ServerSelectionTimeoutError, PyMongoError
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
                try:
                    cls._client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
                    # Test the connection
                    cls._client.admin.command('ping')
                except (ConfigurationError, ConnectionFailure, ServerSelectionTimeoutError) as e:
                    raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")
                except PyMongoError as e:
                    raise ConnectionError(f"MongoDB error: {str(e)}")
        return cls._client

    @classmethod
    def get_db(cls):
        return cls.get_client()[MONGODB_DB_NAME]

    @classmethod
    def payment_intents_collection(cls):
        return cls.get_db()["payment_intents"]

    @classmethod
    def record_payment_intent(cls, data):
        """Record a payment intent to the database. Raises ConnectionError on database failures."""
        try:
            return cls.payment_intents_collection().insert_one(data).inserted_id
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            raise ConnectionError(f"Database connection error: {str(e)}")
        except PyMongoError as e:
            raise ConnectionError(f"Database error while recording payment intent: {str(e)}")

    @classmethod
    def get_payment_intent(cls, payment_intent_id):
        """Retrieve a payment intent by ID. Returns None if not found."""
        try:
            return cls.payment_intents_collection().find_one({"payment_intent_id": payment_intent_id})
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            raise ConnectionError(f"Database connection error: {str(e)}")
        except PyMongoError as e:
            raise ConnectionError(f"Database error while retrieving payment intent: {str(e)}")