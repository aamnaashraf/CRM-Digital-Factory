"""
Support Endpoints
Web form submission and customer support API
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging
from datetime import datetime

from src.database.connection import get_db_session
from src.database.models import Customer, Conversation, Message, ChannelType
# Use simplified config by default for local development
# This allows switching between configurations without code changes
import os
if os.getenv('USE_SIMPLE_CONFIG', 'true').lower() == 'true':
    from src.config_simple import get_settings
else:
    from src.config import get_settings

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


class SupportRequest(BaseModel):
    """Web form support request"""
    name: str = Field(..., min_length=1, max_length=255, description="Customer name")
    email: EmailStr = Field(..., description="Customer email")
    subject: str = Field(..., min_length=1, max_length=500, description="Subject")
    message: str = Field(..., min_length=10, max_length=5000, description="Message content")
    priority: Optional[str] = Field(default="medium", description="Priority level")


class SupportResponse(BaseModel):
    """Support request response"""
    success: bool
    ticket_id: str
    message: str
    estimated_response_time: str
    response: Optional[str] = None  # The AI-generated response
    status: str  # "resolved" or "escalated"


@router.post("/submit", response_model=SupportResponse)
async def submit_support_request(
    request: SupportRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Submit support request via web form

    This endpoint:
    1. Creates/updates customer record
    2. Creates conversation and initial message
    3. Processes request with AI synchronously for immediate response
    4. Queues background tasks for email delivery and post-processing
    5. Returns immediate AI response along with ticket ID
    """
    try:
        # Get or create customer
        from sqlalchemy import select
        result = await session.execute(
            select(Customer).where(Customer.primary_email == request.email)
        )
        customer = result.scalar_one_or_none()

        if not customer:
            customer = Customer(
                customer_id=request.email,
                primary_email=request.email,
                name=request.name,
                plan_type="free"
            )
            session.add(customer)
            await session.flush()
            logger.info(f"Created new customer: {request.email}")

        # Create conversation
        conversation_id = f"conv_{request.email}_{int(datetime.utcnow().timestamp())}"
        conversation = Conversation(
            conversation_id=conversation_id,
            customer_id=customer.customer_id,
            channel=ChannelType.WEB,
            subject=request.subject,
            status="open"
        )
        session.add(conversation)
        await session.flush()

        # Create initial message
        message_id = f"msg_{conversation_id}_0"
        message = Message(
            message_id=message_id,
            conversation_id=conversation_id,
            sender="customer",
            channel=ChannelType.WEB,
            content=request.message,
            sentiment=None  # Will be analyzed by agent
        )
        session.add(message)

        # Update customer stats
        customer.total_conversations += 1
        customer.total_messages += 1
        customer.last_contact_date = datetime.utcnow()

        # Commit the initial setup to the database
        await session.commit()

        logger.info(f"Support request created: {conversation_id}")

        # Process with AI agent synchronously to get immediate response
        from src.services.agent_service import AgentService
        from src.database.models import ChannelType as DBChannelType

        # Create agent service with the same session for the synchronous call
        agent_service = AgentService(session)

        # Process inquiry synchronously to get the AI response immediately
        response = await agent_service.process_inquiry(
            customer_id=request.email,
            channel=DBChannelType.WEB,
            message_content=request.message,
            subject=request.subject
        )

        # Ensure the database session is committed before queuing background tasks
        await session.commit()

        # Queue background tasks for email delivery and any other post-processing
        background_tasks.add_task(
            process_support_request_post_email,
            conversation_id,
            request.email,
            request.message,
            response.response_text  # Pass the response to ensure it's sent via email
        )

        return SupportResponse(
            success=True,
            ticket_id=conversation_id,
            message="We've received your request and here is an immediate response.",
            estimated_response_time="0 seconds",  # Response is immediate
            response=response.response_text,
            status="escalated" if response.should_escalate else "resolved"
        )

    except Exception as e:
        logger.error(f"Support request error: {e}", exc_info=True)
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process support request"
        )


@router.get("/ticket/{ticket_id}")
async def get_ticket_status(
    ticket_id: str,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get ticket status and conversation history
    """
    try:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        # Fetch conversation with messages
        result = await session.execute(
            select(Conversation)
            .where(Conversation.conversation_id == ticket_id)
            .options(selectinload(Conversation.messages))
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )

        return {
            "ticket_id": conversation.conversation_id,
            "status": conversation.status,
            "subject": conversation.subject,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "escalated": conversation.escalated,
            "message_count": len(conversation.messages),
            "messages": [
                {
                    "sender": msg.sender,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in conversation.messages
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get ticket error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve ticket"
        )


async def process_support_request_post_email(
    conversation_id: str,
    customer_email: str,
    message_content: str,
    ai_response_text: str
):
    """
    Process support request in background for email delivery only

    This function is used when the AI response has already been generated
    and we just need to handle email delivery and other post-processing.
    """
    from src.database.connection import get_db_manager
    from src.services.agent_service import AgentService
    from src.database.models import ChannelType as DBChannelType, Conversation, Message
    from sqlalchemy import select

    logger.info(f"Processing support request for email delivery: {conversation_id}")

    try:
        # Get database session
        db = get_db_manager()
        async with db.get_session() as session:
            # Get the conversation to confirm it exists
            result = await session.execute(
                select(Conversation).where(Conversation.conversation_id == conversation_id)
            )
            conversation = result.scalar_one_or_none()

            if not conversation:
                logger.error(f"Conversation not found: {conversation_id}")
                return

            # Create agent service to handle email delivery
            agent_service = AgentService(session)

            # Send the already generated response via email
            await agent_service._send_response(
                customer_id=customer_email,
                channel=DBChannelType.EMAIL,
                subject=conversation.subject or "Response to your support request",
                response_text=ai_response_text
            )

            logger.info(f"Email response delivered for: {conversation_id}")

    except Exception as e:
        logger.error(f"Support request email delivery error: {e}", exc_info=True)


async def process_support_request(
    conversation_id: str,
    customer_email: str,
    message_content: str
):
    """
    Process support request in background

    Uses AgentService to:
    1. Analyze sentiment
    2. Search knowledge base
    3. Generate response
    4. Check escalation
    5. Send response via email
    """
    from src.database.connection import get_db_manager
    from src.services.agent_service import AgentService
    from src.database.models import ChannelType as DBChannelType

    logger.info(f"Processing support request: {conversation_id}")

    try:
        # Get database session
        db = get_db_manager()
        async with db.get_session() as session:
            # Create agent service
            agent_service = AgentService(session)

            # Process inquiry
            response = await agent_service.process_inquiry(
                customer_id=customer_email,
                channel=DBChannelType.WEB,
                message_content=message_content,
                subject=""
            )

            logger.info(
                f"Support request processed: {conversation_id}, "
                f"escalated={response.should_escalate}, "
                f"sentiment={response.sentiment_score:.2f}"
            )

            # Send response via email if channel is email
            if response.should_escalate or response.response_text:
                # The response is already sent via the agent service
                pass

    except Exception as e:
        logger.error(f"Support request processing error: {e}", exc_info=True)
