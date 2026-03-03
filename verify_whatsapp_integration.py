"""
WhatsApp Integration Verification Script

This script helps verify that your Twilio WhatsApp integration is working properly.
Run this after starting your server and setting up ngrok.
"""

import os
import sys
from pathlib import Path

def check_env_vars():
    """Check if required environment variables are set"""
    print("Checking environment variables...")

    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_WHATSAPP_NUMBER'
    ]

    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"  X {var} is not set")
            all_set = False
        else:
            print(f"  OK {var} is set ({len(value)} chars)")

    return all_set

def check_files_exist():
    """Check if required files exist"""
    print("\nChecking required files...")

    required_files = [
        'src/api/webhooks.py',
        'src/services/whatsapp_service.py',
        'src/services/agent_service.py',
        '.env'
    ]

    all_exist = True
    for file_path in required_files:
        file_obj = Path(file_path)
        if file_obj.exists():
            print(f"  OK {file_path} exists")
        else:
            print(f"  X {file_path} does not exist")
            all_exist = False

    return all_exist

def check_webhook_route():
    """Verify the webhook route is registered"""
    print("\nChecking webhook route registration...")
    try:
        from src.main import app
        whatsapp_route = None
        for route in app.routes:
            if hasattr(route, 'path') and route.path == '/api/webhooks/whatsapp':
                whatsapp_route = route
                break

        if whatsapp_route:
            print(f"  OK WhatsApp webhook route found: {whatsapp_route.path} ({whatsapp_route.methods})")
            return True
        else:
            print("  X WhatsApp webhook route not found")
            return False
    except Exception as e:
        print(f"  X Error checking route: {e}")
        return False

def run_verification():
    """Run complete verification"""
    print("WhatsApp Integration Verification")
    print("=" * 50)

    env_ok = check_env_vars()
    files_ok = check_files_exist()
    route_ok = check_webhook_route()

    print("\n" + "=" * 50)
    print("VERIFICATION RESULTS:")

    if env_ok and files_ok and route_ok:
        print("  SUCCESS! All checks passed! Your WhatsApp integration should be ready.")
        print("\nTo test:")
        print("  1. Start your server: 'uvicorn src.main:app --reload'")
        print("  2. Start ngrok: 'ngrok http 8000'")
        print("  3. Update Twilio webhook URL with your ngrok URL")
        print("  4. Send 'test' to your sandbox number")
        print("  5. You should receive 'Hello from AI! Webhook working!'")
    else:
        print("  FAILED! Some checks failed. Please fix the issues above before testing.")

    print("\nFor debugging, check your server logs for messages like:")
    print("  - 'WhatsApp webhook hit!'")
    print("  - 'From: whatsapp:...'")
    print("  - 'Body: test'")
    print("  - 'WhatsApp response sent successfully'")

if __name__ == "__main__":
    run_verification()