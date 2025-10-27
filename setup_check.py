#!/usr/bin/env python
"""
Setup verification script for foundation-dashboard
Checks that all required files and configurations are in place.
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists."""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_env_file():
    """Check if .env file exists and has required variables."""
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        print("  → Run: cp .env.example .env")
        print("  → Then edit .env with your credentials")
        return False

    print("✓ .env file exists")

    required_vars = [
        'MS_CLIENT_ID',
        'MS_CLIENT_SECRET',
        'MS_TENANT_ID',
        'REDIRECT_URI',
        'FLASK_SECRET_KEY'
    ]

    from dotenv import load_dotenv
    load_dotenv()

    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or 'your-' in value or 'here' in value:
            missing.append(var)

    if missing:
        print(f"✗ Missing or placeholder values in .env: {', '.join(missing)}")
        return False
    else:
        print("✓ All required environment variables are set")
        return True

def main():
    """Run all setup checks."""
    print("Foundation Dashboard - Setup Verification")
    print("=" * 50)
    print()

    all_checks_passed = True

    # Check required files
    print("Checking required files...")
    files_to_check = [
        ('app.py', 'Main application'),
        ('requirements.txt', 'Dependencies'),
        ('Procfile', 'Heroku config'),
        ('runtime.txt', 'Python version'),
        ('.env.example', 'Environment template'),
        ('.gitignore', 'Git ignore rules'),
        ('README.md', 'Documentation'),
        ('templates/dashboard/home.html', 'Home template'),
        ('templates/dashboard/pipeline.html', 'Pipeline template'),
    ]

    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_checks_passed = False

    print()

    # Check environment configuration
    print("Checking environment configuration...")
    if not check_env_file():
        all_checks_passed = False

    print()

    # Check Python version
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)")
        all_checks_passed = False

    print()

    # Summary
    print("=" * 50)
    if all_checks_passed:
        print("✓ All checks passed!")
        print()
        print("Next steps:")
        print("1. pip install -r requirements.txt")
        print("2. python app.py")
        print("3. Visit http://localhost:5000")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
