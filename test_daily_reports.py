"""
Test script for daily sentiment reports functionality
"""
import asyncio
import os
from datetime import datetime, timedelta

# Add project root to path so we can import modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.sentiment_report_service import SentimentReportService
from src.scheduler.report_scheduler import daily_report_scheduler


async def test_daily_reports():
    """
    Test the daily sentiment reports functionality
    """
    print("Testing Daily Sentiment Reports...")

    # Test 1: Create service and generate a report
    print("\n1. Testing report generation...")
    service = SentimentReportService()

    # Generate a report for yesterday (since that would have data)
    yesterday = datetime.now() - timedelta(days=1)
    report = await service.generate_daily_report(yesterday)
    print(f"   Generated report for {yesterday.date()}")
    print(f"   Report date: {report['report_date']}")
    print(f"   Metrics: {report['metrics']}")

    # Test 2: Save the report
    print("\n2. Testing report saving...")
    filepath = await service.save_report(report)
    print(f"   Report saved to: {filepath}")

    # Test 3: Verify the file was created
    print("\n3. Verifying file was created...")
    if os.path.exists(filepath):
        print(f"   ✓ File exists: {filepath}")
        # Show file size
        size = os.path.getsize(filepath)
        print(f"   File size: {size} bytes")
    else:
        print(f"   ✗ File not found: {filepath}")

    # Test 4: Start scheduler
    print("\n4. Testing scheduler startup...")
    try:
        await daily_report_scheduler.start()
        print("   ✓ Scheduler started successfully")
    except Exception as e:
        print(f"   ✗ Scheduler failed to start: {e}")

    # Test 5: Try to generate another report for today
    print("\n5. Testing today's report generation...")
    today = datetime.now()
    today_report = await service.generate_daily_report(today)
    print(f"   Generated report for {today.date()}")
    print(f"   Metrics: {today_report['metrics']}")

    # Save today's report
    today_filepath = await service.save_report(today_report, "reports")
    print(f"   Today's report saved to: {today_filepath}")

    print("\nAll tests completed!")


if __name__ == "__main__":
    asyncio.run(test_daily_reports())