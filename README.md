project:
  name: Payment API Mock
  framework: FastAPI
  language: Python 3.14
  purpose: >
    A mock FinTech payment service integrating Stripe Sandbox.
    Supports PaymentIntents, Webhook signature verification,
    and Refunds with strict validation + full test suite.

environment:
  variables:
    STRIPE_SECRET_KEY: "sk_test_xxxxxxxxxxxxx" # optional in mock mode
    STRIPE_WEBHOOK_SECRET: "whsec_xxxxxxxxxxxxx"
    STRIPE_MODE: one_of [mock, live] (default mock)
    MONGODB_URI: "mongodb+srv://<user>:<pass>@cluster-url.mongodb.net/?retryWrites=true&w=majority"
    MONGODB_DB_NAME: "payment_api"
    USE_MOCK_DB: "true" to use in-memory mongomock when no Atlas connection (default auto when URI missing)
  files:
    - .env (copy from .env.example and override as needed)

commands:
  setup:
    - python -m venv venv
    - venv\Scripts\activate
    - pip install -r requirements.txt
  run:
    - uvicorn app.main:app --reload
  tests:
    - pytest

structure:
  root:
    - app/
    - ├── api/
    - ├── schemas/
    - ├── services/
    - ├── tests/
    - ├── utils/
    - .env.example
    - requirements.txt
    - README.md
    - run.bat
    - .gitignore

database:
  engine: MongoDB Atlas (pymongo)
  collections:
    - payment_intents: stores amount, currency, mode, status, client_secret
  setup:
    - Create a MongoDB Atlas cluster (free tier works).
    - Add a database user with read/write access.
    - Whitelist your public IP in Atlas network access.
    - Grab the connection string (mongodb+srv://...) and set MONGODB_URI.
    - Optionally override MONGODB_DB_NAME (defaults to payment_api).
    - Set USE_MOCK_DB=false to force real Atlas even if URI missing.
  local_dev:
    - When USE_MOCK_DB=true or MONGODB_URI empty, an in-memory mongomock database is used automatically so tests do not need a live cluster.

endpoints:
  - path: /payments/create-intent
    method: POST
    request:
      amount: integer
      currency: string
    response:
      client_secret: string

  - path: /refund
    method: POST
    request:
      payment_intent_id: string
      reason: one_of [duplicate, fraudulent, requested_by_customer]
    response:
      refund_id: string
      status: string

  - path: /webhook
    method: POST
    description: Validates Stripe signature and handles event payloads.

testing:
  framework: pytest
  mock_library: unittest.mock
  tests:
    - test_payment_intent_creation
    - test_webhook_invalid_signature
    - test_refund_missing_field
  expected_output: "3 passed, 0 failed"

stripe:
  operations:
    payment_intent:
      create:
        expanded_fields: []
    refund:
      steps:
        - Retrieve PaymentIntent with expand=["charges"]
        - Extract charge_id
        - Create refund with reason
  refund_reasons:
    - duplicate
    - fraudulent
    - requested_by_customer

quality:
  non_functional:
    - unit tests >= 6
    - proper logging
    - clean architecture
    - .gitignore with venv + env security
    - strict validation using Pydantic
    - no secrets committed to git

milestones:
  week_1: Project setup, environment, folder structure
  week_2: PaymentIntent API + validation
  week_3: Webhook + signature verification
  week_4: Refunds + deployment + tests + README

deliverables:
  - Working FastAPI service
  - Mocked Stripe integration
  - Automated tests
  - README.md
  - Deployment instructions
  - Demo video (2–3 mins)
