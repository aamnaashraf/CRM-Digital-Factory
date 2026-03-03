"""
Reports API Endpoints
Generate various analytics reports including sentiment analysis
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pydantic import BaseModel
import json
import os

from src.database.connection import get_db_session
from src.database.models import Conversation, Message, ChannelType, ConversationStatus
from src.database.models import Customer
from src.scheduler.report_scheduler import daily_report_scheduler
from src.services.sentiment_report_service import SentimentReportService

router = APIRouter(prefix="/reports", tags=["Reports"])

class DailySentimentReport(BaseModel):
    """Daily sentiment report model"""
    date: str
    total_resolved: int
    avg_sentiment: float
    positive_count: int
    negative_count: int
    neutral_count: int
    channel_breakdown: Dict[str, Any]
    escalation_rate: float

class SentimentTrend(BaseModel):
    """Sentiment trend model"""
    date: str
    avg_sentiment: float
    total_count: int

class DailyReportResponse(BaseModel):
    """
    Response model for daily sentiment reports
    """
    report_date: str
    period_start: str
    period_end: str
    metrics: dict
    channel_breakdown: dict
    top_negative_topics: List[str]
    trend_comparison: dict

class ReportSummary(BaseModel):
    """
    Summary of available reports
    """
    date: str
    total_messages: int
    average_sentiment: float
    escalations: int

@router.get("/daily-sentiment", response_model=DailySentimentReport)
async def get_daily_sentiment_report(
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get daily sentiment analysis report for resolved conversations
    """
    try:
        # Get all resolved conversations with sentiment data
        result = await session.execute(
            select(Conversation, Message)
            .join(Message, Conversation.conversation_id == Message.conversation_id)
            .where(
                and_(
                    Conversation.status == ConversationStatus.RESOLVED,
                    Message.sentiment.isnot(None),  # Only messages with sentiment data
                    Message.sender == "agent"  # Get agent responses which contain sentiment
                )
            )
        )

        conversation_message_pairs = result.all()

        if not conversation_message_pairs:
            # Return empty report if no data
            return DailySentimentReport(
                date=datetime.utcnow().strftime("%Y-%m-%d"),
                total_resolved=0,
                avg_sentiment=0.0,
                positive_count=0,
                negative_count=0,
                neutral_count=0,
                channel_breakdown={"email": 0, "web": 0, "whatsapp": 0},
                escalation_rate=0.0
            )

        # Calculate sentiment statistics
        sentiments = []
        channel_counts = {"email": 0, "web": 0, "whatsapp": 0}

        for conv, msg in conversation_message_pairs:
            if msg.sentiment is not None:
                sentiments.append(msg.sentiment)
                channel_counts[conv.channel.value] += 1

        if not sentiments:
            avg_sentiment = 0.0
        else:
            avg_sentiment = sum(sentiments) / len(sentiments)

        # Categorize sentiments
        positive_count = sum(1 for s in sentiments if s and s > 0.1)
        negative_count = sum(1 for s in sentiments if s and s < -0.1)
        neutral_count = sum(1 for s in sentiments if s and -0.1 <= s <= 0.1)

        # Get total resolved conversations
        resolved_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.RESOLVED)
        )
        total_resolved = resolved_result.scalar_one_or_none() or 0

        # Calculate escalation rate
        total_result = await session.execute(
            select(func.count(Conversation.conversation_id))
        )
        total_conversations = total_result.scalar_one_or_none() or 1  # Avoid division by zero

        escalation_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.escalated == True)
        )
        total_escalated = escalation_result.scalar_one_or_none() or 0

        escalation_rate = (total_escalated / total_conversations) * 100 if total_conversations > 0 else 0.0

        return DailySentimentReport(
            date=datetime.utcnow().strftime("%Y-%m-%d"),
            total_resolved=total_resolved,
            avg_sentiment=round(avg_sentiment, 3),
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            channel_breakdown=channel_counts,
            escalation_rate=round(escalation_rate, 2)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sentiment report: {str(e)}")


@router.get("/sentiment-trend")
async def get_sentiment_trend(
    days: int = 30,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get sentiment trend over the specified number of days
    """
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Query to get daily sentiment averages
        result = await session.execute(
            select(
                func.date(Message.timestamp).label('date'),
                func.avg(Message.sentiment).label('avg_sentiment'),
                func.count(Message.message_id).label('count')
            )
            .join(Conversation, Message.conversation_id == Conversation.conversation_id)
            .where(
                and_(
                    Message.sentiment.isnot(None),
                    Message.timestamp >= start_date,
                    Message.sender == "agent"
                )
            )
            .group_by(func.date(Message.timestamp))
            .order_by(func.date(Message.timestamp))
        )

        rows = result.all()

        trend_data = []
        for row in rows:
            trend_data.append({
                "date": str(row.date) if row.date else "",
                "avg_sentiment": round(row.avg_sentiment or 0.0, 3),
                "total_count": row.count
            })

        return {
            "days": days,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "trend_data": trend_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sentiment trend: {str(e)}")


@router.get("/channel-performance")
async def get_channel_performance(
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get performance metrics by communication channel
    """
    try:
        result = await session.execute(
            select(
                Conversation.channel,
                func.count(Conversation.conversation_id).label('total'),
                func.avg(Message.sentiment).label('avg_sentiment'),
                func.count().filter(Conversation.status == ConversationStatus.RESOLVED).label('resolved'),
                func.count().filter(Conversation.escalated == True).label('escalated')
            )
            .join(Message, Conversation.conversation_id == Message.conversation_id)
            .where(Message.sentiment.isnot(None))
            .group_by(Conversation.channel)
        )

        rows = result.all()

        performance_data = []
        for row in rows:
            resolved_percentage = (row.resolved / row.total * 100) if row.total > 0 else 0
            escalation_rate = (row.escalated / row.total * 100) if row.total > 0 else 0

            performance_data.append({
                "channel": row.channel.value,
                "total_conversations": row.total,
                "avg_sentiment": round(row.avg_sentiment or 0.0, 3),
                "resolved": row.resolved,
                "resolved_percentage": round(resolved_percentage, 2),
                "escalated": row.escalated,
                "escalation_rate": round(escalation_rate, 2)
            })

        return {
            "performance_data": performance_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating channel performance report: {str(e)}")


@router.get("/sentiment/daily/{date}", response_model=DailyReportResponse)
async def get_daily_sentiment_report(date: str):
    """
    Get daily sentiment report for a specific date
    Date format: YYYY-MM-DD
    """
    try:
        # Parse date string
        report_date = datetime.strptime(date, "%Y-%m-%d")

        # Look for report file
        report_dir = "reports"
        if not os.path.exists(report_dir):
            os.makedirs(report_dir, exist_ok=True)

        filename = f"sentiment_report_{report_date.strftime('%Y%m%d')}.json"
        filepath = os.path.join(report_dir, filename)

        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail=f"Report not found for {date}")

        with open(filepath, 'r', encoding='utf-8') as f:
            report_data = json.load(f)

        return DailyReportResponse(**report_data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving report: {str(e)}")


@router.get("/sentiment/daily")
async def get_recent_daily_reports(limit: int = Query(7, ge=1, le=30)):
    """
    Get summaries of recent daily reports
    """
    try:
        report_dir = "reports"
        if not os.path.exists(report_dir):
            os.makedirs(report_dir, exist_ok=True)

        # Get all report files sorted by date
        report_files = []
        for filename in os.listdir(report_dir):
            if filename.startswith("sentiment_report_") and filename.endswith(".json"):
                report_files.append(filename)

        report_files.sort(reverse=True)  # Most recent first
        report_files = report_files[:limit]  # Limit results

        summaries = []
        for filename in report_files:
            filepath = os.path.join(report_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    report_data = json.load(f)

                # Extract date from filename for display
                date_str = filename.replace("sentiment_report_", "").replace(".json", "")
                if len(date_str) == 8:  # YYYYMMDD format
                    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

                summary = ReportSummary(
                    date=formatted_date,
                    total_messages=report_data.get("metrics", {}).get("total_messages", 0),
                    average_sentiment=report_data.get("metrics", {}).get("average_sentiment_score", 0.0),
                    escalations=report_data.get("metrics", {}).get("escalations", 0)
                )
                summaries.append(summary)
            except Exception as e:
                continue  # Skip invalid report files

        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving report summaries: {str(e)}")


@router.get("/sentiment/generate-today")
async def generate_todays_report():
    """
    Manually trigger generation of today's report (for testing purposes)
    """
    try:
        service = SentimentReportService()

        # Generate report for today
        today = datetime.now().date()
        report_datetime = datetime.combine(today, datetime.min.time())
        report = await service.generate_daily_report(report_datetime)
        filepath = await service.save_report(report)

        return {
            "status": "success",
            "message": "Today's report generated successfully",
            "filepath": filepath
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.get("/sentiment/generate-yesterday")
async def generate_yesterdays_report():
    """
    Manually trigger generation of yesterday's report (for testing purposes)
    """
    try:
        service = SentimentReportService()

        # Generate report for yesterday
        yesterday = (datetime.now() - timedelta(days=1)).date()
        report_datetime = datetime.combine(yesterday, datetime.min.time())
        report = await service.generate_daily_report(report_datetime)
        filepath = await service.save_report(report)

        return {
            "status": "success",
            "message": "Yesterday's report generated successfully",
            "filepath": filepath
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.get("/sentiment/download/{date}")
async def download_report_file(date: str):
    """
    Download a specific report file
    """
    try:
        # Parse date string
        report_date = datetime.strptime(date, "%Y-%m-%d")

        # Look for report file
        report_dir = "reports"
        filename = f"sentiment_report_{report_date.strftime('%Y%m%d')}.json"
        filepath = os.path.join(report_dir, filename)

        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail=f"Report file not found for {date}")

        return FileResponse(
            path=filepath,
            filename=filename,
            media_type='application/json'
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving report file: {str(e)}")


@router.post("/sentiment/start-scheduler")
async def start_daily_scheduler():
    """
    Start the daily report scheduler
    """
    try:
        await daily_report_scheduler.start()
        return {
            "status": "success",
            "message": "Daily report scheduler started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting scheduler: {str(e)}")


@router.get("/sentiment/status")
async def get_scheduler_status():
    """
    Get the status of the daily report scheduler
    """
    # Note: This is a simplified status check since APScheduler doesn't have a direct status check
    # In a real implementation, you'd track scheduler state
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir, exist_ok=True)

    return {
        "scheduler_status": "configured",  # This would be more dynamic in production
        "next_scheduled_run": "23:59:00 daily",  # This would be calculated from actual scheduler
        "reports_directory": reports_dir,
        "reports_generated": len([f for f in os.listdir(reports_dir) if f.startswith("sentiment_report_")]) if os.path.exists(reports_dir) else 0
    }