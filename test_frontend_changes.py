"""
Test script to verify the frontend changes are correct
"""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

def test_frontend_routes():
    """Test that the frontend routes are set up correctly"""
    print("Testing frontend channel route configuration...")

    # Read the home page to verify the route changes
    home_file = "E:\\Hackathon 5\\frontend\\app\\page.tsx"
    with open(home_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if the routes are correctly updated
    web_form_correct = 'href="/support"' in content
    gmail_correct = 'href="/channels/gmail"' in content
    whatsapp_correct = 'href="/channels/whatsapp"' in content

    print(f"SUCCESS: Web Form route (should go to /support): {web_form_correct}")
    print(f"SUCCESS: Gmail route (should go to /channels/gmail): {gmail_correct}")
    print(f"SUCCESS: WhatsApp route (should go to /channels/whatsapp): {whatsapp_correct}")

    # Check if the new channel pages exist
    gmail_page_exists = os.path.exists("E:\\Hackathon 5\\frontend\\app\\channels\\gmail\\page.tsx")
    whatsapp_page_exists = os.path.exists("E:\\Hackathon 5\\frontend\\app\\channels\\whatsapp\\page.tsx")

    print(f"SUCCESS: Gmail channel page exists: {gmail_page_exists}")
    print(f"SUCCESS: WhatsApp channel page exists: {whatsapp_page_exists}")

    if web_form_correct and gmail_correct and whatsapp_correct and gmail_page_exists and whatsapp_page_exists:
        print("\n*** ALL FRONTEND CHANGES ARE CORRECT! ***")
        print("\nChannel routing updated as required:")
        print("- Web Form card -> /support (form submission)")
        print("- Gmail card -> /channels/gmail (webhook info)")
        print("- WhatsApp card -> /channels/whatsapp (webhook info)")
        return True
    else:
        print("\n*** Some changes are missing! ***")
        return False

def test_channel_pages_content():
    """Test the content of the channel pages"""
    print("\nTesting channel page content...")

    # Test Gmail page
    gmail_file = "E:\\Hackathon 5\\frontend\\app\\channels\\gmail\\page.tsx"
    with open(gmail_file, 'r', encoding='utf-8') as f:
        gmail_content = f.read()

    # Test WhatsApp page
    whatsapp_file = "E:\\Hackathon 5\\frontend\\app\\channels\\whatsapp\\page.tsx"
    with open(whatsapp_file, 'r', encoding='utf-8') as f:
        whatsapp_content = f.read()

    # Check for required elements in Gmail page
    gmail_has_instructions = "How to Test Gmail Channel" in gmail_content
    gmail_has_recent_activity = "Recent Gmail Activity" in gmail_content
    gmail_has_api_usage = "apiClient.getActivity()" in gmail_content

    print(f"SUCCESS: Gmail page has instructions: {gmail_has_instructions}")
    print(f"SUCCESS: Gmail page has recent activity: {gmail_has_recent_activity}")
    print(f"SUCCESS: Gmail page uses API: {gmail_has_api_usage}")

    # Check for required elements in WhatsApp page
    whatsapp_has_instructions = "How to Test WhatsApp Channel" in whatsapp_content
    whatsapp_has_recent_activity = "Recent WhatsApp Activity" in whatsapp_content
    whatsapp_has_api_usage = "apiClient.getActivity()" in whatsapp_content

    print(f"SUCCESS: WhatsApp page has instructions: {whatsapp_has_instructions}")
    print(f"SUCCESS: WhatsApp page has recent activity: {whatsapp_has_recent_activity}")
    print(f"SUCCESS: WhatsApp page uses API: {whatsapp_has_api_usage}")

    if (gmail_has_instructions and gmail_has_recent_activity and gmail_has_api_usage and
        whatsapp_has_instructions and whatsapp_has_recent_activity and whatsapp_has_api_usage):
        print("\n*** ALL CHANNEL PAGES HAVE CORRECT CONTENT! ***")
        return True
    else:
        print("\n*** Some channel pages are missing required content! ***")
        return False

if __name__ == "__main__":
    print("Testing Frontend Channel-Accurate UI Implementation")
    print("=" * 50)

    test1 = test_frontend_routes()
    test2 = test_channel_pages_content()

    print("\n" + "=" * 50)
    if test1 and test2:
        print("*** ALL TESTS PASSED - Frontend is ready for demo! ***")
    else:
        print("*** Some tests failed - please review implementation ***")