"""
Dashboard Analytics Endpoints
Real-time statistics and metrics for the customer success dashboard
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from src.database.connection import get_db_session
from src.database.models import Customer, Conversation, Message, Ticket, Escalation, ChannelType, ConversationStatus
from src.config_simple import get_settings  # Use simplified config

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


class StatsResponse(BaseModel):
    """Response for dashboard statistics"""
    total_tickets: int
    open_tickets: int
    avg_sentiment: float
    total_customers: int
    avg_response_time: Optional[float] = None
    recent_activity: List[dict]


class ActivityItem(BaseModel):
    """Recent activity item"""
    id: str
    customer: str
    message: str
    channel: str
    time: str
    sentiment: Optional[float]
    status: str


# We're returning a dict directly instead of AnalyticsResponse to maintain camelCase
# The original AnalyticsResponse class is no longer used


@router.get("/stats")
async def get_dashboard_stats(session: AsyncSession = Depends(get_db_session)):
    """
    Get dashboard statistics including total tickets, open tickets,
    average sentiment, and recent activity
    """
    try:
        # Total tickets (conversations)
        total_tickets_result = await session.execute(
            select(func.count(Conversation.conversation_id))
        )
        total_tickets = total_tickets_result.scalar() or 0

        # Open tickets
        open_tickets_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status.in_([ConversationStatus.OPEN, ConversationStatus.PENDING]))
        )
        open_tickets = open_tickets_result.scalar() or 0

        # Average sentiment across all messages
        avg_sentiment_result = await session.execute(
            select(func.avg(Message.sentiment))
            .where(Message.sentiment.isnot(None))
        )
        avg_sentiment = avg_sentiment_result.scalar() or 0.0
        if avg_sentiment is not None:
            avg_sentiment = float(avg_sentiment)
        else:
            avg_sentiment = 0.0

        # Total customers
        total_customers_result = await session.execute(
            select(func.count(Customer.customer_id))
        )
        total_customers = total_customers_result.scalar() or 0

        # Recent activity (last 20 conversations/messages to show more data)
        recent_activity_result = await session.execute(
            select(Conversation, Customer, Message)
            .join(Customer, Conversation.customer_id == Customer.customer_id)
            .join(Message, Message.conversation_id == Conversation.conversation_id)
            .order_by(Conversation.updated_at.desc())
            .limit(20)
        )

        recent_activity = []
        for conv, customer, msg in recent_activity_result.all():
            activity_item = {
                "id": conv.conversation_id,
                "customer": customer.name or customer.customer_id,
                "message": msg.content[:100] + "..." if len(msg.content) > 100 else msg.content,
                "channel": conv.channel.value,
                "time": conv.updated_at.isoformat(),
                "sentiment": msg.sentiment,
                "status": conv.status.value
            }
            recent_activity.append(activity_item)

        return StatsResponse(
            total_tickets=total_tickets,
            open_tickets=open_tickets,
            avg_sentiment=avg_sentiment,
            total_customers=total_customers,
            recent_activity=recent_activity
        )

    except Exception as e:
        logger.error(f"Dashboard stats error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch dashboard statistics"
        )


@router.get("/activity")
async def get_recent_activity(
    limit: int = 50,  # Increased to 50 to show more diverse activity across channels
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get recent activity feed
    """
    try:
        # Get conversations ordered by most recent, then get their most recent message
        conv_result = await session.execute(
            select(Conversation, Customer)
            .join(Customer, Conversation.customer_id == Customer.customer_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )

        activities = []
        for conv, customer in conv_result.all():
            # Get the most recent message for this conversation
            msg_result = await session.execute(
                select(Message)
                .where(Message.conversation_id == conv.conversation_id)
                .order_by(Message.timestamp.desc())
                .limit(1)
            )
            msg = msg_result.scalar_one_or_none()

            message_content = "No message found"
            sentiment = 0.0
            if msg:
                message_content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                sentiment = msg.sentiment or 0.0

            activity_item = ActivityItem(
                id=conv.conversation_id,
                customer=customer.name or customer.customer_id,
                message=message_content,
                channel=conv.channel.value,
                time=conv.updated_at.isoformat(),
                sentiment=sentiment,
                status=conv.status.value
            )
            activities.append(activity_item)

        return {"activities": activities}

    except Exception as e:
        logger.error(f"Recent activity error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recent activity"
        )


@router.get("/activity/balanced")
async def get_balanced_activity(
    limit_per_channel: int = 5,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get a balanced recent activity feed showing items from all channels

    This endpoint ensures that all channels (email, whatsapp, web) are represented
    in the activity feed instead of one channel dominating due to high volume
    """
    try:
        all_activities = []

        # Get activities for each channel separately
        for channel_type in [ChannelType.EMAIL, ChannelType.WHATSAPP, ChannelType.WEB]:
            conv_result = await session.execute(
                select(Conversation, Customer)
                .join(Customer, Conversation.customer_id == Customer.customer_id)
                .where(Conversation.channel == channel_type)
                .order_by(Conversation.updated_at.desc())
                .limit(limit_per_channel)
            )

            for conv, customer in conv_result.all():
                # Get the most recent message for this conversation
                msg_result = await session.execute(
                    select(Message)
                    .where(Message.conversation_id == conv.conversation_id)
                    .order_by(Message.timestamp.desc())
                    .limit(1)
                )
                msg = msg_result.scalar_one_or_none()

                message_content = "No message found"
                sentiment = 0.0
                if msg:
                    message_content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                    sentiment = msg.sentiment or 0.0

                activity_item = {
                    "id": conv.conversation_id,
                    "customer": customer.name or customer.customer_id,
                    "message": message_content,
                    "channel": conv.channel.value,
                    "time": conv.updated_at.isoformat(),
                    "sentiment": sentiment,
                    "status": conv.status.value
                }
                all_activities.append(activity_item)

        # Sort all activities by time (most recent first) and limit to requested total
        all_activities.sort(key=lambda x: x["time"], reverse=True)
        final_activities = all_activities[:limit_per_channel * 3]  # 3 channels

        return {"activities": final_activities}

    except Exception as e:
        logger.error(f"Balanced activity error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch balanced activity"
        )


@router.get("/analytics")
async def get_analytics_data(session: AsyncSession = Depends(get_db_session)):
    """
    Get comprehensive analytics data
    """
    try:
        # Ticket volume by date (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        ticket_volume_result = await session.execute(
            select(
                func.date(Conversation.created_at).label('date'),
                func.count(Conversation.conversation_id).label('count')
            )
            .where(Conversation.created_at >= thirty_days_ago)
            .group_by(func.date(Conversation.created_at))
            .order_by(func.date(Conversation.created_at))
        )

        ticket_volume = [
            {"date": str(row.date), "count": row.count}
            for row in ticket_volume_result.all()
        ]

        # Channel distribution - include all channel types even if they have no conversations
        from src.database.models import ChannelType

        # First get all existing channel counts
        channel_result = await session.execute(
            select(
                Conversation.channel,
                func.count(Conversation.conversation_id).label('count')
            )
            .group_by(Conversation.channel)
        )

        # Convert to dict safely
        channel_distribution = {}
        for row in channel_result.all():
            if hasattr(row, 'channel') and hasattr(row, 'count'):
                channel_distribution[row.channel.value] = row.count

        # Ensure all channel types are present in the response, even with 0 count
        for channel_type in ChannelType:
            if channel_type.value not in channel_distribution:
                channel_distribution[channel_type.value] = 0

        # Sentiment trend (only if messages have sentiment data)
        sentiment_result = await session.execute(
            select(
                func.date(Message.timestamp).label('date'),
                func.avg(Message.sentiment).label('avg_sentiment')
            )
            .where(Message.sentiment.isnot(None))
            .where(Message.timestamp >= thirty_days_ago)
            .group_by(func.date(Message.timestamp))
            .order_by(func.date(Message.timestamp))
        )

        sentiment_trend = [
            {"date": str(row.date), "sentiment": float(row.avg_sentiment) if row.avg_sentiment else 0.0}
            for row in sentiment_result.all()
        ]

        # Resolution stats
        total_convs_result = await session.execute(
            select(func.count(Conversation.conversation_id))
        )
        total_convs = total_convs_result.scalar() or 0

        resolved_convs_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.RESOLVED)
        )
        resolved_convs = resolved_convs_result.scalar() or 0

        resolution_rate = (resolved_convs / total_convs * 100) if total_convs > 0 else 0

        escalation_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.escalated == True)
        )
        escalated_convs = escalation_result.scalar() or 0

        resolution_stats = {
            "total_conversations": total_convs,
            "resolved_conversations": resolved_convs,
            "resolution_rate": round(resolution_rate, 2),
            "escalated_conversations": escalated_convs
        }

        # Convert snake_case to camelCase for frontend compatibility
        camel_case_resolution_stats = {
            "totalConversations": resolution_stats.get("total_conversations", 0),
            "resolvedConversations": resolution_stats.get("resolved_conversations", 0),
            "resolutionRate": resolution_stats.get("resolution_rate", 0),
            "escalatedConversations": resolution_stats.get("escalated_conversations", 0)
        }

        return {
            "ticketVolume": ticket_volume,
            "channelDistribution": channel_distribution,
            "sentimentTrend": sentiment_trend,
            "resolutionStats": camel_case_resolution_stats
        }

    except Exception as e:
        logger.error(f"Analytics data error: {e}", exc_info=True)
        # Return partial data in case of error with camelCase for frontend compatibility
        return {
            "ticketVolume": [],
            "channelDistribution": {},
            "sentimentTrend": [],
            "resolutionStats": {
                "totalConversations": 0,
                "resolvedConversations": 0,
                "resolutionRate": 0,
                "escalatedConversations": 0
            }
        }


# Include specific endpoints for the frontend
@router.get("/metrics")
async def get_key_metrics(session: AsyncSession = Depends(get_db_session)):
    """
    Get key performance metrics for dashboard cards
    """
    try:
        # Total tickets
        total_tickets_result = await session.execute(
            select(func.count(Conversation.conversation_id))
        )
        total_tickets = total_tickets_result.scalar() or 0

        # Open tickets
        open_tickets_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status.in_([ConversationStatus.OPEN, ConversationStatus.PENDING]))
        )
        open_tickets = open_tickets_result.scalar() or 0

        # Average sentiment
        avg_sentiment_result = await session.execute(
            select(func.avg(Message.sentiment))
            .where(Message.sentiment.isnot(None))
        )
        avg_sentiment = avg_sentiment_result.scalar() or 0.0
        if avg_sentiment is not None:
            avg_sentiment = float(avg_sentiment)

        # Total customers
        total_customers_result = await session.execute(
            select(func.count(Customer.customer_id))
        )
        total_customers = total_customers_result.scalar() or 0

        # Recent conversations for activity (increase to show more data)
        recent_result = await session.execute(
            select(Conversation, Customer)
            .join(Customer, Conversation.customer_id == Customer.customer_id)
            .order_by(Conversation.updated_at.desc())
            .limit(20)
        )

        recent_activity = []
        for conv, customer in recent_result.all():
            recent_activity.append({
                "id": conv.conversation_id,
                "customer": customer.name or customer.customer_id,
                "subject": conv.subject[:50] + "..." if len(conv.subject) > 50 else conv.subject,
                "channel": conv.channel.value,
                "time": conv.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "status": conv.status.value
            })

        # Also get resolved and escalated conversation counts for complete view
        resolved_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.RESOLVED)
        )
        resolved_tickets = resolved_result.scalar() or 0

        escalated_result = await session.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.ESCALATED)
        )
        escalated_tickets = escalated_result.scalar() or 0

        # Get conversation count by channel
        channel_result = await session.execute(
            select(
                Conversation.channel,
                func.count(Conversation.conversation_id).label('count')
            )
            .group_by(Conversation.channel)
        )

        channel_counts = {}
        for row in channel_result.all():
            channel_counts[row.channel.value] = row.count

        return {
            "totalTickets": total_tickets,
            "openTickets": open_tickets,
            "resolvedTickets": resolved_tickets,
            "escalatedTickets": escalated_tickets,
            "avgSentiment": avg_sentiment if avg_sentiment is not None else 0.0,
            "totalCustomers": total_customers,
            "channelCounts": channel_counts,
            "recentActivity": recent_activity
        }

    except Exception as e:
        logger.error(f"Metrics error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch metrics"
        )