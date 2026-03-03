"""
Script to check actual conversation status distribution
"""
import os
import sys
import asyncio

# Set up environment for the simplified config
os.environ['USE_SIMPLE_CONFIG'] = 'true'
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', 'fake-key-for-test')

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.connection import get_db_manager, init_database
from src.database.models import Conversation, ConversationStatus
from sqlalchemy import select

async def check_conversation_status():
    """Check the actual distribution of conversation statuses"""
    print("Checking conversation status distribution...")

    # Initialize the database
    init_database("sqlite+aiosqlite:///./taskflow_crm.db", 5, 2)

    db = get_db_manager()
    async with db.get_session() as session:
        # Count by status
        open_result = await session.execute(
            select(Conversation)
            .where(Conversation.status == ConversationStatus.OPEN)
        )
        open_conversations = open_result.scalars().all()

        resolved_result = await session.execute(
            select(Conversation)
            .where(Conversation.status == ConversationStatus.RESOLVED)
        )
        resolved_conversations = resolved_result.scalars().all()

        escalated_result = await session.execute(
            select(Conversation)
            .where(Conversation.status == ConversationStatus.ESCALATED)
        )
        escalated_conversations = escalated_result.scalars().all()

        pending_result = await session.execute(
            select(Conversation)
            .where(Conversation.status == ConversationStatus.PENDING)
        )
        pending_conversations = pending_result.scalars().all()

        closed_result = await session.execute(
            select(Conversation)
            .where(Conversation.status == ConversationStatus.CLOSED)
        )
        closed_conversations = closed_result.scalars().all()

        print(f"Total conversations: {len(open_conversations) + len(resolved_conversations) + len(escalated_conversations) + len(pending_conversations) + len(closed_conversations)}")
        print(f"Open: {len(open_conversations)}")
        print(f"Resolved: {len(resolved_conversations)}")
        print(f"Escalated: {len(escalated_conversations)}")
        print(f"Pending: {len(pending_conversations)}")
        print(f"Closed: {len(closed_conversations)}")

        print("\nChannels breakdown:")
        # Count by channel
        from src.database.models import ChannelType
        for channel_type in [ChannelType.EMAIL, ChannelType.WEB]:
            result = await session.execute(
                select(Conversation)
                .where(Conversation.channel == channel_type)
            )
            conversations = result.scalars().all()
            print(f"  {channel_type.value}: {len(conversations)}")

        # Check recent resolved conversations
        if resolved_conversations:
            print(f"\nRecent RESOLVED conversations:")
            for conv in resolved_conversations[-5:]:  # Last 5 resolved
                print(f"  - {conv.conversation_id[:50]}...")
                print(f"    Channel: {conv.channel.value}, Status: {conv.status.value}, Created: {conv.created_at}")
                if conv.escalated:
                    print(f"    Escalated: {conv.escalated}, Reason: {conv.escalation_reason}")

if __name__ == "__main__":
    asyncio.run(check_conversation_status())