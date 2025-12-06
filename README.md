# 💳 Payment API Mock - Stripe Sandbox Integration

A production-ready, mock FinTech payment service built with FastAPI that seamlessly integrates with Stripe's sandbox environment. This API provides a complete payment processing solution with support for payment intents, webhook signature verification, and refunds, all with comprehensive validation and a full test suite.

## ✨ Features

- **🔄 Payment Intent Creation** - Create and manage Stripe payment intents with automatic database persistence
- **💰 Refund Processing** - Process refunds with multiple reason codes (duplicate, fraudulent, customer-requested)
- **🔔 Webhook Integration** - Secure webhook endpoint with Stripe signature verification
- **🎭 Dual Mode Operation** - Seamlessly switch between mock and live Stripe modes
- **💾 Flexible Database** - MongoDB Atlas integration with automatic fallback to in-memory mock database
- **✅ Strict Validation** - Pydantic-based request validation with comprehensive error handling
- **🧪 Complete Test Suite** - Full test coverage with pytest
- **📝 Auto-Generated Docs** - Interactive API documentation via FastAPI's Swagger UI
- **🔒 Production Ready** - Thread-safe operations, proper error handling, and logging

## 🚀 Tech Stack

- **Framework**: FastAPI 0.123.2
- **Language**: Python 3.14+
- **Payment Gateway**: Stripe API 14.0.1
- **Database**: MongoDB (via PyMongo) with mongomock for testing
- **Validation**: Pydantic 2.12.5
- **Testing**: pytest 9.0.1 with pytest-asyncio
- **Server**: Uvicorn ASGI server

## 📋 Prerequisites

- Python 3.14 or higher
- pip (Python package manager)
- MongoDB Atlas account (optional - mock mode works without it)
- Stripe account with API keys (optional - mock mode works without it)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Payment-API-Mock
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx          # Optional in mock mode
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx        # Required for live webhook verification
STRIPE_MODE=mock                                  # Options: "mock" or "live" (default: "mock")

# MongoDB Configuration
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster-url.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=payment_api                       # Default: "payment_api"
USE_MOCK_DB=true                                  # Use in-memory mock DB (auto-enabled if URI missing)
```

> **Note**: In mock mode, you can run the API without Stripe keys or MongoDB. The system automatically uses in-memory mocks for testing.

## 🎯 Quick Start

### Run the Server

**Windows:**
```bash
run.bat
```

**Or manually:**
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Test the API

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest app/tests/test_payment.py
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Create Payment Intent

Create a new payment intent for processing payments.

**Endpoint:** `POST /payments/create-intent`

**Request Body:**
```json
{
  "amount": 1000,
  "currency": "inr",
  "payer_name": "John Doe"
}
```

**Request Schema:**
- `amount` (integer, required): Payment amount in smallest currency unit (e.g., paise for INR)
- `currency` (string, optional): Currency code (default: "inr")
- `payer_name` (string, required): Name of the payer (min length: 1)

**Response:**
```json
{
  "client_secret": "pi_1234567890abcdef_secret_xyz"
}
```

**Status Codes:**
- `200` - Payment intent created successfully
- `400` - Invalid request or Stripe error
- `500` - Server error
- `503` - Database connection error

---

#### 2. Process Refund

Refund a payment using the payment intent ID.

**Endpoint:** `POST /refund`

**Request Body:**
```json
{
  "payment_intent_id": "pi_1234567890abcdef",
  "reason": "requested_by_customer"
}
```

**Request Schema:**
- `payment_intent_id` (string, required): Stripe payment intent ID (must start with "pi_", min length: 10)
- `reason` (string, optional): Refund reason - one of:
  - `"duplicate"` - Duplicate payment
  - `"fraudulent"` - Fraudulent transaction
  - `"requested_by_customer"` - Customer requested refund (default)

**Response:**
```json
{
  "refund_id": "re_1234567890abcdef",
  "status": "succeeded",
  "payment_intent_id": "pi_1234567890abcdef"
}
```

**Status Codes:**
- `200` - Refund processed successfully
- `400` - Invalid request or validation error
- `404` - Payment intent not found
- `500` - Server error
- `503` - Database connection error

---

#### 3. Webhook Endpoint

Receive and verify Stripe webhook events.

**Endpoint:** `POST /webhook`

**Headers:**
- `stripe-signature` (required in live mode): Stripe webhook signature

**Request Body:**
Raw webhook payload from Stripe

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200` - Webhook processed successfully
- `400` - Invalid signature or payload
- `500` - Server error

> **Note**: In mock mode, signature verification is skipped for easier testing.

---

#### 4. Health Check

Check if the API is running.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Payment API Mock Running"
}
```

## 🏗️ Project Structure

```
Payment-API-Mock/
├── app/
│   ├── api/                    # API route handlers
│   │   ├── payments.py         # Payment intent endpoints
│   │   ├── refund.py           # Refund endpoints
│   │   └── webhook.py          # Webhook endpoints
│   ├── schemas/                # Pydantic validation schemas
│   │   ├── payments.py         # Payment request schemas
│   │   └── refund.py           # Refund request schemas
│   ├── services/               # Business logic services
│   │   ├── stripe_service.py   # Stripe API integration
│   │   └── mongo_service.py   # MongoDB operations
│   ├── tests/                  # Test suite
│   │   ├── test_payment.py    # Payment intent tests
│   │   ├── test_refund.py     # Refund tests
│   │   └── test_webhooks.py   # Webhook tests
│   ├── utils/                  # Utility modules
│   │   └── logger.py           # Logging configuration
│   ├── config.py               # Environment configuration
│   └── main.py                 # FastAPI application entry point
├── .env                        # Environment variables (create from .env.example)
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows startup script
└── README.md                   # This file
```

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_payment.py
pytest app/tests/test_refund.py
pytest app/tests/test_webhooks.py
```

**Test Coverage:**
- ✅ Payment intent creation
- ✅ Refund processing
- ✅ Webhook signature verification
- ✅ Input validation
- ✅ Error handling
- ✅ Mock mode functionality

## 🔧 Configuration

### Mock Mode vs Live Mode

The API operates in two modes:

**Mock Mode (Default):**
- No Stripe API keys required
- Uses in-memory mock objects
- Perfect for development and testing
- Webhook signature verification skipped

**Live Mode:**
- Requires valid Stripe API keys
- Connects to real Stripe API
- Full webhook signature verification
- Set `STRIPE_MODE=live` and provide `STRIPE_SECRET_KEY`

### Database Configuration

**MongoDB Atlas (Production):**
1. Create a MongoDB Atlas cluster (free tier available)
2. Create a database user with read/write permissions
3. Whitelist your IP address in Network Access
4. Copy the connection string to `MONGODB_URI`
5. Set `USE_MOCK_DB=false`

**Mock Database (Development):**
- Automatically enabled when `MONGODB_URI` is empty or `USE_MOCK_DB=true`
- Uses `mongomock` for in-memory database
- No external dependencies required
- Perfect for testing

## 🔒 Security Features

- ✅ Environment variable-based configuration (no hardcoded secrets)
- ✅ Webhook signature verification (live mode)
- ✅ Input validation with Pydantic
- ✅ Thread-safe API key handling
- ✅ Comprehensive error handling
- ✅ `.gitignore` configured to exclude sensitive files

## 📝 API Validation

### Payment Intent Validation
- Amount must be greater than 0
- Currency must be a valid string
- Payer name must be at least 1 character

### Refund Validation
- Payment intent ID must start with `"pi_"`
- Payment intent ID minimum length: 10 characters
- Refund reason must be one of: `duplicate`, `fraudulent`, `requested_by_customer`

## 🐛 Error Handling

The API provides detailed error responses:

- **400 Bad Request**: Invalid input or Stripe API error
- **404 Not Found**: Payment intent not found
- **500 Internal Server Error**: Unexpected server error
- **503 Service Unavailable**: Database connection error

All errors include descriptive messages to help with debugging.

## 🚀 Deployment

### Local Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

1. Set environment variables on your hosting platform
2. Ensure MongoDB Atlas connection is configured
3. Use a production ASGI server like Gunicorn with Uvicorn workers:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 Features in Detail

### Payment Intent Flow
1. Client sends payment request with amount, currency, and payer name
2. API creates Stripe payment intent (mock or live)
3. Payment intent is stored in database
4. Client secret is returned for frontend integration

### Refund Flow
1. Client sends refund request with payment intent ID and reason
2. API retrieves payment intent from Stripe
3. Extracts charge ID from payment intent
4. Creates refund with specified reason
5. Returns refund details

### Webhook Flow
1. Stripe sends webhook event
2. API verifies webhook signature (live mode)
3. Processes event payload
4. Returns success status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## 🎯 Roadmap

- [ ] Add payment method management
- [ ] Implement subscription support
- [ ] Add webhook event processing logic
- [ ] Enhanced logging and monitoring
- [ ] Rate limiting
- [ ] API versioning

---

**Built with ❤️ using FastAPI and Stripe**
