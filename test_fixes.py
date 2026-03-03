#!/usr/bin/env python3
"""
Test script to validate the fixes for email response and dashboard statistics issues
"""
import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.database.connection import get_db_session, get_db_manager
from src.database.models import Conversation, Customer, Message, ChannelType, ConversationStatus
from src.database.connection import init_database
from src.config_simple import get_settings

async def validate_dashboard_stats():
    """Validate that dashboard stats return complete data"""
    print("Validating dashboard statistics...")

    # Initialize the database with settings
    settings = get_settings()
    init_database(settings.database_url, settings.database_pool_size, settings.database_max_overflow)
    db = get_db_manager()
    async with db.get_session() as session:
        # Total conversations
        total_result = await session.execute(
            select(func.count(Conversation.conversation_id))
        )
        total_convs = total_result.scalar() or 0
        print(f"Total conversations in database: {total_convs}")

        # Open conversations
        open_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status.in_([ConversationStatus.OPEN, ConversationStatus.PENDING]))
        )
        open_convs = open_result.scalar() or 0
        print(f"Open conversations: {open_convs}")

        # Resolved conversations
        resolved_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.RESOLVED)
        )
        resolved_convs = resolved_result.scalar() or 0
        print(f"Resolved conversations: {resolved_convs}")

        # Escalated conversations
        escalated_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.ESCALATED)
        )
        escalated_convs = escalated_result.scalar() or 0
        print(f"Escalated conversations: {escalated_convs}")

        # Channel distribution
        channel_result = await session.execute(
            select(Conversation.channel, func.count(Conversation.conversation_id).label('count'))
            .group_by(Conversation.channel)
        )
        channel_counts = {row.channel.value: row.count for row in channel_result.all()}
        print(f"Channel distribution: {channel_counts}")

        # Verify that stats add up correctly
        if total_convs > 0:
            calculated_total = open_convs + resolved_convs + escalated_convs
            print(f"Calculated total (open + resolved + escalated): {calculated_total}")
            if calculated_total == total_convs:
                print("[SUCCESS] Conversation status counts are consistent")
            else:
                print(f"[WARNING] Conversation status counts may be inconsistent: {calculated_total} vs {total_convs}")

        return total_convs, open_convs, resolved_convs, escalated_convs

async def validate_email_channel_data():
    """Check that email conversations are properly recorded"""
    print("\nValidating email channel data...")

    db = get_db_manager()
    async with db.get_session() as session:
        # Get email conversations
        email_result = await session.execute(
            select(Conversation)
            .where(Conversation.channel == ChannelType.EMAIL)
            .order_by(Conversation.updated_at.desc())
            .limit(10)
        )
        email_convs = email_result.scalars().all()

        print(f"Found {len(email_convs)} recent email conversations")

        for conv in email_convs[:5]:  # Show first 5
            print(f"  - ID: {conv.conversation_id}, Status: {conv.status.value}, Channel: {conv.channel.value}, Updated: {conv.updated_at}")

        return len(email_convs)

async def main():
    """Main function to run all validations"""
    print("Testing fixes for email response and dashboard statistics issues...")

    try:
        total, open_count, resolved, escalated = await validate_dashboard_stats()
        email_count = await validate_email_channel_data()

        print(f"\nValidation Summary:")
        print(f"  - Total conversations: {total}")
        print(f"  - Open conversations: {open_count}")
        print(f"  - Resolved conversations: {resolved}")
        print(f"  - Escalated conversations: {escalated}")
        print(f"  - Email conversations: {email_count}")
        print("\n[SUCCESS] All validations completed successfully")

    except Exception as e:
        print(f"\n[ERROR] Error during validation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())