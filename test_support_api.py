"""
Test script to verify the enhanced web form submission flow
"""
import asyncio
import sys
import os

# Add the project root to path so we can import from src
sys.path.insert(0, os.path.abspath('.'))

from src.api.support import submit_support_request
from src.database.connection import get_db_session
from fastapi.testclient import TestClient
from src.api.support import router
from fastapi import FastAPI
from pydantic import EmailStr

app = FastAPI()
app.include_router(router)

# Test using the TestClient
def test_support_api():
    """Test the enhanced support API"""
    client = TestClient(app)

    # Test data
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message for the AI agent.",
        "priority": "medium"
    }

    # Submit support request
    response = client.post("/api/support/submit", json=test_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        data = response.json()
        if "response" in data and data["response"]:
            print("✓ SUCCESS: API returns AI response as expected!")
            print(f"AI Response: {data['response'][:100]}...")
        else:
            print("✗ WARNING: API did not return AI response")

        if "status" in data:
            print(f"Status: {data['status']}")
        else:
            print("✗ WARNING: Status field missing from response")
    else:
        print(f"✗ ERROR: API returned status code {response.status_code}")
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_support_api()