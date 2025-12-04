import pytest
from unittest.mock import MagicMock, patch

from app.services.mongo_service import MongoService


@pytest.fixture(autouse=True)
def reset_mongo():
    MongoService.drop_mock_database()
    yield
    MongoService.drop_mock_database()


@pytest.fixture
def mock_stripe_payment_intent_create():
    with patch("app.services.stripe_service.stripe.PaymentIntent.create") as mock:
        mock.return_value = MagicMock(client_secret="test_secret")
        yield mock
