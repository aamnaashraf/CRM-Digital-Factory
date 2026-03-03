"""
Test script to verify the enhanced web form submission flow
"""
import asyncio
import sys
import os
import requests
import json

def test_enhanced_support_api():
    """Test the enhanced support API"""
    base_url = "http://localhost:8000"

    # Test data
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message for the AI agent. Can you help me with my account?",
        "priority": "medium"
    }

    try:
        # Submit support request
        response = requests.post(f"{base_url}/api/support/submit", json=test_data)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")

            if "response" in data and data["response"]:
                print("SUCCESS: API returns AI response as expected!")
                print(f"AI Response Preview: {data['response'][:100]}...")
            else:
                print("WARNING: API did not return AI response")

            if "status" in data:
                print(f"Status: {data['status']}")
            else:
                print("WARNING: Status field missing from response")

            if "ticket_id" in data:
                print(f"Ticket ID: {data['ticket_id']}")
            else:
                print("WARNING: Ticket ID missing from response")
        else:
            print(f"ERROR: API returned status code {response.status_code}")
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"✗ ERROR: {e}")

if __name__ == "__main__":
    print("Testing Enhanced Web Form Submission Flow...")
    test_enhanced_support_api()