"""
Test script for WhatsApp webhook functionality
"""
import requests
import json

def test_webhook_endpoint():
    """
    Test the WhatsApp webhook endpoint with a sample request
    """
    # The webhook endpoint as configured
    webhook_url = "http://localhost:8000/api/webhooks/whatsapp"

    # Sample Twilio webhook data (as form data)
    sample_data = {
        "From": "whatsapp:+1234567890",  # This would be the user's number
        "To": "whatsapp:+14155238886",   # This is the sandbox number
        "Body": "test",  # This should trigger our test response
        "MessageSid": "SMtest1234567890",
        "NumMedia": "0"
    }

    # Headers that Twilio would send (excluding signature for now since we've disabled validation)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    print("Testing WhatsApp webhook with 'test' message...")
    print(f"Sending to: {webhook_url}")
    print(f"Data: {sample_data}")

    try:
        response = requests.post(webhook_url, data=sample_data, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")

        if response.status_code == 200:
            print("✓ Webhook test successful!")
            if "Hello from AI! Webhook working!" in response.text:
                print("✓ Test response received correctly!")
            else:
                print("? Test response was sent but might not contain expected text")
        else:
            print("✗ Webhook test failed!")

    except Exception as e:
        print(f"✗ Error testing webhook: {e}")
        print("Make sure the server is running on port 8000")

if __name__ == "__main__":
    test_webhook_endpoint()