# ChadPay API Documentation

## Base URL
```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

### Merchant Authentication
- **Method**: JWT in HTTP-only cookie (`merchant_token`)
- **Login**: POST `/merchant/login` (phone + PIN)
- **Logout**: GET `/merchant/logout`
- **Expiry**: 8 hours

### Admin Authentication
- **Method**: JWT in HTTP-only cookie (`admin_token`)
- **Login**: POST `/admin/login` (username + password)
- **Logout**: GET `/admin/logout`
- **Expiry**: 1 hour

---

## Public Endpoints (No Auth Required)

### 1. Home Page
```
GET /
```
**Response**: HTML - Landing page with info

---

### 2. Merchant Payment Page
```
GET /m/{merchant_code}?t={signed_token}
```
**Parameters**:
- `merchant_code` (path): Unique merchant code (e.g., "TAXI001")
- `t` (query): Signed QR token

**Response**: HTML - Payment form with amount and wallet selection

**Error Responses**:
- 400: Invalid QR token
- 404: Merchant not found or inactive

---

### 3. Initiate Payment
```
POST /m/{merchant_code}/initiate?amount={amount}&wallet_type={wallet_type}
```
**Parameters**:
- `merchant_code` (path): Merchant code
- `amount` (query): Payment amount in XAF (min: 50)
- `wallet_type` (query): `airtel_money` or `moov_cash`

**Response**: HTML - Payment initiated page with USSD dialer

**Process**:
1. Validates merchant exists and is active
2. Validates amount (preset for transport, custom for vendors)
3. Creates payment intent with idempotency key
4. Generates USSD string from template
5. Returns dialer page

---

### 4. Confirm Payment (Customer)
```
POST /payment/{payment_intent_id}/confirm?customer_phone={phone}
```
**Parameters**:
- `payment_intent_id` (path): Payment intent ID
- `customer_phone` (query, optional): Customer phone number

**Response**: HTML - Waiting for merchant confirmation page

**Rate Limiting**: 30 seconds between confirmations per IP

**Process**:
1. Validates payment intent exists and is in INITIATED state
2. Checks rate limit
3. Hashes customer phone (if provided)
4. Updates status to CUSTOMER_CONFIRMED
5. Logs confirmation

---

### 5. Check Payment Status (HTMX Polling)
```
GET /payment/{payment_intent_id}/status
```
**Parameters**:
- `payment_intent_id` (path): Payment intent ID

**Response**: JSON
```json
{
  "status": "customer_confirmed",
  "merchant_accepted": false,
  "merchant_rejected": false
}
```

---

## Merchant Endpoints (Auth Required)

### 1. Login Page
```
GET /merchant/login
```
**Response**: HTML - Login form

---

### 2. Login Submit
```
POST /merchant/login
```
**Body** (form-data):
- `phone`: Merchant phone number
- `pin`: 4-digit PIN

**Success**: Sets cookie, redirects to `/merchant/dashboard`
**Failure**: Returns login page with error

---

### 3. Dashboard
```
GET /merchant/dashboard
```
**Response**: HTML - Dashboard with:
- Pending confirmations
- Today's total
- Recent transactions

---

### 4. Accept Payment (HTMX)
```
POST /merchant/payment/{payment_intent_id}/accept
```
**Response**: HTML partial - Updated pending list

**Process**:
1. Verifies payment intent belongs to merchant
2. Updates status to MERCHANT_ACCEPTED
3. Creates transaction record
4. Logs acceptance

---

### 5. Reject Payment (HTMX)
```
POST /merchant/payment/{payment_intent_id}/reject
```
**Body** (form-data):
- `reason` (optional): Rejection reason

**Response**: HTML partial - Updated pending list

---

### 6. Transaction History
```
GET /merchant/transactions?page={page}
```
**Parameters**:
- `page` (query, optional): Page number (default: 1)

**Response**: HTML - Paginated transaction list

---

### 7. Profile
```
GET /merchant/profile
```
**Response**: HTML - Merchant profile with QR code

---

### 8. Logout
```
GET /merchant/logout
```
**Response**: Redirect to login page

---

## Admin Endpoints (Auth Required)

### 1. Login Page
```
GET /admin/login
```
**Response**: HTML - Admin login form

---

### 2. Login Submit
```
POST /admin/login
```
**Body** (form-data):
- `username`: Admin username
- `password`: Admin password

**Success**: Sets cookie, redirects to `/admin/dashboard`

---

### 3. Dashboard
```
GET /admin/dashboard
```
**Response**: HTML - Admin dashboard with:
- Merchant stats
- Today's volume
- Recent audit logs

---

### 4. List Merchants
```
GET /admin/merchants?page={page}&search={query}
```
**Parameters**:
- `page` (query, optional): Page number
- `search` (query, optional): Search by name/code/phone

**Response**: HTML - Paginated merchant list

---

### 5. Create Merchant Page
```
GET /admin/merchants/create
```
**Response**: HTML - Merchant creation form

---

### 6. Create Merchant
```
POST /admin/merchants/create
```
**Body** (form-data):
- `name`: Merchant name
- `code`: Unique code (max 20 chars)
- `phone`: Merchant phone
- `merchant_type`: `bus`, `moto_taxi`, `taxi`, or `vendor`
- `user_name`: Admin user name
- `user_phone`: Admin user phone
- `user_pin`: 4-digit PIN
- `default_amount` (optional): For vendors
- `description` (optional)
- `location` (optional)

**Response**: Redirect to merchant detail page

---

### 7. View Merchant
```
GET /admin/merchants/{merchant_id}
```
**Response**: HTML - Merchant details, QR code, users, transactions

---

### 8. Generate QR Code
```
POST /admin/merchants/{merchant_id}/generate-qr
```
**Body** (form-data):
- `base_url`: Base URL for QR (e.g., `https://chadpay.com`)

**Response**: HTML partial - QR code image

---

### 9. List Transactions
```
GET /admin/transactions?merchant_id={id}&status={status}&date_from={date}&date_to={date}&page={page}
```
**Parameters**:
- `merchant_id` (query, optional): Filter by merchant
- `status` (query, optional): Filter by status
- `date_from` (query, optional): Start date (YYYY-MM-DD)
- `date_to` (query, optional): End date (YYYY-MM-DD)
- `page` (query, optional): Page number

**Response**: HTML - Paginated transaction list with filters

---

### 10. Export Transactions
```
GET /admin/transactions/export?merchant_id={id}&date_from={date}&date_to={date}
```
**Parameters**: Same as list transactions

**Response**: CSV file download

**CSV Columns**:
- ID
- Date
- Merchant
- Merchant Code
- Amount (XAF)
- Wallet
- Status
- Customer Hash
- Disputed

---

### 11. View Audit Logs
```
GET /admin/audit-logs?page={page}&entity_type={type}
```
**Parameters**:
- `page` (query, optional): Page number
- `entity_type` (query, optional): Filter by entity type

**Response**: HTML - Paginated audit logs

---

### 12. Settings
```
GET /admin/settings
```
**Response**: HTML - View current settings (read-only in UI)

---

### 13. Logout
```
GET /admin/logout
```
**Response**: Redirect to login page

---

## System Endpoints

### Health Check
```
GET /health
```
**Response**: JSON
```json
{
  "status": "ok",
  "app": "ChadPay"
}
```

---

## Error Responses

### HTML Errors (Browser Routes)
- 404: `error.html` with message
- 500: `error.html` with generic message

### JSON Errors (API Routes)
```json
{
  "detail": "Error message"
}
```

### Common HTTP Status Codes
- `200 OK`: Success
- `302 Found`: Redirect
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Not authorized
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limited
- `500 Internal Server Error`: Server error

---

## HTMX Integration

Several endpoints return HTML partials for HTMX:

| Endpoint | HTMX Trigger | Target | Swap |
|----------|--------------|--------|------|
| `/merchant/payment/{id}/accept` | `hx-post` | `#pending-list` | `innerHTML` |
| `/merchant/payment/{id}/reject` | `hx-post` | `#pending-list` | `innerHTML` |
| `/payment/{id}/status` | `hx-get` (poll) | N/A (JSON) | N/A |
| `/admin/merchants/{id}/generate-qr` | `hx-post` | QR container | `innerHTML` |

---

## USSD Template Format

Templates use Python format syntax:

```
Airtel Money: *144*1*{merchant_phone}*{amount}#
Moov Cash:    *155*1*{merchant_phone}*{amount}#
```

**Variables**:
- `{merchant_phone}`: Merchant's phone number
- `{amount}`: Payment amount

**Example**:
```
Input:  *144*1*+23566112233*500#
Output: tel:*144*1*+23566112233*500#
```
