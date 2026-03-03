"""
Tests for API Endpoints
"""

import pytest
from httpx import AsyncClient
from fastapi import status

from src.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test basic health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["status"] == "operational"


@pytest.mark.asyncio
async def test_support_submit_valid():
    """Test support request submission with valid data"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test inquiry",
            "message": "This is a test message for support.",
            "priority": "medium"
        }

        response = await client.post("/api/support/submit", json=payload)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "ticket_id" in data
        assert data["estimated_response_time"] == "3 seconds"


@pytest.mark.asyncio
async def test_support_submit_invalid_email():
    """Test support request with invalid email"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "name": "Test User",
            "email": "invalid-email",
            "subject": "Test",
            "message": "Test message"
        }

        response = await client.post("/api/support/submit", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_support_submit_missing_fields():
    """Test support request with missing required fields"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "name": "Test User",
            "email": "test@example.com"
            # Missing subject and message
        }

        response = await client.post("/api/support/submit", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_webhook_whatsapp():
    """Test WhatsApp webhook endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Simulate Twilio webhook data
        form_data = {
            "From": "whatsapp:+1234567890",
            "To": "whatsapp:+14155238886",
            "Body": "Test message",
            "MessageSid": "SM1234567890"
        }

        response = await client.post("/api/webhooks/whatsapp", data=form_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "accepted"


@pytest.mark.asyncio
async def test_webhook_gmail():
    """Test Gmail webhook endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Simulate Gmail Pub/Sub notification
        import base64
        import json

        notification = {
            "emailAddress": "support@taskflow.com",
            "historyId": "12345"
        }

        encoded = base64.b64encode(json.dumps(notification).encode()).decode()

        payload = {
            "message": {
                "data": encoded,
                "messageId": "msg123"
            },
            "subscription": "projects/test/subscriptions/gmail"
        }

        response = await client.post("/api/webhooks/gmail", json=payload)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "accepted"
