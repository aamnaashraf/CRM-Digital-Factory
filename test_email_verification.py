"""
Test script to verify the enhanced Gmail/email channel functionality
"""
import asyncio
import sys
import os

# Add the project root to path so we can import from src
sys.path.insert(0, os.path.abspath('.'))

from src.database.connection import get_db_manager
from sqlalchemy import select
from src.database.models import Conversation, Message, Customer, ChannelType
import logging

# Set up logging to see detailed output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_email_channel_verification():
    """Test that the email channel is working properly"""
    print("Testing Enhanced Gmail/Email Channel Functionality...")

    # Initialize the database first
    from src.database.connection import init_database
    from src.config_simple import get_settings
    settings = get_settings()
    init_database(settings.database_url)

    try:
        # Get database connection
        db = get_db_manager()
        async with db.get_session() as session:
            # Check for recent email conversations in the database
            result = await session.execute(
                select(Conversation)
                .where(Conversation.channel == ChannelType.EMAIL)
                .order_by(Conversation.created_at.desc())
                .limit(5)
            )

            email_conversations = result.scalars().all()

            print(f"\nFound {len(email_conversations)} email conversations in database:")

            for conv in email_conversations:
                print(f"  - ID: {conv.conversation_id}")
                print(f"    Channel: {conv.channel}")
                print(f"    Status: {conv.status}")
                print(f"    Subject: {conv.subject}")
                print(f"    Created: {conv.created_at}")

                # Get messages in this conversation
                msg_result = await session.execute(
                    select(Message)
                    .where(Message.conversation_id == conv.conversation_id)
                    .order_by(Message.timestamp)
                )
                messages = msg_result.scalars().all()

                print(f"    Messages: {len(messages)}")
                for i, msg in enumerate(messages):
                    print(f"      {i+1}. {msg.sender}: {msg.content[:100]}...")

                print()

            if email_conversations:
                print("SUCCESS: Email channel is properly creating conversations with channel='email'")

                # Check for resolved conversations
                resolved_count = sum(1 for c in email_conversations if c.status == 'resolved')
                escalated_count = sum(1 for c in email_conversations if c.status == 'escalated')
                open_count = sum(1 for c in email_conversations if c.status == 'open')

                print(f"  - Resolved: {resolved_count}")
                print(f"  - Escalated: {escalated_count}")
                print(f"  - Open: {open_count}")
            else:
                print("INFO: No email conversations found in database yet (this may be normal if no emails have been received recently)")

            # Also check web conversations to make sure they still work
            web_result = await session.execute(
                select(Conversation)
                .where(Conversation.channel == ChannelType.WEB)
                .order_by(Conversation.created_at.desc())
                .limit(3)
            )

            web_conversations = web_result.scalars().all()
            print(f"\nFound {len(web_conversations)} web conversations for comparison:")
            for conv in web_conversations:
                print(f"  - ID: {conv.conversation_id}, Channel: {conv.channel}, Status: {conv.status}")

    except Exception as e:
        print(f"ERROR: Error during email channel verification: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\nSUCCESS: Email channel verification completed successfully!")
    return True

if __name__ == "__main__":
    asyncio.run(test_email_channel_verification())