"""
Debug script to check message content and agent responses
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
from src.database.models import Conversation, Message, ConversationStatus
from sqlalchemy import select

async def check_messages_debug():
    """Check message content and statuses"""
    print("Checking message content and statuses...")

    # Initialize the database
    init_database("sqlite+aiosqlite:///./taskflow_crm.db", 5, 2)

    db = get_db_manager()
    async with db.get_session() as session:
        # Get all conversations
        result = await session.execute(
            select(Conversation)
            .order_by(Conversation.created_at.desc())
            .limit(10)
        )
        conversations = result.scalars().all()

        print(f"Found {len(conversations)} recent conversations:")

        for i, conv in enumerate(conversations):
            print(f"\n{i+1}. Conversation: {conv.conversation_id}")
            print(f"   Channel: {conv.channel.value}")
            print(f"   Status: {conv.status.value}")
            print(f"   Escalated: {conv.escalated}")
            print(f"   Subject: {conv.subject[:50]}...")

            # Get messages for this conversation
            msg_result = await session.execute(
                select(Message)
                .where(Message.conversation_id == conv.conversation_id)
                .order_by(Message.timestamp.asc())
            )
            messages = msg_result.scalars().all()

            print(f"   Messages: {len(messages)}")
            for j, msg in enumerate(messages):
                sender = msg.sender
                content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                sentiment = msg.sentiment
                print(f"     {j+1}. {sender}: {content_preview}")
                print(f"         Sentiment: {sentiment}")

if __name__ == "__main__":
    asyncio.run(check_messages_debug())