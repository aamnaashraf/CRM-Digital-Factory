#!/usr/bin/env python3
"""
Script to simulate email processing flow and test status updates
"""
import asyncio
import sys
import os
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.database.connection import init_database
from src.database.models import Conversation, Customer, Message, ChannelType, ConversationStatus
from src.services.agent_service import AgentService
from src.config_simple import get_settings
from src.database.connection import get_db_manager

async def simulate_email_flow():
    """Simulate an email flow to test status updates"""
    print("Simulating email flow to test status updates...")

    # Initialize the database with settings
    settings = get_settings()
    init_database(settings.database_url, settings.database_pool_size, settings.database_max_overflow)
    db = get_db_manager()

    async with db.get_session() as session:
        # Get all open email conversations that might need processing
        open_email_result = await session.execute(
            select(Conversation)
            .where(Conversation.channel == ChannelType.EMAIL)
            .where(Conversation.status.in_([ConversationStatus.OPEN, ConversationStatus.PENDING]))
            .order_by(Conversation.updated_at.desc())
            .limit(5)
        )
        open_emails = open_email_result.scalars().all()

        print(f"Found {len(open_emails)} open email conversations to process")

        if not open_emails:
            print("No open email conversations found for testing")
            return

        # Get the first conversation to simulate processing
        test_conversation = open_emails[0]
        print(f"Testing with conversation ID: {test_conversation.conversation_id}")
        print(f"Initial status: {test_conversation.status.value}")
        print(f"Subject: {test_conversation.subject}")

        # Get the last message in this conversation to use as input
        last_message_result = await session.execute(
            select(Message)
            .where(Message.conversation_id == test_conversation.conversation_id)
            .order_by(Message.timestamp.desc())
        )
        last_message = last_message_result.scalars().first()

        if last_message:
            print(f"Last message content (first 100 chars): {last_message.content[:100]}...")

            # Create agent service and process the conversation
            agent_service = AgentService(session)

            try:
                response = await agent_service.process_inquiry(
                    customer_id=test_conversation.customer_id,
                    channel=test_conversation.channel,
                    message_content=last_message.content,
                    subject=test_conversation.subject,
                    existing_conversation_id=test_conversation.conversation_id
                )

                print(f"AI response generated: {response.should_escalate} (escalated), sentiment: {response.sentiment_score:.2f}")

                # Refresh the conversation to see the updated status
                session.expunge(test_conversation)
                refresh_result = await session.execute(
                    select(Conversation)
                    .where(Conversation.conversation_id == test_conversation.conversation_id)
                )
                refreshed_conv = refresh_result.scalar_one_or_none()

                if refreshed_conv:
                    print(f"Updated conversation status: {refreshed_conv.status.value}")
                    print(f"Escalated: {refreshed_conv.escalated}")

            except Exception as e:
                print(f"Error processing inquiry with agent: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("No messages found in the conversation")

        # Summary after processing attempt
        total_result = await session.execute(
            select(func.count(Conversation.conversation_id))
        )
        total_convs = total_result.scalar() or 0

        resolved_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.RESOLVED)
        )
        resolved_convs = resolved_result.scalar() or 0

        print(f"\nOverall Stats after simulation:")
        print(f"  - Total conversations: {total_convs}")
        print(f"  - Resolved conversations: {resolved_convs}")

async def main():
    """Main function"""
    print("Testing email flow and status updates...")
    try:
        await simulate_email_flow()
        print("\n[SUCCESS] Simulation completed")
    except Exception as e:
        print(f"\n[ERROR] Simulation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())