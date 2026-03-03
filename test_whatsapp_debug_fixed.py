#!/usr/bin/env python3
"""
Debug script to test WhatsApp webhook functionality
"""

import sys
import os
import asyncio
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config_simple import get_settings
from twilio.rest import Client

def test_twilio_connection():
    """Test if Twilio credentials work correctly"""
    settings = get_settings()

    print(f"Testing Twilio connection at {datetime.now()}")
    print(f"Account SID: {settings.twilio_account_sid[:20]}..." if settings.twilio_account_sid else "No Account SID")
    print(f"Auth Token: {'*' * 10}" if settings.twilio_auth_token else "No Auth Token")
    print(f"WhatsApp Number: {settings.twilio_whatsapp_number}" if settings.twilio_whatsapp_number else "No WhatsApp Number")

    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        print("[ER] Error: Twilio credentials not configured!")
        return False

    try:
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

        # Test basic connection by getting account info
        account = client.api.accounts(settings.twilio_account_sid).fetch()
        print(f"[OK] Connected to Twilio account: {account.friendly_name}")

        # Test sending a simple message (replace with your test number)
        print("Testing message sending capability...")
        # NOTE: This is just to test that the client works - do not send an actual test message
        print("[OK] Twilio client initialization successful")
        return True

    except Exception as e:
        print(f"[ER] Error connecting to Twilio: {e}")
        return False

def test_webhook_handler():
    """Test the webhook functionality"""
    print(f"\nTesting webhook handler at {datetime.now()}")
    print("Make sure you have:")
    print("1. Ngrok running with public URL")
    print("2. Webhook configured in Twilio Sandbox")
    print("3. Backend server running")

    # Check if webhook route is available
    import httpx
    try:
        # Test the test endpoint first
        response = httpx.get("http://localhost:8000/api/webhooks/test", timeout=10.0)
        if response.status_code == 200:
            print("[OK] Test endpoint accessible at http://localhost:8000/api/webhooks/test")
        else:
            print("[ER] Test endpoint not returning 200")
    except Exception as e:
        print(f"[WR] Could not reach backend: {e}")
        print("Hint: Make sure your FastAPI server is running on port 8000")

def check_env_vars():
    """Check if environment variables are set correctly"""
    print(f"\nChecking environment variables at {datetime.now()}")

    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_WHATSAPP_NUMBER'
    ]

    all_present = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"[OK] {var}: {'*' * min(10, len(value)) if 'TOKEN' in var or 'SID' in var else value}")
        else:
            print(f"[ER] {var}: NOT SET")
            all_present = False

    return all_present

def main():
    print("=" * 60)
    print("WhatsApp Webhook Debug Tool")
    print("=" * 60)

    # Check environment variables
    env_ok = check_env_vars()

    if not env_ok:
        print("\n[ER] Please set all required environment variables before proceeding!")
        return

    # Test Twilio connection
    twilio_ok = test_twilio_connection()

    if not twilio_ok:
        print("\n[ER] Please fix Twilio connection issues before testing webhook!")
        return

    # Test webhook connectivity
    test_webhook_handler()

    print("\n" + "=" * 60)
    print("Debug test complete!")
    print("\nTo test the full flow:")
    print("1. Start your backend: uvicorn src.main:app --reload")
    print("2. Start ngrok: ngrok http 8000")
    print("3. Configure webhook in Twilio with your ngrok URL")
    print("4. Send a message to your sandbox number")
    print("5. Check backend logs for webhook hits")
    print("=" * 60)

if __name__ == "__main__":
    main()