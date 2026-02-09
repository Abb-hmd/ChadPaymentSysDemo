# ChadPay - Mobile Money Payment System for Chad

![ChadPay](https://img.shields.io/badge/ChadPay-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-teal)

A lightweight, USSD-based mobile money payment system for transport operators and street vendors in N'Djamena, Chad.

## 🎯 Mission

Enable **bus drivers**, **moto-taxi operators**, **taxi drivers**, and **street vendors** to accept mobile money payments without:
- ❌ Direct API integration with mobile money providers
- ❌ Payment licenses
- ❌ Fund custody
- ❌ Complex infrastructure

## ✨ Features

### For Customers
- 📱 Scan QR code to pay
- 💰 Preset amounts for transport (300/500 XAF)
- 🔢 Custom amounts for vendors
- 📞 Direct USSD dialer integration
- 🔒 Privacy-protected (phone numbers hashed)

### For Merchants
- 🔐 Simple login (phone + 4-digit PIN)
- 📊 Real-time dashboard
- ⏱️ Instant payment notifications
- ✅ One-tap confirmation (REÇU / NON REÇU)
- 📈 Transaction history

### For Admins
- 👥 Merchant management
- 🎨 QR code generation
- 📋 Transaction reporting
- 📤 CSV export
- 📜 Audit logs

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Customer   │     │  Merchant   │     │    Admin    │
│  (No Login) │     │ (Phone+PIN) │     │(User/Pass)  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
              ┌────────────┴────────────┐
              │    FastAPI + Jinja2     │
              │    HTMX + Tailwind      │
              └────────────┬────────────┘
                           │
                    ┌──────┴──────┐
                    │   SQLite    │
                    │  (SQLModel) │
                    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/chadpay.git
cd chadpay

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and change SECRET_KEY and QR_SIGNING_KEY

# 5. Seed database with demo data
cd scripts && python seed.py && cd ..

# 6. Run the application
python main.py
```

Visit: http://localhost:8000

### Demo Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**Merchants** (from seed script):
- Phone: `+235 66 11 22 33` / PIN: `1234` (Bus Ligne 3)
- Phone: `+235 66 44 55 66` / PIN: `1234` (Taxi Jaune)
- Phone: `+235 66 77 88 99` / PIN: `1234` (Moto-Taxi Farcha)

## 📱 User Flows

### Customer Payment Flow

```
1. Scan merchant QR code
        ↓
2. Select wallet (Airtel Money / Moov Cash)
        ↓
3. Click "Payer maintenant"
        ↓
4. Dial USSD code shown
        ↓
5. Complete payment in mobile money app
        ↓
6. Click "J'ai payé"
        ↓
7. Wait for merchant confirmation
```

### Merchant Confirmation Flow

```
1. Login with phone + PIN
        ↓
2. See pending payment on dashboard
        ↓
3. Verify payment received in wallet
        ↓
4. Tap "REÇU" to confirm
        ↓
5. Transaction recorded
```

## 💳 Payment Rules

| Service | Amount |
|---------|--------|
| Bus | 300 XAF |
| Moto-taxi | 300 XAF |
| Taxi | 500 XAF |
| Vendor | Custom |

## 🔐 Security Features

- **Signed QR Codes**: HMAC-signed tokens prevent tampering
- **Idempotent Payments**: Prevents duplicate charges
- **Rate Limiting**: 30-second cooldown between confirmations
- **Phone Hashing**: Customer phones stored as SHA256 hashes
- **bcrypt**: For password/PIN hashing
- **JWT Tokens**: Stateless session management
- **Audit Logs**: All actions tracked

## 📁 Project Structure

```
chadpay/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── database.py        # Database setup
│   ├── models.py          # SQLModel definitions
│   ├── auth.py            # Authentication logic
│   ├── audit.py           # Audit logging
│   ├── qr_utils.py        # QR code generation
│   ├── routers/
│   │   ├── public.py      # Customer-facing routes
│   │   ├── merchant.py    # Merchant dashboard routes
│   │   └── admin.py       # Admin panel routes
│   ├── templates/         # Jinja2 templates
│   └── static/            # CSS, JS, QR codes
├── scripts/
│   └── seed.py            # Demo data generator
├── docs/
│   ├── ARCHITECTURE.md    # System architecture
│   ├── API.md             # API documentation
│   ├── WIREFRAMES.md      # UI wireframes
│   ├── BUILD_PLAN.md      # 12-week build plan
│   └── DEPLOYMENT.md      # Deployment guide
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+, FastAPI |
| Database | SQLite (SQLModel) |
| Templates | Jinja2 |
| Frontend | HTMX, Tailwind CSS (CDN) |
| Auth | JWT, bcrypt |
| QR Codes | python-qrcode |

## 📝 API Documentation

See [docs/API.md](docs/API.md) for complete API reference.

### Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /m/{code}` | Customer payment page |
| `POST /m/{code}/initiate` | Initiate payment |
| `POST /payment/{id}/confirm` | Customer confirmation |
| `GET /merchant/dashboard` | Merchant dashboard |
| `POST /merchant/payment/{id}/accept` | Accept payment |
| `GET /admin/dashboard` | Admin dashboard |
| `GET /admin/transactions/export` | Export CSV |

## 🚀 Deployment

### Free Hosting Options

**Render.com (Recommended)**
1. Push code to GitHub
2. Connect Render to your repo
3. Set environment variables
4. Deploy automatically

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 📋 Roadmap

### Phase 1: POC (Current)
- [x] Basic payment flow
- [x] Merchant dashboard
- [x] Admin panel
- [x] QR code generation
- [x] CSV export

### Phase 2: Enhancements
- [ ] SMS notifications
- [ ] Multi-language support
- [ ] Receipt generation
- [ ] Analytics dashboard
- [ ] Mobile app (PWA)

### Phase 3: Scale
- [ ] PostgreSQL migration
- [ ] Redis for sessions
- [ ] API rate limiting
- [ ] Webhook integrations

## 🤝 Contributing

This is a POC for educational and demonstration purposes. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built for the people of N'Djamena, Chad
- Inspired by mobile money innovation across Africa
- Thanks to the FastAPI and HTMX communities

## 📞 Contact

For questions or support:
- Email: your-email@example.com
- Twitter: @yourhandle

---

**Made with ❤️ for Chad**
