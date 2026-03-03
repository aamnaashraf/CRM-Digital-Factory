"""
Test script to verify all channels are properly storing data in the database
"""
import asyncio
import os
from datetime import datetime, timedelta

# Add project root to path so we can import modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select, func
from src.database.connection import get_db_manager, init_database
from src.database.models import Conversation, Message, Customer, ChannelType


async def test_activity_data():
    """
    Test to see if all channels are properly storing data
    """
    print("Testing database activity data...")

    # Initialize database
    init_database("sqlite+aiosqlite:///./taskflow_crm.db", 5, 10)

    # Get database manager
    db = get_db_manager()

    async with db.get_session() as session:
        # Get all conversations ordered by most recent
        conv_result = await session.execute(
            select(Conversation)
            .order_by(Conversation.updated_at.desc())
            .limit(20)
        )
        conversations = conv_result.scalars().all()

        print(f"\nRecent conversations ({len(conversations)} found):")
        print("-" * 80)

        for conv in conversations:
            # Get the most recent message for this conversation
            msg_result = await session.execute(
                select(Message)
                .where(Message.conversation_id == conv.conversation_id)
                .order_by(Message.timestamp.desc())
                .limit(1)
            )
            msg = msg_result.scalar_one_or_none()

            message_content = "No message found" if not msg else msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
            sentiment = "No sentiment" if not msg else msg.sentiment

            print(f"ID: {conv.conversation_id[:20]}... | Channel: {conv.channel.value} | Status: {conv.status.value} | Updated: {conv.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Message: {message_content}")
            print(f"  Sentiment: {sentiment}")
            print()

        # Count conversations by channel
        print("\nConversation count by channel:")
        for channel_type in ChannelType:
            count_result = await session.execute(
                select(func.count(Conversation.conversation_id))
                .where(Conversation.channel == channel_type)
            )
            count = count_result.scalar_one()
            print(f"  {channel_type.value}: {count}")

        # Get recent messages across all channels
        print(f"\nRecent messages (any channel):")
        msg_result = await session.execute(
            select(Message, Conversation)
            .join(Conversation, Message.conversation_id == Conversation.conversation_id)
            .order_by(Message.timestamp.desc())
            .limit(15)
        )
        messages = msg_result.all()

        for msg, conv in messages:
            print(f"  {conv.channel.value} | {msg.sender} | {msg.content[:50]}... | {msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    asyncio.run(test_activity_data())