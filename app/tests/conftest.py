import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_stripe_payment_intent_create():
    with patch("app.services.stripe_service.stripe.PaymentIntent.create") as mock:
        mock.return_value = MagicMock(client_secret="test_secret")
        yield mock
