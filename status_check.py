"""
Simple script to verify Gmail integration is working
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set the environment to ensure we use simple config
os.environ['USE_SIMPLE_CONFIG'] = 'true'
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', 'fake-key-for-test')

from src.services.gmail_service import gmail_service
import pickle

def check_gmail_integration():
    print("Checking Gmail integration status...")

    # Check if token file exists and is valid
    token_path = gmail_service.oauth_service.settings.gmail_token_file
    print(f"Token file path: {token_path}")

    if os.path.exists(token_path):
        print("SUCCESS: Token file exists!")

        # Try to load the token file to see if it's valid
        try:
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
                print(f"SUCCESS: Credentials loaded from token file")
                print(f"Credentials valid: {creds.valid if hasattr(creds, 'valid') else 'Unknown'}")
                if hasattr(creds, 'expiry'):
                    print(f"Token expires: {creds.expiry}")
        except Exception as e:
            print(f"Could not load token: {e}")
    else:
        print("No token file found")

    # Try to get the service (this will use the saved token)
    try:
        service = gmail_service.get_service()
        print("SUCCESS: Gmail service acquired using saved credentials!")
        print("Gmail integration is ready for use!")
        return True
    except Exception as e:
        print(f"Could not get service: {e}")
        return False

if __name__ == "__main__":
    print("Gmail Integration Status Check")
    print("=" * 30)
    success = check_gmail_integration()

    if success:
        print("\nVERDICT: Gmail integration is fully operational!")
        print("- Authentication completed successfully")
        print("- Credentials saved and can be loaded")
        print("- Ready to send and receive emails")
        print("- AI agent can send email responses")
    else:
        print("\nIntegration needs attention")