"""
Script to simulate an inbound email through the Gmail webhook
This will create an email channel conversation that will show up
as 'email' channel in the dashboard
"""
import requests
import json
import base64
import os

def simulate_inbound_email():
    print("Simulating inbound email through Gmail webhook...")
    print("=" * 50)

    # Create a simulated Gmail webhook notification
    # This simulates what Google's Gmail API would send when an email arrives

    # First, let's create a base64 encoded message data that represents an incoming email
    email_content = {
        "emailAddress": "aamnaashraf501@gmail.com",
        "historyId": "1234567890"
    }

    # This is what Google's Pub/Sub would send (simplified version)
    webhook_payload = {
        "message": {
            "data": base64.b64encode(json.dumps(email_content).encode()).decode(),
            "message_id": "test-message-id-12345"
        },
        "subscription": "projects/your-project/subscriptions/gmail-subscription"
    }

    try:
        print("1. Sending simulated Gmail webhook...")

        # Send the simulated webhook to trigger processing
        response = requests.post(
            "http://localhost:8000/api/webhooks/gmail",
            headers={"Content-Type": "application/json"},
            json=webhook_payload
        )

        print(f"   Response status: {response.status_code}")
        print(f"   Response: {response.json()}")

        if response.status_code == 200:
            print("   ✅ Webhook sent successfully")
        else:
            print(f"   ❌ Webhook failed: {response.text}")

    except Exception as e:
        print(f"   ❌ Error sending webhook: {e}")

    print(f"\n2. Alternative: Direct email processing test...")

    # Let's also try polling method which might help create an email channel conversation
    try:
        poll_response = requests.post(
            "http://localhost:8000/api/webhooks/gmail/poll",
            headers={"Content-Type": "application/json"},
            json={}
        )

        print(f"   Poll response: {poll_response.status_code}")
        if poll_response.status_code == 200:
            print(f"   Poll result: {poll_response.json()}")
    except Exception as e:
        print(f"   Poll error: {e}")

    print(f"\n3. Checking updated channel distribution...")
    try:
        analytics_response = requests.get("http://localhost:8000/api/dashboard/analytics")
        if analytics_response.status_code == 200:
            analytics = analytics_response.json()
            print(f"   Channel distribution: {analytics.get('channelDistribution', {})}")

            # Show the distribution more clearly
            channels = analytics.get('channelDistribution', {})
            for channel, count in channels.items():
                print(f"   - {channel}: {count} conversations")
        else:
            print(f"   Could not get analytics: {analytics_response.status_code}")
    except Exception as e:
        print(f"   Error getting analytics: {e}")

    print("\n" + "=" * 50)
    print("NOTES:")
    print("- Web channel = requests from web forms")
    print("- Email channel = requests from Gmail webhook")
    print("- To see 'email' on dashboard, actual emails must be processed via webhook")
    print("- The email response functionality is working (as verified earlier)")
    print("- Check your email inbox at aamnaashraf501@gmail.com for AI responses")

if __name__ == "__main__":
    simulate_inbound_email()