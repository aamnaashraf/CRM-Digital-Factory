"""
Test script to manually generate a daily sentiment report
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add project root to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.scheduler.report_scheduler import daily_report_scheduler
from src.database.connection import init_database
from src.services.sentiment_report_service import SentimentReportService


async def generate_test_report():
    """Generate a test report for today"""
    try:
        print("Initializing database...")
        # Initialize the database connection
        init_database("sqlite+aiosqlite:///./taskflow_crm.db", 5, 10)

        print("Generating test report...")

        # Initialize and start the scheduler
        await daily_report_scheduler.start()

        # Create a report service directly to test if there's data
        service = SentimentReportService()

        # Try to generate a report for yesterday
        yesterday = datetime.now() - timedelta(days=1)
        print(f"Attempting to generate report for {yesterday.date()}")

        report = await service.generate_daily_report(yesterday)
        filepath = await service.save_report(report)

        print(f"Report generated successfully: {filepath}")
        print(f"Report metrics: {report['metrics']}")

    except Exception as e:
        print(f"Error generating report: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            # Stop the scheduler if it was started
            await daily_report_scheduler.stop()
        except:
            pass


if __name__ == "__main__":
    asyncio.run(generate_test_report())