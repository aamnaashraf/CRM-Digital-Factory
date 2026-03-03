"""
Script to check if email processing is creating conversations with the correct channel
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set the environment
os.environ['USE_SIMPLE_CONFIG'] = 'true'
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', 'fake-key-for-test')

from src.database.connection import get_db_manager
from src.database.models import Conversation, ChannelType
from sqlalchemy import select
import asyncio

async def check_email_conversations():
    print("Checking for email channel conversations...")

    db = get_db_manager()
    async with db.get_session() as session:
        # Count conversations by channel
        web_count_result = await session.execute(
            select(Conversation)
            .where(Conversation.channel == ChannelType.WEB)
        )
        web_conversations = web_count_result.scalars().all()

        email_count_result = await session.execute(
            select(Conversation)
            .where(Conversation.channel == ChannelType.EMAIL)
        )
        email_conversations = email_count_result.scalars().all()

        total_result = await session.execute(
            select(Conversation)
        )
        total_conversations = total_result.scalars().all()

        print(f"Total conversations: {len(total_conversations)}")
        print(f"Web conversations: {len(web_conversations)}")
        print(f"Email conversations: {len(email_conversations)}")

        if email_conversations:
            print("\nEmail conversations found:")
            for conv in email_conversations:
                print(f"  - ID: {conv.conversation_id}")
                print(f"    Customer: {conv.customer_id}")
                print(f"    Channel: {conv.channel.value}")
                print(f"    Status: {conv.status.value}")
                print(f"    Subject: {conv.subject}")
                print(f"    Created: {conv.created_at}")
                print()
        else:
            print("\nNo email conversations found yet.")
            print("\nThis could be because:")
            print("1. The polling process is still running in background")
            print("2. There might be an issue with the email processing logic")
            print("3. The emails found might not be processable by our system (e.g., sent to the same address)")

        # Check the most recent conversations regardless of channel
        recent_result = await session.execute(
            select(Conversation)
            .order_by(Conversation.created_at.desc())
            .limit(5)
        )
        recent_convs = recent_result.scalars().all()

        print(f"\n5 Most Recent Conversations:")
        for i, conv in enumerate(recent_convs):
            print(f"  {i+1}. {conv.conversation_id}")
            print(f"     Channel: {conv.channel.value}")
            print(f"     Customer: {conv.customer_id}")
            print(f"     Created: {conv.created_at}")
            print(f"     Status: {conv.status.value}")
            print()

async def main():
    await check_email_conversations()

if __name__ == "__main__":
    asyncio.run(main())