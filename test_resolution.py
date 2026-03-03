#!/usr/bin/env python3
"""
Script to test a simple, non-escalating query to verify status updates work properly
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

async def test_simple_query():
    """Test a simple query that should result in resolution, not escalation"""
    print("Testing simple query to verify resolution status updates...")

    # Initialize the database with settings
    settings = get_settings()
    init_database(settings.database_url, settings.database_pool_size, settings.database_max_overflow)
    db = get_db_manager()

    async with db.get_session() as session:
        # Create a new test conversation that should get resolved, not escalated
        test_customer_id = "test@example.com"
        test_subject = "Question about features"

        # Get or create a test customer
        customer_result = await session.execute(
            select(Customer).where(Customer.customer_id == test_customer_id)
        )
        customer = customer_result.scalar_one_or_none()

        if not customer:
            customer = Customer(
                customer_id=test_customer_id,
                primary_email=test_customer_id,
                name="Test Customer",
                plan_type="free"
            )
            session.add(customer)
            await session.flush()

        # Create a conversation that should get resolved (not escalated)
        conversation_id = f"test_conv_{int(datetime.now().timestamp())}"
        conversation = Conversation(
            conversation_id=conversation_id,
            customer_id=customer.customer_id,
            channel=ChannelType.EMAIL,
            subject=test_subject,
            status=ConversationStatus.OPEN
        )
        session.add(conversation)
        await session.flush()

        # Create an initial customer message that should NOT trigger escalation
        message_id = f"msg_test_{int(datetime.now().timestamp())}"
        message = Message(
            message_id=message_id,
            conversation_id=conversation.conversation_id,
            sender="customer",
            channel=ChannelType.EMAIL,
            content="Hi, can you tell me about your premium features?",
            sentiment=None
        )
        session.add(message)
        await session.commit()  # Commit to ensure the conversation and message are in the DB

        print(f"Created test conversation ID: {conversation.conversation_id}")
        print(f"Test message: 'Hi, can you tell me about your premium features?'")

        # Now process with agent service - this should generate a response and set status to RESOLVED
        agent_service = AgentService(session)

        try:
            response = await agent_service.process_inquiry(
                customer_id=test_customer_id,
                channel=ChannelType.EMAIL,
                message_content="Hi, can you tell me about your premium features?",
                subject=test_subject,
                existing_conversation_id=conversation.conversation_id
            )

            print(f"AI response generated: Escalated={response.should_escalate}, Sentiment={response.sentiment_score:.2f}")
            print(f"Response text (first 100 chars): {response.response_text[:100]}...")

            # Refresh the conversation to see the updated status
            session.expunge(conversation)
            refresh_result = await session.execute(
                select(Conversation)
                .where(Conversation.conversation_id == conversation.conversation_id)
            )
            refreshed_conv = refresh_result.scalar_one_or_none()

            if refreshed_conv:
                print(f"Updated conversation status: {refreshed_conv.status.value}")
                print(f"Escalated: {refreshed_conv.escalated}")

                if refreshed_conv.status == ConversationStatus.RESOLVED:
                    print("[SUCCESS] Conversation was correctly updated to RESOLVED status")
                else:
                    print(f"[ERROR] Conversation status is {refreshed_conv.status.value}, expected RESOLVED")
            else:
                print("[ERROR] Could not refresh conversation")

        except Exception as e:
            print(f"[ERROR] Error processing inquiry with agent: {e}")
            import traceback
            traceback.print_exc()

        # Summary after processing
        total_result = await session.execute(
            select(func.count(Conversation.conversation_id))
        )
        total_convs = total_result.scalar() or 0

        resolved_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.RESOLVED)
        )
        resolved_convs = resolved_result.scalar() or 0

        print(f"\nOverall Stats after test:")
        print(f"  - Total conversations: {total_convs}")
        print(f"  - Resolved conversations: {resolved_convs}")

async def main():
    """Main function"""
    print("Testing simple query response and status updates...")
    try:
        await test_simple_query()
        print("\n[SUCCESS] Simple query test completed")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())