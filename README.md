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
