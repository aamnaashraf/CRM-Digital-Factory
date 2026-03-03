#!/usr/bin/env python3
"""
Script to simulate a WhatsApp webhook call to test the endpoint
"""

import sys
import os
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from urllib.parse import urlencode

def simulate_whatsapp_webhook():
    """Simulate a WhatsApp webhook call to test the endpoint"""
    print(f"Simulating WhatsApp webhook at {datetime.now()}")

    # Test data that Twilio would send
    test_data = {
        'From': 'whatsapp:+15005550001',  # Test sender
        'To': 'whatsapp:+14155238886',   # Your sandbox number
        'Body': 'test',  # Test message body
        'MessageSid': 'SMtest123456789',
        'AccountSid': os.getenv('TWILIO_ACCOUNT_SID', ''),
        'NumMedia': '0'
    }

    # Send a POST request to the webhook endpoint
    webhook_url = "http://localhost:8000/api/webhooks/whatsapp"

    # Set proper headers for form-encoded data
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    print(f"Sending test data: {test_data}")
    print(f"Target URL: {webhook_url}")

    try:
        response = requests.post(
            webhook_url,
            data=test_data,
            headers=headers,
            timeout=30
        )

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            print("\n✅ Webhook test successful!")
            print("Check your backend logs to see if the webhook was processed correctly.")
        else:
            print(f"\n❌ Webhook test failed with status {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend server!")
        print("Make sure your backend is running on http://localhost:8000")
        print("Start it with: uvicorn src.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error sending webhook request: {e}")

def test_multiple_messages():
    """Test different types of messages"""
    print(f"\nTesting multiple message types at {datetime.now()}")

    test_cases = [
        {'message': 'test', 'description': 'Test message'},
        {'message': 'hi', 'description': 'Hi message'},
        {'message': 'hello', 'description': 'Hello message'},
        {'message': 'Can you help me?', 'description': 'Regular inquiry'}
    ]

    for test_case in test_cases:
        print(f"\nTesting: {test_case['description']} ('{test_case['message']}')")

        test_data = {
            'From': 'whatsapp:+15005550001',
            'To': 'whatsapp:+14155238886',
            'Body': test_case['message'],
            'MessageSid': 'SMtest123456789',
            'AccountSid': os.getenv('TWILIO_ACCOUNT_SID', ''),
            'NumMedia': '0'
        }

        webhook_url = "http://localhost:8000/api/webhooks/whatsapp"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            response = requests.post(
                webhook_url,
                data=test_data,
                headers=headers,
                timeout=30
            )

            print(f"  Response: {response.status_code} - {response.text[:100]}...")

        except Exception as e:
            print(f"  Error: {e}")

def main():
    print("=" * 60)
    print("WhatsApp Webhook Simulation Tool")
    print("=" * 60)

    print("This script simulates Twilio sending a WhatsApp message to your webhook.")
    print("Make sure your backend server is running before executing this test.\n")

    # Run the main test
    simulate_whatsapp_webhook()

    # Test different message types
    test_multiple_messages()

    print("\n" + "=" * 60)
    print("Simulation complete!")
    print("\nTo test with real WhatsApp messages:")
    print("1. Make sure your backend is running")
    print("2. Make sure ngrok is running and forwarding to your backend")
    print("3. Configure the webhook URL in your Twilio Sandbox settings")
    print("4. Send a message to your sandbox number")
    print("5. Check your backend logs and WhatsApp for responses")
    print("=" * 60)

if __name__ == "__main__":
    main()