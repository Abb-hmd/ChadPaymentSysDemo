"""
ChadPay Setup Verification Script
---------------------------------
Run this to verify your installation is correct.
"""

import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (need 3.11+)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    required = [
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "passlib",
        "jose",
        "qrcode",
        "jinja2"
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    return len(missing) == 0


def check_file_structure():
    """Check if all required files exist."""
    required_files = [
        "main.py",
        "requirements.txt",
        ".env.example",
        "app/__init__.py",
        "app/config.py",
        "app/database.py",
        "app/models.py",
        "app/auth.py",
        "app/audit.py",
        "app/qr_utils.py",
        "app/routers/__init__.py",
        "app/routers/public.py",
        "app/routers/merchant.py",
        "app/routers/admin.py",
        "app/templates/base.html",
        "app/templates/index.html",
        "app/templates/payment.html",
        "app/templates/merchant/login.html",
        "app/templates/merchant/dashboard.html",
        "app/templates/admin/login.html",
        "app/templates/admin/dashboard.html",
        "scripts/seed.py",
        "docs/README.md",
        "docs/ARCHITECTURE.md",
        "docs/API.md"
    ]
    
    missing = []
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for file in required_files:
        path = os.path.join(base_dir, file)
        if os.path.exists(path):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (missing)")
            missing.append(file)
    
    return len(missing) == 0


def check_environment():
    """Check if .env file exists."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    example_path = os.path.join(base_dir, ".env.example")
    
    if os.path.exists(env_path):
        print("✅ .env file exists")
        
        # Check for default keys
        with open(env_path) as f:
            content = f.read()
            if "change-me" in content or "your-" in content:
                print("⚠️  .env contains placeholder values - update before production!")
                return False
        return True
    else:
        print(f"❌ .env file missing (copy from .env.example)")
        return False


def check_database():
    """Check if database exists."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "chadpay.db")
    
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"✅ Database exists ({size} bytes)")
        return True
    else:
        print("⚠️  Database not created yet (run scripts/seed.py)")
        return False


def main():
    """Run all checks."""
    print("=" * 50)
    print("ChadPay Setup Verification")
    print("=" * 50)
    print()
    
    print("1. Python Version:")
    python_ok = check_python_version()
    print()
    
    print("2. Dependencies:")
    deps_ok = check_dependencies()
    print()
    
    print("3. File Structure:")
    files_ok = check_file_structure()
    print()
    
    print("4. Environment:")
    env_ok = check_environment()
    print()
    
    print("5. Database:")
    db_ok = check_database()
    print()
    
    print("=" * 50)
    
    all_ok = python_ok and deps_ok and files_ok
    
    if all_ok:
        print("✅ All critical checks passed!")
        print()
        print("Next steps:")
        if not db_ok:
            print("  1. Run: cd scripts && python seed.py")
        print("  2. Run: python main.py")
        print("  3. Open: http://localhost:8000")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        if not deps_ok:
            print("  - Install dependencies: pip install -r requirements.txt")
        if not env_ok:
            print("  - Create .env: cp .env.example .env")
        return 1


if __name__ == "__main__":
    sys.exit(main())
