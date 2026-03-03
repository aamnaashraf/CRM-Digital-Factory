"""
Daily Report Scheduler
Handles scheduling of daily sentiment reports
"""
try:
    from apscheduler.schedulers.asyncio import AsyncScheduler
except ImportError:
    # For older versions of APScheduler
    from apscheduler.schedulers.asyncio import AsyncIOScheduler as AsyncScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime
import asyncio

from src.services.sentiment_report_service import SentimentReportService

logger = logging.getLogger(__name__)


class DailyReportScheduler:
    """
    Scheduler for daily sentiment reports
    """

    def __init__(self):
        self.scheduler = AsyncScheduler()
        self._sentiment_service = None  # Initialize lazily

    @property
    def sentiment_service(self):
        """Lazy initialization of sentiment service to avoid import-time db issues"""
        if self._sentiment_service is None:
            self._sentiment_service = SentimentReportService()
        return self._sentiment_service

    async def start(self):
        """
        Start the scheduler and add daily report job
        """
        self.scheduler.start()

        # Schedule daily report generation at 11:59 PM every day
        # This will generate the report for the current day
        self.scheduler.add_job(
            self._generate_daily_report,
            CronTrigger(hour=23, minute=59),  # Every day at 11:59 PM
            id='daily_sentiment_report'
        )

        logger.info("Daily report scheduler started, job scheduled for 11:59 PM daily")

    async def _generate_daily_report(self):
        """
        Internal method to generate the daily report
        """
        try:
            logger.info(f"Starting scheduled daily sentiment report generation at {datetime.now()}")
            report = await self.sentiment_service.generate_daily_report()
            filepath = await self.sentiment_service.save_report(report)
            logger.info(f"Successfully generated and saved daily report to {filepath}")
        except Exception as e:
            logger.error(f"Error generating daily report: {e}", exc_info=True)

    async def manual_generate_report(self, report_date: datetime = None):
        """
        Manually generate a report for testing purposes

        Args:
            report_date: Date to generate report for (defaults to yesterday)
        """
        try:
            report = await self.sentiment_service.generate_daily_report(report_date)
            filepath = await self.sentiment_service.save_report(report)
            logger.info(f"Manually generated report: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error in manual report generation: {e}", exc_info=True)
            raise

    async def stop(self):
        """
        Stop the scheduler
        """
        self.scheduler.shutdown()
        logger.info("Daily report scheduler stopped")


# Global scheduler instance
daily_report_scheduler = DailyReportScheduler()


async def initialize_scheduler():
    """
    Initialize and start the daily report scheduler
    """
    await daily_report_scheduler.start()


if __name__ == "__main__":
    # For testing the scheduler
    async def test_scheduler():
        print("Testing daily report scheduler...")

        # Start scheduler
        scheduler = DailyReportScheduler()
        await scheduler.start()

        # Generate a report manually for testing
        await scheduler.manual_generate_report()

        print("Scheduler test completed. Press Ctrl+C to stop...")

        # Keep running for a while to see scheduled jobs
        try:
            await asyncio.sleep(60)  # Run for 1 minute for testing
        except KeyboardInterrupt:
            print("Stopping scheduler...")
            await scheduler.stop()

    # Run test
    asyncio.run(test_scheduler())