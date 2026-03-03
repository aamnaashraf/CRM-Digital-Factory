"""
Sentiment Report Service
Generates daily customer sentiment reports
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
import logging
import json
import os
from dataclasses import dataclass
from enum import Enum

from src.database.models import Message, Conversation, Customer, ChannelType, ConversationStatus
from src.database.connection import get_db_manager

logger = logging.getLogger(__name__)


@dataclass
class SentimentSummary:
    """Summary of sentiment data for a specific period"""
    total_messages: int
    positive_count: int
    neutral_count: int
    negative_count: int
    average_sentiment: float
    conversation_count: int
    escalation_count: int
    channel_breakdown: Dict[str, Dict[str, int]]  # channel -> {positive, neutral, negative}
    top_negative_topics: List[str]  # Most common negative topics


class SentimentCategory(Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class SentimentReportService:
    """
    Service to generate daily customer sentiment reports
    """

    def __init__(self):
        self.db_manager = get_db_manager()

    def categorize_sentiment(self, score: float) -> SentimentCategory:
        """
        Categorize sentiment score into positive/neutral/negative
        Score range: -1.0 to 1.0 where negative values are negative sentiment
        """
        if score >= 0.1:
            return SentimentCategory.POSITIVE
        elif score <= -0.1:
            return SentimentCategory.NEGATIVE
        else:
            return SentimentCategory.NEUTRAL

    async def get_sentiment_summary(self, start_date: datetime, end_date: datetime) -> SentimentSummary:
        """
        Get sentiment summary for a specific date range

        Args:
            start_date: Start of the period to analyze
            end_date: End of the period to analyze

        Returns:
            SentimentSummary with aggregated metrics
        """
        async with self.db_manager.get_session() as session:
            # Get all messages in the date range
            message_query = select(Message).where(
                and_(
                    Message.timestamp >= start_date,
                    Message.timestamp < end_date,
                    Message.sentiment.isnot(None)  # Only include messages with sentiment
                )
            ).options(selectinload(Message.conversation))

            result = await session.execute(message_query)
            messages = result.scalars().all()

            # Get all conversations in the date range
            conv_query = select(Conversation).where(
                and_(
                    Conversation.created_at >= start_date,
                    Conversation.created_at < end_date
                )
            )
            conv_result = await session.execute(conv_query)
            conversations = conv_result.scalars().all()

            # Initialize counters
            total_messages = len(messages)
            positive_count = 0
            neutral_count = 0
            negative_count = 0
            total_sentiment = 0.0
            channel_breakdown = {}
            escalation_count = 0

            # Process messages
            for message in messages:
                if message.sentiment is not None:
                    sentiment_cat = self.categorize_sentiment(message.sentiment)
                    total_sentiment += message.sentiment

                    if sentiment_cat == SentimentCategory.POSITIVE:
                        positive_count += 1
                    elif sentiment_cat == SentimentCategory.NEGATIVE:
                        negative_count += 1
                    else:
                        neutral_count += 1

                    # Track channel breakdown
                    channel = message.channel.value
                    if channel not in channel_breakdown:
                        channel_breakdown[channel] = {
                            SentimentCategory.POSITIVE.value: 0,
                            SentimentCategory.NEUTRAL.value: 0,
                            SentimentCategory.NEGATIVE.value: 0
                        }

                    channel_breakdown[channel][sentiment_cat.value] += 1

            # Count escalations
            for conv in conversations:
                if conv.status == ConversationStatus.ESCALATED:
                    escalation_count += 1

            # Calculate average sentiment
            average_sentiment = total_sentiment / total_messages if total_messages > 0 else 0.0

            # Get top negative topics (simplified - could be enhanced with NLP)
            top_negative_topics = await self._get_top_negative_topics(session, start_date, end_date)

            return SentimentSummary(
                total_messages=total_messages,
                positive_count=positive_count,
                neutral_count=neutral_count,
                negative_count=negative_count,
                average_sentiment=average_sentiment,
                conversation_count=len(conversations),
                escalation_count=escalation_count,
                channel_breakdown=channel_breakdown,
                top_negative_topics=top_negative_topics
            )

    async def _get_top_negative_topics(self, session: AsyncSession, start_date: datetime, end_date: datetime) -> List[str]:
        """
        Get top topics from negative conversations (simplified implementation)
        In a real scenario, this would use NLP to extract topics from negative messages
        """
        # For now, return common negative topics based on conversation subjects
        negative_convs_query = select(Conversation).where(
            and_(
                Conversation.created_at >= start_date,
                Conversation.created_at < end_date,
                Conversation.status == ConversationStatus.ESCALATED
            )
        )

        result = await session.execute(negative_convs_query)
        negative_conversations = result.scalars().all()

        # Extract common words/topics from subjects (simplified approach)
        topics = []
        for conv in negative_conversations[:5]:  # Limit to top 5 for now
            if conv.subject:
                topics.append(conv.subject[:50] + "..." if len(conv.subject) > 50 else conv.subject)

        return topics

    async def generate_daily_report(self, report_date: datetime = None) -> Dict[str, Any]:
        """
        Generate a daily sentiment report

        Args:
            report_date: Date to generate report for (defaults to yesterday)

        Returns:
            Dictionary containing the daily report
        """
        if report_date is None:
            # Default to yesterday
            report_date = datetime.now() - timedelta(days=1)

        # Set time range for the day (from 00:00:00 to 23:59:59)
        start_date = report_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)

        # Get summary for the day
        summary = await self.get_sentiment_summary(start_date, end_date)

        report = {
            "report_date": report_date.isoformat(),
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "metrics": {
                "total_messages": summary.total_messages,
                "positive_interactions": summary.positive_count,
                "neutral_interactions": summary.neutral_count,
                "negative_interactions": summary.negative_count,
                "average_sentiment_score": round(summary.average_sentiment, 3),
                "total_conversations": summary.conversation_count,
                "escalations": summary.escalation_count,
                "positive_ratio": round(summary.positive_count / summary.total_messages * 100, 2) if summary.total_messages > 0 else 0,
                "negative_ratio": round(summary.negative_count / summary.total_messages * 100, 2) if summary.total_messages > 0 else 0,
                "escalation_rate": round(summary.escalation_count / summary.conversation_count * 100, 2) if summary.conversation_count > 0 else 0
            },
            "channel_breakdown": summary.channel_breakdown,
            "top_negative_topics": summary.top_negative_topics,
            "trend_comparison": await self._get_trend_comparison(start_date, end_date)
        }

        logger.info(f"Generated daily sentiment report for {report_date.date()}: {report['metrics']}")
        return report

    async def _get_trend_comparison(self, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """
        Compare current day metrics with previous day
        """
        prev_start = start_date - timedelta(days=1)
        prev_end = end_date - timedelta(days=1)

        try:
            current_summary = await self.get_sentiment_summary(start_date, end_date)
            prev_summary = await self.get_sentiment_summary(prev_start, prev_end)

            if prev_summary.total_messages == 0:
                return {"message_volume_change": 0, "sentiment_trend": 0}

            volume_change = ((current_summary.total_messages - prev_summary.total_messages) /
                           prev_summary.total_messages) * 100

            sentiment_trend = current_summary.average_sentiment - prev_summary.average_sentiment

            return {
                "message_volume_change": round(volume_change, 2),
                "sentiment_trend": round(sentiment_trend, 3)
            }
        except Exception as e:
            logger.error(f"Error calculating trend comparison: {e}")
            return {"message_volume_change": 0, "sentiment_trend": 0}

    async def save_report(self, report: Dict[str, Any], output_dir: str = "reports") -> str:
        """
        Save the report to a JSON file

        Args:
            report: The report dictionary to save
            output_dir: Directory to save reports

        Returns:
            Path to saved report file
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        report_date = datetime.fromisoformat(report["report_date"])
        filename = f"sentiment_report_{report_date.strftime('%Y%m%d')}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Saved sentiment report to {filepath}")
        return filepath


# Example usage and scheduling
if __name__ == "__main__":
    import asyncio

    async def run_daily_report():
        service = SentimentReportService()
        report = await service.generate_daily_report()
        filepath = await service.save_report(report)
        print(f"Daily report generated: {filepath}")
        print(f"Summary: {report['metrics']}")

    # For testing
    # asyncio.run(run_daily_report())