#!/usr/bin/env python3
"""
Script to reset the database and clear any duplicate entries
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from src.database.connection import init_database
from src.database.models import Conversation, Message, Customer
from src.config_simple import get_settings

async def reset_database():
    """Reset the database and clear any issues"""
    print("Resetting database to clear duplicate entries...")

    # Initialize the database with settings
    settings = get_settings()
    init_database(settings.database_url, settings.database_pool_size, settings.database_max_overflow)

    from src.database.connection import get_db_manager
    db = get_db_manager()

    async with db.get_session() as session:
        # Find conversations with duplicate customer_id and status combinations
        print("Checking for duplicate conversations...")

        # Group conversations by customer_id and channel and keep only the most recent
        from sqlalchemy import func
        result = await session.execute(
            select(
                Conversation.customer_id,
                Conversation.channel,
                func.count(Conversation.conversation_id).label('count')
            )
            .group_by(Conversation.customer_id, Conversation.channel)
            .having(func.count(Conversation.conversation_id) > 1)
        )
        duplicates = result.all()

        if duplicates:
            print(f"Found {len(duplicates)} customers with duplicate conversations")
            for dup in duplicates:
                print(f"  Customer: {dup.customer_id}, Channel: {dup.channel}, Count: {dup.count}")

                # Keep only the most recent conversation for each customer/channel combo
                conv_result = await session.execute(
                    select(Conversation)
                    .where(
                        Conversation.customer_id == dup.customer_id,
                        Conversation.channel == dup.channel
                    )
                    .order_by(Conversation.updated_at.desc())
                )
                conversations = conv_result.scalars().all()

                # Keep the first (most recent) and delete the rest
                for i, conv in enumerate(conversations):
                    if i > 0:  # Keep the first one, delete the rest
                        # First delete related messages
                        await session.execute(
                            delete(Message)
                            .where(Message.conversation_id == conv.conversation_id)
                        )
                        # Then delete the conversation
                        await session.delete(conv)

        await session.commit()
        print("Database reset complete!")

        # Show final counts
        conv_count = await session.execute(select(func.count(Conversation.conversation_id)))
        total_convs = conv_count.scalar()
        print(f"Total conversations after cleanup: {total_convs}")

if __name__ == "__main__":
    asyncio.run(reset_database())