#!/usr/bin/env python3
"""
Test script to verify imports are working correctly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    print("Testing imports...")

    # Test the specific import that was causing issues
    try:
        from src.tasks.email_polling_task import GmailPollingTask
        print("✅ GmailPollingTask imported successfully")
    except Exception as e:
        print(f"❌ Error importing GmailPollingTask: {e}")
        return False

    # Test the models import
    try:
        from src.database.models import ConversationStatus
        print("✅ ConversationStatus imported successfully")
    except Exception as e:
        print(f"❌ Error importing ConversationStatus: {e}")
        return False

    # Test other critical imports
    try:
        from src.services.agent_service import AgentService
        print("✅ AgentService imported successfully")
    except Exception as e:
        print(f"❌ Error importing AgentService: {e}")
        return False

    try:
        from src.services.gmail_service import GmailService
        print("✅ GmailService imported successfully")
    except Exception as e:
        print(f"❌ Error importing GmailService: {e}")
        return False

    print("✅ All imports working correctly!")
    return True

if __name__ == "__main__":
    test_imports()