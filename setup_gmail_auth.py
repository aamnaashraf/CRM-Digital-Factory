"""
Script to set up Gmail OAuth authentication
This script will trigger the OAuth flow for the first time
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set the environment to ensure we use simple config
os.environ['USE_SIMPLE_CONFIG'] = 'true'
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', 'fake-key-for-test')

# Import after setting environment
from src.services.gmail_service import gmail_service
import logging

# Set up logging to see what happens
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_gmail_auth():
    """Set up Gmail authentication for the first time"""
    print("Setting up Gmail authentication...")
    print("This will open a browser window for you to authenticate with Google.")
    print("After authentication, your credentials will be saved for future use.\n")

    try:
        print("Getting authenticated Gmail service...")

        # This call will trigger the OAuth flow if there's no valid token
        service = gmail_service.get_service()

        print("\n✅ Gmail authentication successful!")
        print("Token has been saved to:", gmail_service.oauth_service.settings.gmail_token_file)

        # Test basic functionality
        print("\nTesting basic Gmail connectivity...")
        import googleapiclient.errors

        # Get basic profile info to confirm access
        profile = service.users().getProfile(userId='me').execute()
        print(f"✅ Successfully connected to Gmail account: {profile.get('emailAddress', 'Unknown')}")

        return True

    except googleapiclient.errors.HttpError as e:
        if '"reason": "authError"' in str(e) or 'invalid_grant' in str(e).lower():
            print(f"\n❌ Authentication error: {e}")
            print("This may happen if:")
            print("1. The credentials in gmail-credentials.json are invalid")
            print("2. The OAuth consent hasn't been properly configured in Google Cloud Console")
            print("3. The redirect URIs in your credentials don't match what's expected")
            return False
        else:
            print(f"\n❌ HTTP Error: {e}")
            return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThis is likely the first time running the Gmail integration.")
        print("A browser window should have opened for you to authenticate with Google.")
        print("If no browser opened, check that:")
        print("1. Your gmail-credentials.json file is properly configured")
        print("2. The OAuth consent screen is properly set up in Google Cloud Console")
        print("3. Your client type is set to 'Desktop application' in the credentials")
        return False

if __name__ == "__main__":
    print("Gmail Authentication Setup")
    print("=" * 40)
    success = setup_gmail_auth()

    if success:
        print("\n🎉 Gmail integration is ready to use!")
        print("You can now receive emails via webhooks and send responses via the AI agent.")
    else:
        print("\n⚠️  Gmail integration setup incomplete.")
        print("Please verify your Google Cloud Console setup and credential file.")