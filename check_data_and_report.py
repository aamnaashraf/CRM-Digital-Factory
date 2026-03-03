"""
Test script to check what data is available and generate today's report
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
from sqlalchemy import select, func

# Add project root to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.connection import init_database, get_db_manager
from src.database.models import Message, Conversation, Customer, ConversationStatus, ChannelType
from src.services.sentiment_report_service import SentimentReportService, SentimentCategory


async def check_data_and_generate_report():
    """Check what data is available and generate today's report"""
    try:
        print("Initializing database...")
        # Initialize the database connection
        init_database("sqlite+aiosqlite:///./taskflow_crm.db", 5, 10)

        db_manager = get_db_manager()

        # Check the overall data
        async with db_manager.get_session() as session:
            # Get total counts
            total_messages_result = await session.execute(select(func.count(Message.message_id)))
            total_messages = total_messages_result.scalar_one()

            total_convs_result = await session.execute(select(func.count(Conversation.conversation_id)))
            total_conversations = total_convs_result.scalar_one()

            print(f"Total messages in database: {total_messages}")
            print(f"Total conversations in database: {total_conversations}")

            # Get messages with sentiment
            messages_with_sentiment_result = await session.execute(
                select(func.count(Message.message_id))
                .where(Message.sentiment.isnot(None))
            )
            messages_with_sentiment = messages_with_sentiment_result.scalar_one()

            print(f"Messages with sentiment data: {messages_with_sentiment}")

            # Get conversation statuses
            status_counts_result = await session.execute(
                select(Conversation.status, func.count(Conversation.conversation_id))
                .group_by(Conversation.status)
            )
            status_counts = status_counts_result.all()

            print("Conversation status counts:")
            for status, count in status_counts:
                print(f"  {status}: {count}")

            # Get date range of messages
            date_range_result = await session.execute(
                select(func.min(Message.timestamp), func.max(Message.timestamp))
                .where(Message.sentiment.isnot(None))
            )
            min_date, max_date = date_range_result.first()

            print(f"Message date range with sentiment: {min_date} to {max_date if max_date else 'N/A'}")

        # Generate report for today
        service = SentimentReportService()

        # Try today
        today = datetime.now()
        print(f"\nGenerating report for today: {today.date()}")
        report = await service.generate_daily_report(today)
        filepath = await service.save_report(report)

        print(f"Today's report generated: {filepath}")
        print(f"Today's metrics: {report['metrics']}")

        # Also try yesterday
        yesterday = datetime.now() - timedelta(days=1)
        print(f"\nGenerating report for yesterday: {yesterday.date()}")
        report_yesterday = await service.generate_daily_report(yesterday)
        filepath_yesterday = await service.save_report(report_yesterday)

        print(f"Yesterday's report generated: {filepath_yesterday}")
        print(f"Yesterday's metrics: {report_yesterday['metrics']}")

    except Exception as e:
        print(f"Error checking data and generating report: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(check_data_and_generate_report())