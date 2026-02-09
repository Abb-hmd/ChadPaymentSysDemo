# ChadPay Deployment Guide

## Local Development

### Prerequisites
- Python 3.11+
- pip
- (Optional) virtualenv or conda

### Setup

```bash
# 1. Clone/navigate to project
cd chadpay

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create environment file
cp .env.example .env

# 6. Edit .env with your settings
# Change SECRET_KEY and QR_SIGNING_KEY!

# 7. Initialize database and seed
cd scripts
python seed.py
cd ..

# 8. Run development server
python main.py
```

### Access
- App: http://localhost:8000
- Admin login: admin / admin123
- Merchant logins: See seed.py output

---

## Production Deployment (Render.com - Free Tier)

### Step 1: Prepare Your Code

```bash
# Create a GitHub repository and push your code
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/chadpay.git
git push -u origin main
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your GitHub repository

### Step 3: Configure Render Service

**Settings:**
- **Name**: chadpay (or your preferred name)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
```
APP_NAME=ChadPay
DEBUG=false
SECRET_KEY=your-super-secret-random-key-here
DATABASE_URL=sqlite:///./chadpay.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/I5e
AIRTEL_MONEY_TEMPLATE=*144*1*{merchant_phone}*{amount}#
MOOV_CASH_TEMPLATE=*155*1*{merchant_phone}*{amount}#
QR_SIGNING_KEY=your-qr-signing-key-here
BUS_FARE=300
MOTO_TAXI_FARE=300
TAXI_FARE=500
CONFIRMATION_RATE_LIMIT=30
```

**Important**: Generate your own keys:
```python
import secrets
print(secrets.token_hex(32))  # For SECRET_KEY
print(secrets.token_hex(16))  # For QR_SIGNING_KEY
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for build to complete
3. Your app will be live at `https://chadpay.onrender.com`

### Step 5: Seed Database

```bash
# SSH into Render instance (via Dashboard > Shell)
# Or use Render CLI

# Run seed script
cd scripts
python seed.py
```

---

## Alternative: Fly.io (Free Tier)

### Install Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
```

### Deploy
```bash
# Login
fly auth login

# Create app
fly launch --name chadpay --region cdg

# Set secrets
fly secrets set SECRET_KEY=your-secret-key
fly secrets set QR_SIGNING_KEY=your-qr-key
fly secrets set ADMIN_PASSWORD_HASH=your-hash

# Deploy
fly deploy
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `APP_NAME` | No | ChadPay | App name |
| `DEBUG` | No | false | Debug mode |
| `SECRET_KEY` | **Yes** | - | JWT signing key |
| `DATABASE_URL` | No | sqlite:///./chadpay.db | Database URL |
| `ADMIN_USERNAME` | No | admin | Admin username |
| `ADMIN_PASSWORD_HASH` | **Yes** | - | Bcrypt hash of admin password |
| `AIRTEL_MONEY_TEMPLATE` | No | *144*1*{merchant_phone}*{amount}# | Airtel USSD |
| `MOOV_CASH_TEMPLATE` | No | *155*1*{merchant_phone}*{amount}# | Moov USSD |
| `QR_SIGNING_KEY` | **Yes** | - | QR code signing key |
| `BUS_FARE` | No | 300 | Bus fare (XAF) |
| `MOTO_TAXI_FARE` | No | 300 | Moto-taxi fare (XAF) |
| `TAXI_FARE` | No | 500 | Taxi fare (XAF) |
| `CONFIRMATION_RATE_LIMIT` | No | 30 | Seconds between confirmations |

### Generate Admin Password Hash

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("your-password"))
```

---

## Post-Deployment Checklist

### Security
- [ ] Changed default SECRET_KEY
- [ ] Changed default QR_SIGNING_KEY
- [ ] Changed default admin password
- [ ] DEBUG set to false
- [ ] HTTPS enabled (Render/Fly provide this)

### Functionality
- [ ] Can access homepage
- [ ] Can login as admin
- [ ] Can create merchant
- [ ] Can generate QR code
- [ ] QR code scans correctly
- [ ] Payment flow works end-to-end
- [ ] Merchant can confirm payment

### Data
- [ ] Database is persisted (SQLite on disk)
- [ ] QR codes are saved in static/qr_codes/
- [ ] Audit logs are recording

---

## Updating Production

### Render
1. Push changes to GitHub
2. Render auto-deploys

### Fly.io
```bash
fly deploy
```

---

## Troubleshooting

### Database Issues
```bash
# Reset database (WARNING: loses all data!)
rm chadpay.db
python scripts/seed.py
```

### Static Files Not Loading
- Ensure `app/static` is in repo
- Check `static/qr_codes/` exists and is writable

### QR Codes Not Generating
- Check `QR_SIGNING_KEY` is set
- Ensure `static/qr_codes/` directory exists

### Session Issues
- Check `SECRET_KEY` is set and consistent
- Verify cookies are being set (HTTPS in production)

---

## Backup Strategy (Production)

### SQLite Backup
```bash
# Daily backup cron job
0 2 * * * cp /path/to/chadpay.db /backups/chadpay-$(date +%Y%m%d).db
```

### QR Codes Backup
```bash
# Backup QR codes
rsync -av /path/to/static/qr_codes/ /backups/qr_codes/
```

---

## Monitoring (Free Options)

### Uptime Monitoring
- UptimeRobot: https://uptimerobot.com (free tier)
- Ping your app every 5 minutes

### Error Tracking
- Sentry: https://sentry.io (free tier)
- Add to your app:
```python
import sentry_sdk
sentry_sdk.init("your-dsn-url")
```

---

## Scaling Considerations

When you outgrow the free tier:

1. **Database**: Migrate to PostgreSQL
2. **File Storage**: Move QR codes to S3/CloudFront
3. **Session Store**: Use Redis
4. **Load Balancing**: Multiple app servers
5. **CDN**: CloudFlare (free tier available)
