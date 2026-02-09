"""
ChadPay Database Seed Script
----------------------------
Creates demo merchants and users for testing.
Run: python scripts/seed.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.database import engine, init_database
from app.models import Merchant, MerchantUser, MerchantType, Settings
from app.auth import get_password_hash
from app.config import get_settings


def seed_database():
    """Seed database with demo data."""
    print("🌱 Seeding database...")
    
    # Initialize database
    init_database()
    
    with Session(engine) as session:
        # Check if already seeded
        existing = session.exec(select(Merchant)).first()
        if existing:
            print("⚠️  Database already has merchants. Skipping seed.")
            return
        
        # Demo merchants
        demo_merchants = [
            {
                "name": "Bus Ligne 3 - N'Djamena",
                "code": "BUS003",
                "phone": "+235 66 11 22 33",
                "type": MerchantType.BUS,
                "location": "Terminus Moursal",
                "description": "Bus jaune ligne 3",
                "user_name": "Amadou Bus",
                "user_phone": "+235 66 11 22 33",
                "user_pin": "1234"
            },
            {
                "name": "Taxi Jaune - Centre Ville",
                "code": "TAXI001",
                "phone": "+235 66 44 55 66",
                "type": MerchantType.TAXI,
                "location": "Centre ville",
                "description": "Taxi jaune disponible 24/7",
                "user_name": "Moussa Taxi",
                "user_phone": "+235 66 44 55 66",
                "user_pin": "1234"
            },
            {
                "name": "Moto-Taxi - Farcha",
                "code": "MOTO001",
                "phone": "+235 66 77 88 99",
                "type": MerchantType.MOTO_TAXI,
                "location": "Farcha",
                "description": "Moto-taxi rapide et sécurisé",
                "user_name": "Issa Moto",
                "user_phone": "+235 66 77 88 99",
                "user_pin": "1234"
            },
            {
                "name": "Boutique Alimentation - Marché Central",
                "code": "VEND001",
                "phone": "+235 66 00 11 22",
                "type": MerchantType.VENDOR,
                "location": "Marché Central",
                "description": "Vente de produits alimentaires",
                "default_amount": 1000,
                "user_name": "Fatima Vendeuse",
                "user_phone": "+235 66 00 11 22",
                "user_pin": "1234"
            },
            {
                "name": "Kiosque Jus de Fruit",
                "code": "VEND002",
                "phone": "+235 66 33 44 55",
                "type": MerchantType.VENDOR,
                "location": "Avenue Charles de Gaulle",
                "description": "Jus frais naturels",
                "default_amount": 500,
                "user_name": "Hassan Jus",
                "user_phone": "+235 66 33 44 55",
                "user_pin": "1234"
            }
        ]
        
        for data in demo_merchants:
            # Create merchant
            merchant = Merchant(
                name=data["name"],
                code=data["code"],
                phone=data["phone"],
                merchant_type=data["type"],
                location=data.get("location"),
                description=data.get("description"),
                default_amount=data.get("default_amount")
            )
            session.add(merchant)
            session.flush()  # Get merchant.id
            
            # Create merchant user
            user = MerchantUser(
                phone=data["user_phone"],
                name=data["user_name"],
                merchant_id=merchant.id,
                pin_hash=get_password_hash(data["user_pin"]),
                is_admin=True
            )
            session.add(user)
            
            print(f"  ✅ Created: {merchant.name} ({merchant.code})")
            print(f"     Login: {user.phone} / PIN: {data['user_pin']}")
        
        # Add default settings
        settings_data = [
            ("airtel_money_template", get_settings().airtel_money_template, "Template USSD Airtel Money"),
            ("moov_cash_template", get_settings().moov_cash_template, "Template USSD Moov Cash"),
        ]
        
        for key, value, desc in settings_data:
            setting = Settings(key=key, value=value, description=desc)
            session.add(setting)
        
        session.commit()
        
        print("\n" + "="*50)
        print("✅ Database seeded successfully!")
        print("="*50)
        print("\nDemo Login Credentials:")
        print("-" * 30)
        print("Admin:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nMerchants (use any of these):")
        for data in demo_merchants:
            print(f"  {data['name']}")
            print(f"    Phone: {data['user_phone']}")
            print(f"    PIN: {data['user_pin']}")
        print("-" * 30)


if __name__ == "__main__":
    seed_database()
