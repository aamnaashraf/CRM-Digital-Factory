"""
Agent Service
Orchestrates agent processing with database and messaging
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import logging
from datetime import datetime

from src.database.models import (
    Customer, Conversation, Message, Escalation,
    ChannelType, ConversationStatus, EscalationReason
)
from src.agent.production_agent import ProductionAgent, AgentContext, AgentResponse
from src.messaging import get_producer
from .gmail_service import gmail_service

logger = logging.getLogger(__name__)


class AgentService:
    """
    Service layer for agent operations

    Coordinates between database, agent, and messaging
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize agent service

        Args:
            session: Database session
        """
        self.session = session
        self.agent = ProductionAgent(session)
        self.producer = get_producer()

    async def process_inquiry(
        self,
        customer_id: str,
        channel: ChannelType,
        message_content: str,
        subject: str = "",
        thread_id: Optional[str] = None,  # Add thread_id parameter for email continuity
        existing_conversation_id: Optional[str] = None  # Allow specifying existing conversation
    ) -> AgentResponse:
        """
        Process customer inquiry end-to-end

        Args:
            customer_id: Customer email or phone
            channel: Communication channel
            message_content: Customer message
            subject: Message subject (optional)
            thread_id: Thread ID for email continuity (optional)
            existing_conversation_id: ID of existing conversation to use (optional)

        Returns:
            AgentResponse with generated response
        """
        try:
            # Step 1: Get or create customer
            customer = await self._get_or_create_customer(customer_id, channel)

            # Step 2: Get or create conversation
            if existing_conversation_id:
                # Use existing conversation if provided
                result = await self.session.execute(
                    select(Conversation)
                    .where(Conversation.conversation_id == existing_conversation_id)
                )
                conversation = result.scalar_one_or_none()
                if not conversation:
                    # Fallback to creating if not found
                    conversation = await self._get_or_create_conversation(
                        customer.customer_id,
                        channel,
                        subject
                    )
            else:
                # Normal get or create behavior
                conversation = await self._get_or_create_conversation(
                    customer.customer_id,
                    channel,
                    subject
                )

            # Step 3: Save customer message
            await self._save_message(
                conversation.conversation_id,
                sender="customer",
                channel=channel,
                content=message_content,
                sentiment=None  # Will be analyzed by agent
            )

            # Step 4: Get conversation history
            history = await self._get_conversation_history(conversation.conversation_id)

            # Step 5: Build agent context
            context = AgentContext(
                customer_id=customer.customer_id,
                customer_name=customer.name,
                channel=channel,
                message=message_content,
                subject=subject,
                conversation_history=history,
                customer_profile=customer
            )

            # Step 6: Process with agent
            response = await self.agent.process_message(context)

            # Step 7: Save agent response
            await self._save_message(
                conversation.conversation_id,
                sender="agent",
                channel=channel,
                content=response.response_text,
                sentiment=response.sentiment_score
            )

            # Step 8: Handle escalation if needed
            if response.should_escalate:
                await self._escalate_conversation(
                    conversation,
                    response.escalation_reason
                )

            # Step 9: Update customer stats
            await self._update_customer_stats(customer, response.sentiment_score)

            # Step 10: Update conversation status and send response
            if response.should_escalate:
                # Status is already updated in _escalate_conversation
                logger.info(f"Conversation {conversation.conversation_id} escalated, status already updated")
            else:
                # Update conversation status to resolved if not escalated
                conversation.status = ConversationStatus.RESOLVED
                logger.info(f"Conversation {conversation.conversation_id} marked as resolved")

            # Commit the status update before attempting to send response
            await self.session.commit()

            logger.info(f"Attempting to send response for conversation {conversation.conversation_id}, channel: {channel.value}")

            try:
                await self._send_response(
                    customer_id,
                    channel,
                    subject,
                    response.response_text,
                    thread_id=thread_id  # Pass thread ID for email continuity
                )
                logger.info(f"Response successfully sent for conversation {conversation.conversation_id}")
            except Exception as e:
                # Log the error but the status has already been updated
                logger.error(f"Failed to send response via {channel.value} for conversation {conversation.conversation_id}, but status is already updated: {e}")
                # Status is already committed, so we don't raise the exception
                # to allow normal flow to continue

            # Step 11: Publish response to Kafka
            self._publish_response(
                customer_id,
                conversation.conversation_id,
                channel,
                response
            )

            await self.session.commit()

            logger.info(
                f"Inquiry processed: customer={customer_id}, "
                f"conversation={conversation.conversation_id}, "
                f"escalated={response.should_escalate}, "
                f"status={conversation.status}, "
                f"channel={channel.value}"
            )

            return response

        except Exception as e:
            logger.error(f"Inquiry processing error: {e}", exc_info=True)
            await self.session.rollback()
            raise

    async def _get_or_create_customer(
        self,
        customer_id: str,
        channel: ChannelType
    ) -> Customer:
        """Get existing customer or create new one"""

        # Determine if this is an email or phone number
        is_email = '@' in customer_id

        if is_email:
            # For email channels, find by primary_email
            result = await self.session.execute(
                select(Customer).where(Customer.primary_email == customer_id)
            )
        else:
            # For WhatsApp channels, normalize the phone number and search for various formats
            # Remove 'whatsapp:' prefix and '+' for matching
            normalized_customer_id = customer_id.replace('whatsapp:', '').replace('+', '').strip()

            result = await self.session.execute(
                select(Customer).where(
                    (Customer.phone_number == customer_id) |
                    (Customer.phone_number == f"whatsapp:{normalized_customer_id}") |
                    (Customer.phone_number == f"whatsapp:+{normalized_customer_id}") |
                    (Customer.phone_number == f"+{normalized_customer_id}") |
                    (Customer.phone_number == normalized_customer_id) |
                    (Customer.customer_id == normalized_customer_id) |
                    (Customer.customer_id == f"whatsapp:{normalized_customer_id}") |
                    (Customer.customer_id == f"+{normalized_customer_id}")
                )
            )

        customer = result.scalar_one_or_none()

        if not customer:
            # If creating a new customer from WhatsApp, ensure we use the normalized format for customer_id
            final_customer_id = customer_id.replace('whatsapp:', '').replace('+', '').strip() if not is_email else customer_id

            customer = Customer(
                customer_id=final_customer_id,
                primary_email=customer_id if is_email else None,
                phone_number=customer_id if not is_email else None,  # Store with original format
                name="",
                plan_type="free"
            )
            self.session.add(customer)
            await self.session.flush()

            logger.info(f"Created new customer: {customer_id} with customer_id: {final_customer_id}")

        return customer

    async def _get_or_create_conversation(
        self,
        customer_id: str,
        channel: ChannelType,
        subject: str
    ) -> Conversation:
        """Get active conversation or create new one"""
        # Look for open conversation
        result = await self.session.execute(
            select(Conversation).where(
                Conversation.customer_id == customer_id,
                Conversation.channel == channel,
                Conversation.status.in_([ConversationStatus.OPEN, ConversationStatus.PENDING])
            ).order_by(Conversation.updated_at.desc())  # Get the most recent one
        )
        # Use scalar() which returns the first result or None, avoiding MultipleResultsFound error
        conversation = result.scalar()

        if not conversation:
            conversation_id = f"conv_{customer_id}_{int(datetime.utcnow().timestamp())}"

            conversation = Conversation(
                conversation_id=conversation_id,
                customer_id=customer_id,
                channel=channel,
                subject=subject,
                status=ConversationStatus.OPEN
            )
            self.session.add(conversation)
            await self.session.flush()

            logger.info(f"Created new conversation: {conversation_id}")

        return conversation

    async def _save_message(
        self,
        conversation_id: str,
        sender: str,
        channel: ChannelType,
        content: str,
        sentiment: Optional[float]
    ) -> Message:
        """Save message to database"""
        # Count existing messages
        result = await self.session.execute(
            select(Message).where(Message.conversation_id == conversation_id)
        )
        message_count = len(result.scalars().all())

        message_id = f"msg_{conversation_id}_{message_count}"

        # Ensure content is not None to avoid database constraint errors
        message_content = content or "No content provided"
        message = Message(
            message_id=message_id,
            conversation_id=conversation_id,
            sender=sender,
            channel=channel,
            content=message_content,
            sentiment=sentiment
        )
        self.session.add(message)
        await self.session.flush()

        return message

    async def _get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 10
    ) -> list:
        """Get recent conversation history"""
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp.desc())
            .limit(limit)
        )
        messages = result.scalars().all()

        # Reverse to chronological order
        return [
            {
                'sender': msg.sender,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            }
            for msg in reversed(messages)
        ]

    async def _escalate_conversation(
        self,
        conversation: Conversation,
        reason: EscalationReason
    ):
        """Escalate conversation to human agent"""
        conversation.escalated = True
        conversation.escalation_reason = reason.value
        conversation.status = ConversationStatus.ESCALATED

        # Create escalation record
        escalation = Escalation(
            conversation_id=conversation.conversation_id,
            reason=reason,
            target_team=self._get_target_team(reason),
            urgency="immediate" if reason in [
                EscalationReason.CHURN_THREAT,
                EscalationReason.SECURITY,
                EscalationReason.BILLING
            ] else "high",
            notes=f"Auto-escalated by AI agent: {reason.value}"
        )
        self.session.add(escalation)

        # Update customer escalation count
        result = await self.session.execute(
            select(Customer).where(Customer.customer_id == conversation.customer_id)
        )
        customer = result.scalar_one()
        customer.escalation_count += 1

        logger.info(
            f"Escalated conversation: {conversation.conversation_id}, "
            f"reason={reason.value}"
        )

    def _get_target_team(self, reason: EscalationReason) -> str:
        """Get target team for escalation"""
        team_map = {
            EscalationReason.BILLING: "billing",
            EscalationReason.SECURITY: "security",
            EscalationReason.LEGAL: "legal",
            EscalationReason.COMPLIANCE: "compliance",
            EscalationReason.ENTERPRISE_SALES: "sales",
            EscalationReason.TECHNICAL: "engineering",
            EscalationReason.CHURN_THREAT: "customer_success",
            EscalationReason.BUG_REPORT: "engineering"
        }
        return team_map.get(reason, "support")

    async def _update_customer_stats(self, customer: Customer, sentiment: float):
        """Update customer statistics"""
        customer.total_messages += 1
        customer.last_contact_date = datetime.utcnow()

        # Update average sentiment
        if customer.average_sentiment == 0.0:
            customer.average_sentiment = sentiment
        else:
            # Running average
            total = customer.total_messages
            customer.average_sentiment = (
                (customer.average_sentiment * (total - 1) + sentiment) / total
            )

    async def _send_response(
        self,
        customer_id: str,
        channel: ChannelType,
        subject: str,
        response_text: str,
        thread_id: Optional[str] = None
    ):
        """Send response via appropriate channel"""
        try:
            logger.info(f"Attempting to send response via channel: {channel.value} to customer: {customer_id}")

            if channel == ChannelType.EMAIL:
                # Send response via Gmail
                await self._send_email_response(customer_id, subject, response_text, thread_id)
                logger.info(f"Email response sent successfully to: {customer_id}, thread_id: {thread_id}")
            elif channel == ChannelType.WHATSAPP:
                # Send response via WhatsApp
                await self._send_whatsapp_response(customer_id, response_text)
                logger.info(f"WhatsApp response sent successfully to: {customer_id}")
            else:
                # Other channels can be implemented here
                logger.info(f"Response sent via channel {channel.value}: {response_text[:100]}...")
        except Exception as e:
            logger.error(f"Failed to send response via {channel.value} to {customer_id}: {e}", exc_info=True)
            raise

    async def _send_email_response(
        self,
        to_email: str,
        subject: str,
        response_text: str,
        thread_id: Optional[str] = None
    ):
        """Send email response via Gmail API"""
        logger.info(f"Preparing to send email response to: {to_email}, thread_id: {thread_id}")

        try:
            # Create appropriate subject if not provided
            email_subject = subject if subject else "Response to your support request"

            # Add formal email signature for email channel with proper greeting
            full_response = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .email-container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
                    .content {{ padding: 20px 0; }}
                    .footer {{ font-size: 12px; color: #666; padding-top: 20px; border-top: 1px solid #eee; }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">
                        <h2>TaskFlow Support Response</h2>
                    </div>
                    <div class="content">
                        <p>Dear Customer,</p>
                        <p>Thank you for reaching out to TaskFlow support. Here is the response to your inquiry:</p>
                        <p><strong>{response_text}</strong></p>
                        <p>If you have any additional questions, please feel free to reach out.</p>
                    </div>
                    <div class="footer">
                        <p>Best regards,<br>
                        TaskFlow Customer Success Team</p>
                        <p><em>This is an automated response. Please do not reply directly to this email.</em></p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Send the email with thread ID if available
            result = gmail_service.send_email(
                to=to_email,
                subject=email_subject,
                body=full_response,
                thread_id=thread_id  # Use thread ID if provided for continuity
            )

            logger.info(f"Email response sent successfully to {to_email}, message ID: {result.get('id', 'unknown')}, thread_id: {thread_id}")

        except Exception as e:
            logger.error(f"Failed to send email response to {to_email}: {e}", exc_info=True)
            # Re-raise to be caught by the calling method
            raise

    async def _send_whatsapp_response(
        self,
        to_number: str,
        response_text: str
    ):
        """Send WhatsApp response via Twilio API"""
        from .whatsapp_service import whatsapp_service, format_whatsapp_response

        logger.info(f"Preparing to send WhatsApp response to: {to_number}")

        try:
            # Format the response appropriately for WhatsApp (casual, conversational)
            formatted_response = format_whatsapp_response(response_text)
            logger.info(f"Sending formatted WhatsApp response: {formatted_response[:100]}...")

            # Send the WhatsApp message via Twilio
            result = whatsapp_service.send_message(to_number, formatted_response)

            if result:
                logger.info(f"WhatsApp response sent successfully to {to_number}, message SID: {result.get('sid')}")
            else:
                logger.error(f"Failed to send WhatsApp response to {to_number}")
                raise Exception(f"Failed to send WhatsApp message to {to_number}")

        except Exception as e:
            logger.error(f"Failed to send WhatsApp response to {to_number}: {e}", exc_info=True)
            # Re-raise to be caught by the calling method
            raise

    def _publish_response(
        self,
        customer_id: str,
        conversation_id: str,
        channel: ChannelType,
        response: AgentResponse
    ):
        """Publish response to Kafka for delivery"""
        try:
            self.producer.publish_response(
                customer_id,
                {
                    'conversation_id': conversation_id,
                    'channel': channel.value,
                    'response_text': response.response_text,
                    'escalated': response.should_escalate,
                    'sentiment_score': response.sentiment_score,
                    'processing_time_ms': response.processing_time_ms
                }
            )
        except Exception as e:
            logger.error(f"Failed to publish response to Kafka: {e}")
            # Don't fail the request if Kafka publish fails
