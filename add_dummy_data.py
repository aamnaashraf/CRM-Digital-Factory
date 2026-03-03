"""
Test script to add some dummy data to the database for reports
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
import random

# Add project root to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.connection import init_database, get_db_manager
from src.database.models import Customer, Conversation, Message, ConversationStatus, ChannelType
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


async def add_dummy_data():
    """Add some dummy data to the database"""
    try:
        print("Initializing database...")
        # Initialize the database connection
        init_database("sqlite+aiosqlite:///./taskflow_crm.db", 5, 10)

        db_manager = get_db_manager()

        async with db_manager.get_session() as session:
            # Check if we already have customers
            result = await session.execute(select(Customer))
            existing_customers = result.scalars().all()

            if not existing_customers:
                # Add some dummy customers
                customers = [
                    Customer(
                        customer_id=f"cust_{i}",
                        primary_email=f"customer{i}@example.com",
                        name=f"Customer {i}",
                        company=f"Company {i}"
                    )
                    for i in range(1, 6)  # Create 5 customers
                ]

                for customer in customers:
                    session.add(customer)

                await session.commit()
                print(f"Added {len(customers)} customers")
            else:
                print(f"Found {len(existing_customers)} existing customers")

            # Get customers from the database
            result = await session.execute(select(Customer))
            customers = result.scalars().all()

            # Check if we already have conversations
            result = await session.execute(select(Conversation))
            existing_conversations = result.scalars().all()

            if not existing_conversations:
                # Add some dummy conversations
                statuses = [ConversationStatus.OPEN, ConversationStatus.RESOLVED, ConversationStatus.ESCALATED, ConversationStatus.CLOSED]
                channels = [ChannelType.EMAIL, ChannelType.WHATSAPP, ChannelType.WEB]

                conversations = []
                for i in range(10):  # Create 10 conversations
                    conv = Conversation(
                        conversation_id=f"conv_{i}",
                        customer_id=customers[i % len(customers)].customer_id,
                        channel=random.choice(channels),
                        status=random.choice(statuses),
                        subject=f"Support request #{i}",
                        escalated=random.choice([True, False])
                    )
                    conversations.append(conv)
                    session.add(conv)

                await session.commit()
                print(f"Added {len(conversations)} conversations")
            else:
                print(f"Found {len(existing_conversations)} existing conversations")

            # Get conversations from the database
            result = await session.execute(select(Conversation))
            conversations = result.scalars().all()

            # Check if we already have messages
            result = await session.execute(select(Message))
            existing_messages = result.scalars().all()

            if not existing_messages:
                # Add some dummy messages with sentiment scores
                sample_messages = [
                    "Great service, thank you!",
                    "The product works well for me.",
                    "I'm satisfied with the solution.",
                    "Could be better, but it's okay.",
                    "I'm not happy with this issue.",
                    "This isn't working as expected.",
                    "I need help with this problem.",
                    "Excellent support team!",
                    "Very disappointed with the service.",
                    "The feature is confusing to use."
                ]

                messages = []
                for i in range(20):  # Create 20 messages
                    # Generate sentiment scores (-1 to 1)
                    sentiment_score = random.uniform(-1.0, 1.0)

                    msg = Message(
                        message_id=f"msg_{i}",
                        conversation_id=conversations[i % len(conversations)].conversation_id,
                        sender=random.choice(['customer', 'agent']),
                        channel=conversations[i % len(conversations)].channel,
                        content=random.choice(sample_messages),
                        sentiment=sentiment_score
                    )
                    messages.append(msg)
                    session.add(msg)

                await session.commit()
                print(f"Added {len(messages)} messages with sentiment scores")
            else:
                print(f"Found {len(existing_messages)} existing messages")

        print("Successfully added dummy data to the database!")

    except Exception as e:
        print(f"Error adding dummy data: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(add_dummy_data())