# ChadPay System Architecture

## Overview

ChadPay is a lightweight, USSD-based mobile money payment system for transport operators and vendors in N'Djamena, Chad. It provides a trusted UX layer on top of existing mobile money infrastructure without requiring direct API integration or payment licenses.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CHADPAY SYSTEM                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Customer   │    │   Merchant   │    │    Admin     │                  │
│  │  (No Login)  │    │ (Phone+PIN)  │    │(User/Pass)   │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         │ Scan QR           │ Login             │ Login                     │
│         │ Select Amount     │ View Dashboard    │ Manage Merchants          │
│         │ Dial USSD         │ Confirm Payments  │ Generate QR Codes         │
│         │ Confirm Payment   │ View History      │ Export Reports            │
│         │                   │                   │                           │
│         └───────────────────┴───────────────────┘                           │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        FastAPI Application                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │  │   Public    │  │  Merchant   │  │    Admin    │  │   Health   │  │   │
│  │  │   Router    │  │   Router    │  │   Router    │  │   Check    │  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └────────────┘  │   │
│  │         └─────────────────┴─────────────────┘                        │   │
│  │                              │                                        │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │                     Business Logic Layer                        │  │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │  │   │
│  │  │  │   Auth   │  │    QR    │  │ Payment  │  │    Audit     │   │  │   │
│  │  │  │  Service │  │  Service │  │  Service │  │    Logger    │   │  │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │                              │                                        │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │                      Data Access Layer                          │  │   │
│  │  │                    (SQLModel/SQLAlchemy)                        │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         SQLite Database                              │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ merchants│ │merchant_ │ │ payment_ │ │transactions│ │audit_logs│  │   │
│  │  │          │ │  users   │ │ intents  │ │          │ │          │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

External Systems:
┌─────────────────┐    ┌─────────────────┐
│  Airtel Money   │    │   Moov Cash     │
│  (USSD Dialer)  │    │  (USSD Dialer)  │
└─────────────────┘    └─────────────────┘
```

## Request/Response Flow

### Customer Payment Flow

```
1. Customer scans QR code
   └─> GET /m/{merchant_code}?t={signed_token}
       └─> Verify QR signature
       └─> Render payment page

2. Customer selects amount and wallet
   └─> POST /m/{merchant_code}/initiate?amount=X&wallet_type=Y
       └─> Create payment intent
       └─> Generate USSD string
       └─> Render payment initiated page

3. Customer dials USSD and pays
   └─> (External: Airtel Money / Moov Cash)

4. Customer confirms payment
   └─> POST /payment/{id}/confirm
       └─> Update payment intent status
       └─> Log confirmation
       └─> Render waiting page

5. Merchant confirms receipt
   └─> POST /merchant/payment/{id}/accept (HTMX)
       └─> Create transaction record
       └─> Update payment intent
       └─> Log acceptance
```

### Merchant Login Flow

```
1. Merchant visits login page
   └─> GET /merchant/login

2. Merchant submits credentials
   └─> POST /merchant/login (phone, pin)
       └─> Verify credentials
       └─> Create JWT token
       └─> Set HTTP-only cookie
       └─> Redirect to dashboard

3. Merchant accesses dashboard
   └─> GET /merchant/dashboard
       └─> Verify JWT from cookie
       └─> Load pending payments
       └─> Load today's summary
       └─> Render dashboard
```

## Security Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                      PUBLIC ZONE                             │
│  - QR code scanning (signed tokens)                          │
│  - Payment pages (no auth required)                          │
│  - Rate limiting on confirmations                            │
│  - No PII stored for customers                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MERCHANT ZONE                             │
│  - Phone + PIN authentication                                │
│  - JWT tokens (HTTP-only cookies)                            │
│  - Can only access own data                                  │
│  - Can confirm/reject payments                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      ADMIN ZONE                              │
│  - Username + password authentication                        │
│  - Shorter session expiry                                    │
│  - Full system access                                        │
│  - Audit logging of all actions                              │
└─────────────────────────────────────────────────────────────┘
```

## Key Security Features

### 1. QR Code Security
- **Signed Tokens**: QR codes contain HMAC-signed tokens
- **Tamper Detection**: Any modification invalidates the signature
- **Expiration**: Tokens expire after 1 year

### 2. Payment Intent Security
- **Idempotency Keys**: Prevent duplicate payments
- **Rate Limiting**: 30-second cooldown between confirmations
- **IP Tracking**: For fraud detection
- **Expiration**: Payment intents expire after 15 minutes

### 3. Data Privacy
- **Customer Phone Hashing**: SHA256 with secret salt
- **Phone Masking**: Partial display (e.g., +235 66XX XXXX)
- **No Full Numbers**: Customer phone numbers never stored in plain text

### 4. Authentication
- **bcrypt**: For password/PIN hashing
- **JWT**: Stateless session tokens
- **HTTP-only Cookies**: XSS protection
- **Session Expiry**: 8 hours (merchant), 1 hour (admin)

## PostgreSQL Migration Path

### Current (SQLite)
- Single file database
- No connection pooling needed
- `check_same_thread=False` for multi-threading

### Production (PostgreSQL)
```python
# Change in config.py
DATABASE_URL = "postgresql://user:password@localhost/chadpay"

# Remove from engine creation
connect_args = {}  # Remove check_same_thread

# Add connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    echo=settings.debug
)
```

### Required Indexes (PostgreSQL)
```sql
-- Performance indexes
CREATE INDEX idx_merchants_code ON merchants(code);
CREATE INDEX idx_merchants_phone ON merchants(phone);
CREATE INDEX idx_payment_intents_status ON payment_intents(status);
CREATE INDEX idx_payment_intents_merchant ON payment_intents(merchant_id);
CREATE INDEX idx_transactions_merchant ON transactions(merchant_id);
CREATE INDEX idx_transactions_created ON transactions(created_at);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
```

## Scalability Considerations

### Current (POC)
- Single server
- SQLite database
- In-memory rate limiting
- File-based QR storage

### Production Scaling
1. **Database**: PostgreSQL with read replicas
2. **Rate Limiting**: Redis
3. **QR Storage**: S3/CloudFront
4. **Session Store**: Redis
5. **Load Balancer**: Multiple app servers
6. **CDN**: Static assets + QR codes
