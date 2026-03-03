"""
Background Task for Gmail Polling

This module implements a background polling task that periodically checks
for new inbound emails and processes them into the ticket system.
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

# Use simplified config by default for local development
import os
if os.getenv('USE_SIMPLE_CONFIG', 'true').lower() == 'true':
    from src.config_simple import get_settings
else:
    from src.config import get_settings

from src.database.connection import get_db_manager
from src.database.models import Customer, Conversation, Message, ChannelType, ConversationStatus
from src.services.gmail_service import gmail_service
from src.services.agent_service import AgentService

logger = logging.getLogger(__name__)
settings = get_settings()

class GmailPollingTask:
    """
    Background task to poll Gmail for new inbound emails
    """

    def __init__(self):
        self.running = False
        self.settings = get_settings()
        self.poll_interval = self.settings.poll_interval_seconds
        self.last_poll_time = None

    async def start_polling(self):
        """
        Start the continuous polling loop
        """
        self.running = True
        logger.info(f"Starting Gmail polling task with interval: {self.poll_interval} seconds")

        while self.running:
            try:
                await self.poll_inbound_emails()
                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                # Wait a bit before retrying to avoid rapid error cycles
                await asyncio.sleep(10)

    async def stop_polling(self):
        """
        Stop the polling task
        """
        self.running = False
        logger.info("Gmail polling task stopped")

    async def poll_inbound_emails(self):
        """
        Poll for new inbound emails and process them
        """
        try:
            # Use the improved method to get only inbound emails
            # Query to get only emails that are not from the user (inbound emails)
            query = f"is:unread in:inbox -from:{settings.gmail_support_email}"

            inbound_emails = gmail_service.get_inbound_emails(max_results=10)

            if not inbound_emails:
                logger.debug("No new inbound emails found")
                return

            logger.info(f"Found {len(inbound_emails)} new inbound emails to process")

            for email in inbound_emails:
                try:
                    await self.process_single_email(email)
                    # Mark as read after successful processing
                    message_id = email.get('id')
                    if message_id:
                        gmail_service.mark_as_read(message_id)
                        logger.debug(f"Marked email {message_id} as read")

                except Exception as e:
                    logger.error(f"Error processing email: {e}", exc_info=True)
                    # Continue with the next email even if one fails
                    continue

        except Exception as e:
            logger.error(f"Error polling inbound emails: {e}", exc_info=True)

    async def process_single_email(self, email: dict):
        """
        Process a single email into a ticket conversation
        """
        try:
            parsed_email = gmail_service.parse_email(email)
            email_id = parsed_email.get('id')
            thread_id = parsed_email.get('thread_id')
            sender_email = parsed_email.get('from_email')
            subject = parsed_email.get('subject', '')
            body = parsed_email.get('body', parsed_email.get('snippet', ''))

            if not sender_email:
                logger.warning(f"No sender email found in message: {email_id}")
                return

            logger.info(f"Processing email from {sender_email} with subject '{subject}' (ID: {email_id})")

            # Get database session and process the email
            db = get_db_manager()
            async with db.get_session() as session:
                # Check if we've already processed this email to prevent duplicates
                # We'll look for messages with this email_id in the content or metadata
                from sqlalchemy import select
                # Using existing conversation and message models to track email processing
                # Check if a conversation already exists for this thread_id to prevent duplicate processing
                if thread_id:
                    existing_conv_result = await session.execute(
                        select(Conversation).where(Conversation.conversation_id.like(f"email_{sender_email}%"))
                    )
                    existing_convs = existing_conv_result.scalars().all()

                    # Check if any existing conversation has messages with content similar to the current email
                    for existing_conv in existing_convs:
                        existing_msg_result = await session.execute(
                            select(Message).where(
                                Message.conversation_id == existing_conv.conversation_id,
                                Message.content.contains(body[:50] if body else "")  # Check for similar content
                            )
                        )
                        existing_msgs = existing_msg_result.scalars().all()
                        if existing_msgs and body:
                            logger.info(f"Duplicate email detected for thread {thread_id}, skipping processing")
                            return

                # Get or create customer
                result = await session.execute(
                    select(Customer).where(Customer.primary_email == sender_email)
                )
                customer = result.scalar_one_or_none()

                if not customer:
                    customer = Customer(
                        customer_id=sender_email,
                        primary_email=sender_email,
                        name=parsed_email.get('from_name', ''),
                        plan_type="free"
                    )
                    session.add(customer)
                    await session.flush()
                    logger.info(f"Created new customer: {sender_email}")

                # Create conversation
                import time
                from datetime import datetime
                conversation_id = f"email_{sender_email}_{int(time.time())}_{email_id[-6:]}"  # Include part of email_id to make more unique
                conversation = Conversation(
                    conversation_id=conversation_id,
                    customer_id=customer.customer_id,
                    channel=ChannelType.EMAIL,  # This ensures channel is "email" in dashboard
                    subject=subject,
                    status=ConversationStatus.OPEN
                )
                session.add(conversation)
                await session.flush()

                # Create initial message - handle case where body might be None/empty
                message_body = body or "No content found in email"
                message_id_db = f"msg_{conversation_id}_0"
                message = Message(
                    message_id=message_id_db,
                    conversation_id=conversation_id,
                    sender="customer",
                    channel=ChannelType.EMAIL,
                    content=message_body,
                    sentiment=None  # Will be analyzed by agent
                )
                session.add(message)

                # Update customer stats
                customer.total_conversations += 1
                customer.total_messages += 1
                customer.last_contact_date = datetime.utcnow()

                await session.commit()

                logger.info(f"Email processed into conversation: {conversation_id}")

                # Process the inquiry with agent
                agent_service = AgentService(session)
                response = await agent_service.process_inquiry(
                    customer_id=sender_email,
                    channel=ChannelType.EMAIL,
                    message_content=body,
                    subject=subject,
                    thread_id=thread_id  # Pass thread ID for email continuity
                )

                logger.info(
                    f"Email inquiry processed: {conversation_id}, "
                    f"escalated={response.should_escalate}, "
                    f"sentiment={response.sentiment_score:.2f}"
                )

                # Update conversation status to reflect resolution
                if not response.should_escalate:
                    conversation.status = ConversationStatus.RESOLVED
                    await session.commit()
                    logger.info(f"Conversation {conversation_id} marked as resolved after processing")
                else:
                    conversation.status = ConversationStatus.ESCALATED
                    await session.commit()
                    logger.info(f"Conversation {conversation_id} marked as escalated")

        except Exception as e:
            logger.error(f"Error processing single email: {e}", exc_info=True)
            # Re-raise the exception so the caller knows this email failed
            raise