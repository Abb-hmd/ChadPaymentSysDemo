# ChadPay 12-Week Build Plan

## Overview

This plan is designed for a **solo developer** building a **real, demo-worthy POC** with $0 investment. Each week has clear goals, tasks, and acceptance criteria.

---

## Week 1: Foundation & Setup

### Goals
- Set up development environment
- Create project structure
- Implement database models

### Tasks
- [ ] Set up Python 3.11+ virtual environment
- [ ] Install FastAPI, SQLModel, and dependencies
- [ ] Create folder structure
- [ ] Implement database configuration
- [ ] Create all SQLModel models (merchants, users, payments, transactions, audit logs)
- [ ] Write database migration notes

### Acceptance Criteria
- [ ] `pip install -r requirements.txt` works
- [ ] Database tables created successfully
- [ ] Can insert/read test data via Python shell

### Demo
- Show database schema in SQLite browser

---

## Week 2: Authentication System

### Goals
- Implement merchant and admin authentication
- Set up JWT tokens and cookies

### Tasks
- [ ] Implement password hashing (bcrypt)
- [ ] Create JWT token utilities
- [ ] Build merchant login/logout (phone + PIN)
- [ ] Build admin login/logout (username + password)
- [ ] Create login templates
- [ ] Add authentication middleware

### Acceptance Criteria
- [ ] Merchant can login with phone/PIN
- [ ] Admin can login with username/password
- [ ] Sessions persist via cookies
- [ ] Unauthorized access is blocked

### Demo
- Login as merchant, show protected dashboard
- Login as admin, show admin panel

---

## Week 3: QR Code System

### Goals
- Implement signed QR code generation
- Create QR verification logic

### Tasks
- [ ] Implement HMAC signing for QR tokens
- [ ] Create QR code generation (PNG)
- [ ] Build QR verification endpoint
- [ ] Add QR code storage (static files)
- [ ] Test QR tampering detection

### Acceptance Criteria
- [ ] QR codes contain signed tokens
- [ ] Modified QR codes are rejected
- [ ] QR codes expire after 1 year
- [ ] QR images are saved and served

### Demo
- Generate QR code, show it can't be tampered

---

## Week 4: Customer Payment Flow (Part 1)

### Goals
- Build customer-facing payment pages
- Implement payment initiation

### Tasks
- [ ] Create merchant payment page template
- [ ] Build amount selection (preset/editable)
- [ ] Implement wallet selection UI
- [ ] Create payment initiation endpoint
- [ ] Generate USSD strings from templates
- [ ] Build payment initiated page with dialer

### Acceptance Criteria
- [ ] Customer can scan QR and see payment page
- [ ] Amount is preset for transport, editable for vendors
- [ ] USSD string is generated correctly
- [ ] Dial button opens phone dialer

### Demo
- Scan QR, select wallet, show USSD code

---

## Week 5: Customer Payment Flow (Part 2)

### Goals
- Complete payment confirmation flow
- Add rate limiting

### Tasks
- [ ] Build "I have paid" confirmation
- [ ] Implement customer confirmation endpoint
- [ ] Add rate limiting (30s between confirmations)
- [ ] Hash customer phone numbers
- [ ] Create waiting page with status polling
- [ ] Implement status check endpoint (HTMX)

### Acceptance Criteria
- [ ] Customer can confirm payment
- [ ] Rate limiting works (test with rapid clicks)
- [ ] Phone numbers are hashed, not stored plain
- [ ] Status polling updates automatically

### Demo
- Full customer flow: scan → pay → confirm → wait

---

## Week 6: Merchant Dashboard

### Goals
- Build merchant dashboard
- Implement payment confirmation actions

### Tasks
- [ ] Create merchant dashboard template
- [ ] Show pending confirmations
- [ ] Show today's summary
- [ ] Build accept/reject endpoints (HTMX)
- [ ] Create transaction on acceptance
- [ ] Build transaction history page

### Acceptance Criteria
- [ ] Merchant sees pending payments immediately
- [ ] Accept/Reject updates without page refresh
- [ ] Transaction created on acceptance
- [ ] History shows all transactions

### Demo
- Merchant logs in, sees pending payment, clicks "REÇU"

---

## Week 7: Admin Panel (Part 1)

### Goals
- Build admin dashboard
- Implement merchant CRUD

### Tasks
- [ ] Create admin dashboard template
- [ ] Show system stats (merchants, transactions)
- [ ] Build merchant list with search
- [ ] Create merchant form
- [ ] Implement merchant creation endpoint
- [ ] Build merchant detail page

### Acceptance Criteria
- [ ] Admin sees system overview
- [ ] Can search/filter merchants
- [ ] Can create new merchant with user
- [ ] Can view merchant details

### Demo
- Create new merchant, show in list

---

## Week 8: Admin Panel (Part 2)

### Goals
- Complete admin features
- Add QR generation and reporting

### Tasks
- [ ] Build QR code generation in admin
- [ ] Create transactions list with filters
- [ ] Implement CSV export
- [ ] Build audit logs viewer
- [ ] Create settings page (read-only)

### Acceptance Criteria
- [ ] Admin can generate QR for any merchant
- [ ] Can filter transactions by date/merchant
- [ ] CSV export works with correct data
- [ ] Audit logs show all actions

### Demo
- Generate QR, export transactions to CSV

---

## Week 9: UI Polish & Mobile Optimization

### Goals
- Improve UI/UX
- Optimize for low bandwidth

### Tasks
- [ ] Add loading states and spinners
- [ ] Improve button feedback (press effects)
- [ ] Add error pages with helpful messages
- [ ] Optimize CSS (purge unused styles)
- [ ] Test on slow connections
- [ ] Add French translations (complete)

### Acceptance Criteria
- [ ] UI feels responsive on 3G
- [ ] All error cases have helpful messages
- [ ] Buttons have clear press states
- [ ] No layout issues on small screens

### Demo
- Show app on simulated slow connection

---

## Week 10: Testing & Bug Fixes

### Goals
- Test all flows
- Fix bugs

### Tasks
- [ ] Test complete customer flow (end-to-end)
- [ ] Test merchant flow
- [ ] Test admin flow
- [ ] Test edge cases (expired payments, rate limits)
- [ ] Test QR tampering
- [ ] Fix all critical bugs
- [ ] Add basic logging

### Acceptance Criteria
- [ ] All happy paths work
- [ ] Edge cases handled gracefully
- [ ] No critical bugs
- [ ] Logs are informative

### Demo
- Run through all three user flows

---

## Week 11: Seed Data & Documentation

### Goals
- Create demo data
- Complete documentation

### Tasks
- [ ] Write seed script with demo merchants
- [ ] Create demo users with known credentials
- [ ] Generate demo QR codes
- [ ] Complete API documentation
- [ ] Write deployment guide
- [ ] Create README with setup instructions

### Acceptance Criteria
- [ ] `python scripts/seed.py` creates demo data
- [ ] Can login with demo credentials
- [ ] All documentation is complete
- [ ] README is clear for new developers

### Demo
- Fresh install, seed, login with demo accounts

---

## Week 12: Deployment & Launch Prep

### Goals
- Deploy to free hosting
- Prepare for demo

### Tasks
- [ ] Deploy to Render.com (free tier)
- [ ] Set up environment variables
- [ ] Test deployed version
- [ ] Print demo QR codes
- [ ] Prepare demo script
- [ ] Record demo video (optional)
- [ ] Write launch checklist

### Acceptance Criteria
- [ ] App is live on public URL
- [ ] All features work in production
- [ ] Demo QR codes printed and tested
- [ ] Can run demo without issues

### Demo
- Live demo with printed QR codes

---

## Weekly Time Commitment

| Week | Hours | Focus |
|------|-------|-------|
| 1 | 10-15 | Setup, models |
| 2 | 10-15 | Auth |
| 3 | 8-12 | QR codes |
| 4 | 10-15 | Customer flow |
| 5 | 10-15 | Customer flow (cont) |
| 6 | 10-15 | Merchant dashboard |
| 7 | 10-15 | Admin (part 1) |
| 8 | 10-15 | Admin (part 2) |
| 9 | 8-12 | UI polish |
| 10 | 10-15 | Testing |
| 11 | 8-12 | Documentation |
| 12 | 10-15 | Deployment |

**Total**: ~120-160 hours over 12 weeks (10-13 hours/week)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Scope creep | Stick to MVP features only |
| Technical blockers | Simplify, don't over-engineer |
| Time constraints | Cut features, not quality |
| Deployment issues | Test deployment early (Week 10) |

---

## Success Criteria

At the end of 12 weeks, you should have:

1. ✅ Working POC deployed online
2. ✅ Demo merchants with QR codes
3. ✅ Complete customer payment flow
4. ✅ Merchant dashboard with confirmations
5. ✅ Admin panel with reporting
6. ✅ Documentation for continued development
7. ✅ Real-world test with 2-3 drivers/vendors
