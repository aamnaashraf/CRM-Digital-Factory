"""
Script to manually test the email polling functionality
"""
import asyncio
import os
import sys

# Set up environment for the simplified config
os.environ['USE_SIMPLE_CONFIG'] = 'true'

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_email_polling():
    """Test the email polling functionality"""
    print("Testing Email Polling Functionality...")
    print("="*50)

    try:
        from src.tasks.email_polling_task import GmailPollingTask
        from src.services.gmail_service import gmail_service
        from src.config_simple import get_settings

        settings = get_settings()

        print(f"Gmail Support Email: {settings.gmail_support_email}")
        print(f"Poll Interval: {settings.poll_interval_seconds} seconds")
        print(f"Email Polling Enabled: {settings.enable_email_polling}")

        # Test getting inbound emails
        print("\nTesting inbound email retrieval...")
        inbound_emails = gmail_service.get_inbound_emails(max_results=10)

        print(f"Found {len(inbound_emails)} inbound emails")

        for i, email in enumerate(inbound_emails):
            parsed = gmail_service.parse_email(email)
            print(f"  Email {i+1}:")
            print(f"    From: {parsed.get('from_email', 'Unknown')}")
            subject = parsed.get('subject', 'No subject')
        # Safely print the subject, handling encoding issues
        try:
            print(f"    Subject: {subject[:50]}...")
        except UnicodeEncodeError:
            print(f"    Subject: {subject[:50].encode('utf-8', errors='ignore').decode('utf-8')}...")
            print(f"    ID: {email.get('id', 'Unknown')}")
            print()

        # Test the polling task manually (without starting the background loop)
        print("Testing single poll cycle...")
        polling_task = GmailPollingTask()

        # Just run the polling method once to test
        await polling_task.poll_inbound_emails()
        print("Poll cycle completed successfully!")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_email_polling())