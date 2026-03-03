"""
Webhook Endpoints
Receive messages from Gmail and WhatsApp
"""

from fastapi import APIRouter, Request, HTTPException, status, BackgroundTasks, Depends
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel, Field
from typing import Optional
import logging
import json
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from twilio.twiml.messaging_response import MessagingResponse

# Use simplified config by default for local development
# This allows switching between configurations without code changes
import os
if os.getenv('USE_SIMPLE_CONFIG', 'true').lower() == 'true':
    from src.config_simple import get_settings
else:
    from src.config import get_settings

from src.database.connection import get_db_session
from src.database.models import Customer, Conversation, Message, ChannelType, ConversationStatus

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


class GmailPubSubMessage(BaseModel):
    """Gmail Pub/Sub notification"""
    message: dict
    subscription: str


class WhatsAppMessage(BaseModel):
    """Twilio WhatsApp incoming message"""
    From: str = Field(..., description="Sender phone number")
    To: str = Field(..., description="Recipient phone number")
    Body: str = Field(..., description="Message content")
    MessageSid: str = Field(..., description="Message ID")
    NumMedia: Optional[str] = Field(default="0", description="Number of media attachments")


@router.get("/test")
async def test_endpoint():
    """
    Simple test endpoint to verify ngrok/backend is working
    """
    logger.info("Test endpoint hit successfully!")
    return {"status": "OK", "message": "Test endpoint working"}


@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Receive WhatsApp messages from Twilio

    When a customer sends a WhatsApp message, Twilio forwards it
    to this endpoint. We process it and send a response.
    """
    try:
        # Added explicit print statements as requested
        from datetime import datetime
        print(f"WhatsApp webhook HIT at {datetime.now()}")

        logger.info("WhatsApp webhook hit!")

        # Parse form data (Twilio sends as form-encoded)
        form_data = await request.form()

        # More explicit prints as requested
        from_number = form_data.get('From', 'N/A')
        body = form_data.get('Body', 'N/A')
        print(f"From: {from_number}")
        print(f"Body: {body}")
        print(f"All request values: {dict(form_data)}")
        print(f"Signature: {request.headers.get('X-Twilio-Signature', 'N/A')}")

        logger.info(f"From: {form_data.get('From', 'N/A')}")
        logger.info(f"Body: {form_data.get('Body', 'N/A')}")
        logger.info(f"All values: {dict(form_data)}")
        logger.info(f"Signature: {request.headers.get('X-Twilio-Signature', 'N/A')}")

        # Get the Twilio signature for validation
        signature = request.headers.get("X-Twilio-Signature", "")
        request_url = str(request.url)

        # Convert form data to dict for validation
        form_dict = {}
        for field, value in form_data.items():
            form_dict[field] = value

        logger.info(f"Twilio signature from header: {signature}")
        logger.info(f"Request URL for validation: {request_url}")
        logger.info(f"Form data for validation: {form_dict}")

        # TEMPORARILY DISABLE signature validation for testing
        from src.services.whatsapp_service import whatsapp_service
        # Temporarily disable validation to make sure it's not blocking webhook hits
        print(f"Signature validation temporarily disabled for testing")
        # is_valid = False  # Set to False to bypass validation during testing
        # if settings.twilio_auth_token and signature:  # Only validate if token and signature are provided
        #     is_valid = whatsapp_service.validate_webhook(request_url, form_dict, signature)
        #     logger.info(f"Webhook signature validation result: {is_valid}")
        #     if not is_valid:
        #         logger.warning(f"Invalid webhook signature: {signature}, but continuing for testing...")
        #         print(f"Invalid signature: {signature}")
        #         # Return 403 for invalid signature in production
        #         return PlainTextResponse(content="", status_code=403)
        # else:
        #     logger.warning("Skipping webhook signature validation (no auth token or signature)")
        #     print("Skipping signature validation")

        # Extract message details
        from_number = form_data.get("From", "")
        to_number = form_data.get("To", "")
        body = form_data.get("Body", "")
        message_sid = form_data.get("MessageSid", "")

        logger.info(f"Extracted from_number: {from_number}")
        logger.info(f"Extracted to_number: {to_number}")
        logger.info(f"Extracted body: {body}")
        logger.info(f"Extracted message_sid: {message_sid}")

        logger.info(f"WhatsApp message from {from_number}: {body[:50]}...")

        # Validate it's to our WhatsApp number
        # Normalize both numbers for comparison (remove 'whatsapp:' prefix, '+' signs, and whitespace)
        normalized_to_number = to_number.replace('whatsapp:', '').replace('+', '').strip()
        normalized_expected_number = settings.twilio_whatsapp_number.replace('whatsapp:', '').replace('+', '').strip()

        if settings.twilio_whatsapp_number and normalized_to_number != normalized_expected_number:
            logger.warning(f"Message to unknown number: {to_number}, normalized: '{normalized_to_number}', expected: {settings.twilio_whatsapp_number}, normalized: '{normalized_expected_number}'")
            # Return minimal XML response that Twilio expects
            return Response(
                content="<?xml version='1.0' encoding='UTF-8'?><Response></Response>",
                media_type="application/xml",
                headers={"Content-Type": "text/xml; charset=utf-8"}
            )

        # Check if this is a test message - Added immediate test reply as requested
        if body.lower().strip() in ["test", "hi", "hello", "hey"]:
            logger.info("Test message detected, sending test response")
            test_response = f"AI test reply working! 😊 Your query: {body}"
            print(f"Immediate test reply sent: {test_response}")

            # Use the existing WhatsApp service to send the reply
            from src.services.whatsapp_service import whatsapp_service
            result = whatsapp_service.send_message(from_number, test_response)

            if result:
                print(f"Reply sent! Message SID: {result['sid']}")
                logger.info(f"Immediate test reply sent successfully: {result['sid']}")
            else:
                print("Failed to send reply via WhatsApp service")
                logger.error("Failed to send immediate test reply via WhatsApp service")

            # Return empty response since we've already sent the reply via Twilio
            # But return minimal XML for Twilio compatibility
            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response></Response>"""

            return Response(
                content=response_xml,
                media_type="application/xml",
                headers={"Content-Type": "text/xml; charset=utf-8"}
            )

        # Process in background
        logger.info(f"Queueing background task for message: {message_sid}")
        background_tasks.add_task(
            process_whatsapp_message,
            from_number,
            body,
            message_sid
        )

        logger.info(f"Background task queued successfully for message: {message_sid}")
        print("After processing: reply sent or error")

        # Return immediate response to Twilio - this is what they'll send back to the user
        # Use explicit XML content to ensure no FastAPI JSON conversion happens
        # For better compatibility with Twilio, we'll return an empty response since
        # we're handling the reply asynchronously with the background task
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response></Response>"""

        return Response(
            content=xml_response,
            media_type="application/xml",
            headers={"Content-Type": "text/xml; charset=utf-8"}
        )

    except HTTPException as http_err:
        logger.error(f"HTTP exception in WhatsApp webhook: {http_err.detail}")
        # Re-raise HTTP exceptions (like 403 for invalid signature)
        raise
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {e}", exc_info=True)
        # Return a minimal response that Twilio expects
        error_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>We're experiencing technical difficulties. Please try again later.</Message>
</Response>"""
        return Response(
            content=error_response,
            media_type="application/xml",
            headers={"Content-Type": "text/xml; charset=utf-8"}
        )


async def process_gmail_notification(email_address: str, history_id: str):
    """
    Process Gmail notification in background
    Fetches email content using Gmail API and creates ticket for agent processing
    """
    try:
        from src.services.gmail_service import gmail_service
        from src.database.connection import get_db_manager
        from src.services.agent_service import AgentService

        logger.info(f"Processing Gmail notification: {email_address}, history: {history_id}")

        # Get Gmail service to fetch the specific message
        service = gmail_service.get_service()

        # If we get a message ID as the history_id (common in webhook notifications)
        if len(history_id) > 20:  # Assume it's a message ID if longer than typical history ID
            # Treat it as a message ID directly
            try:
                full_message = service.users().messages().get(
                    userId='me',
                    id=history_id
                ).execute()

                # Process just this single message
                parsed_email = gmail_service.parse_email(full_message)
                sender_email = parsed_email.get('from_email')
                subject = parsed_email.get('subject', '')
                body = parsed_email.get('body', parsed_email.get('snippet', ''))

                if not sender_email:
                    logger.warning(f"No sender email found in message: {history_id}")
                    return

                logger.info(f"Processing email from {sender_email} with subject '{subject}'")

                # Get database session and process the email
                db = get_db_manager()
                async with db.get_session() as session:
                    # Get or create customer
                    from sqlalchemy import select
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

                    # Extract thread ID from parsed email
                    thread_id = parsed_email.get('thread_id', None)

                    # Create conversation with specific ID format for email processing
                    import time
                    from datetime import datetime
                    conversation_id = f"email_{sender_email}_{int(time.time())}"
                    conversation = Conversation(
                        conversation_id=conversation_id,
                        customer_id=customer.customer_id,
                        channel=ChannelType.EMAIL,
                        subject=subject,
                        status=ConversationStatus.OPEN,
                        metadata={"thread_id": thread_id} if thread_id else {}  # Store thread ID if available
                    )
                    session.add(conversation)
                    await session.flush()

                    # Create initial message
                    message_id_db = f"msg_{conversation_id}_0"
                    message = Message(
                        message_id=message_id_db,
                        conversation_id=conversation_id,
                        sender="customer",
                        channel=ChannelType.EMAIL,
                        content=body,
                        sentiment=None,  # Will be analyzed by agent
                        metadata={"thread_id": thread_id} if thread_id else {}  # Store thread ID if available
                    )
                    session.add(message)

                    # Update customer stats
                    customer.total_conversations += 1
                    customer.total_messages += 1
                    customer.last_contact_date = datetime.utcnow()

                    # Mark the email as read in Gmail before committing
                    gmail_service.mark_as_read(history_id)

                    # Commit changes
                    await session.commit()

                    logger.info(f"Email processed into conversation: {conversation_id}")

                    # Now call the agent service to process the inquiry
                    # The agent service should use the existing conversation
                    agent_service = AgentService(session)

                    # Get the conversation again to ensure it's fresh
                    result = await session.execute(
                        select(Conversation).where(Conversation.conversation_id == conversation_id)
                    )
                    existing_conversation = result.scalar_one_or_none()

                    if existing_conversation:
                        # Process with agent, using the existing conversation ID
                        response = await agent_service.process_inquiry(
                            customer_id=sender_email,
                            channel=ChannelType.EMAIL,
                            message_content=body,
                            subject=subject,
                            thread_id=parsed_email.get('thread_id'),  # Pass thread ID for email continuity
                            existing_conversation_id=conversation_id  # Use the existing conversation
                        )

                        # Get the conversation again to check status after agent processing
                        result = await session.execute(
                            select(Conversation).where(Conversation.conversation_id == conversation_id)
                        )
                        updated_conversation = result.scalar_one_or_none()

                        # Final check and update if needed
                        if updated_conversation:
                            if response.should_escalate and not updated_conversation.escalated:
                                updated_conversation.status = ConversationStatus.ESCALATED
                                updated_conversation.escalated = True
                            elif not response.should_escalate and updated_conversation.status != ConversationStatus.RESOLVED:
                                # Update to RESOLVED status after successful response generation
                                updated_conversation.status = ConversationStatus.RESOLVED

                        await session.commit()
                        logger.info(
                            f"Email inquiry processed: {conversation_id}, "
                            f"status={updated_conversation.status if updated_conversation else 'unknown'}, "
                            f"escalated={response.should_escalate}, "
                            f"sentiment={response.sentiment_score:.2f}"
                        )
                    else:
                        logger.error(f"Conversation {conversation_id} not found for agent processing")

                    logger.info(
                        f"Email inquiry processed: {conversation_id}, "
                        f"escalated={response.should_escalate}, "
                        f"sentiment={response.sentiment_score:.2f}"
                    )
            except Exception as e:
                logger.error(f"Error processing specific message {history_id}: {e}", exc_info=True)
        else:
            # Use history API to get messages (original approach)
            try:
                results = service.users().history().list(
                    userId='me',
                    startHistoryId=history_id,
                    historyTypes=['messageAdded']
                ).execute()

                if 'history' in results:
                    for history_record in results['history']:
                        if 'messagesAdded' in history_record:
                            for message_added in history_record['messagesAdded']:
                                msg = message_added['message']
                                message_id = msg['id']

                                # Get the full message
                                full_message = service.users().messages().get(
                                    userId='me',
                                    id=message_id
                                ).execute()

                                # Parse the email content
                                parsed_email = gmail_service.parse_email(full_message)

                                sender_email = parsed_email.get('from_email')
                                subject = parsed_email.get('subject', '')
                                body = parsed_email.get('body', parsed_email.get('snippet', ''))

                                if not sender_email:
                                    logger.warning(f"No sender email found in message: {message_id}")
                                    continue

                                logger.info(f"Processing email from {sender_email} with subject '{subject}'")

                                # Get database session and process the email
                                db = get_db_manager()
                                async with db.get_session() as session:
                                    # Get or create customer
                                    from sqlalchemy import select
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

                                    # Create conversation with specific ID format for email processing
                                    import time
                                    from datetime import datetime
                                    conversation_id = f"email_{sender_email}_{int(time.time())}"
                                    conversation = Conversation(
                                        conversation_id=conversation_id,
                                        customer_id=customer.customer_id,
                                        channel=ChannelType.EMAIL,
                                        subject=subject,
                                        status=ConversationStatus.OPEN
                                    )
                                    session.add(conversation)
                                    await session.flush()

                                    # Create initial message
                                    message_id_db = f"msg_{conversation_id}_0"
                                    message = Message(
                                        message_id=message_id_db,
                                        conversation_id=conversation_id,
                                        sender="customer",
                                        channel=ChannelType.EMAIL,
                                        content=body,
                                        sentiment=None  # Will be analyzed by agent
                                    )
                                    session.add(message)

                                    # Update customer stats
                                    customer.total_conversations += 1
                                    customer.total_messages += 1
                                    customer.last_contact_date = datetime.utcnow()

                                    # Mark the email as read in Gmail before committing
                                    gmail_service.mark_as_read(message_id)

                                    # Commit changes
                                    await session.commit()

                                    logger.info(f"Email processed into conversation: {conversation_id}")

                                    # Now call the agent service to process the inquiry
                                    # The agent service should use the existing conversation
                                    agent_service = AgentService(session)

                                    # Get the conversation again to ensure it's fresh
                                    result = await session.execute(
                                        select(Conversation).where(Conversation.conversation_id == conversation_id)
                                    )
                                    existing_conversation = result.scalar_one_or_none()

                                    if existing_conversation:
                                        # Process with agent, using the existing conversation ID
                                        response = await agent_service.process_inquiry(
                                            customer_id=sender_email,
                                            channel=ChannelType.EMAIL,
                                            message_content=body,
                                            subject=subject,
                                            thread_id=parsed_email.get('thread_id'),  # Pass thread ID for email continuity
                                            existing_conversation_id=conversation_id  # Use the existing conversation
                                        )

                                        # Get the conversation again to check status after agent processing
                                        result = await session.execute(
                                            select(Conversation).where(Conversation.conversation_id == conversation_id)
                                        )
                                        updated_conversation = result.scalar_one_or_none()

                                        # Final check and update if needed
                                        if updated_conversation:
                                            if response.should_escalate and not updated_conversation.escalated:
                                                updated_conversation.status = ConversationStatus.ESCALATED
                                                updated_conversation.escalated = True
                                            elif not response.should_escalate and updated_conversation.status != ConversationStatus.RESOLVED:
                                                # Update to RESOLVED status after successful response generation
                                                updated_conversation.status = ConversationStatus.RESOLVED

                                        await session.commit()
                                        logger.info(
                                            f"Email inquiry processed: {conversation_id}, "
                                            f"status={updated_conversation.status if updated_conversation else 'unknown'}, "
                                            f"escalated={response.should_escalate}, "
                                            f"sentiment={response.sentiment_score:.2f}"
                                        )
                                    else:
                                        logger.error(f"Conversation {conversation_id} not found for agent processing")
            except Exception as e:
                logger.error(f"Error in history-based processing: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Error processing Gmail notification: {e}", exc_info=True)


async def process_whatsapp_message(from_number: str, body: str, message_sid: str):
    """
    Process WhatsApp message in background
    1. Normalize message format
    2. Create customer record if not exists
    3. Create conversation with channel="whatsapp"
    4. Create message entry in database
    5. Process with AgentService
    6. Send response back via Twilio
    """
    try:
        from src.database.connection import get_db_manager
        from src.services.agent_service import AgentService
        from sqlalchemy import select

        # Added logging as requested
        print(f"Processing WhatsApp message: {message_sid}, from: {from_number}, body: {body}")

        logger.info(f"Processing WhatsApp message: {message_sid}, from: {from_number}, body: {body}")

        # Get database manager and session
        db = get_db_manager()
        async with db.get_session() as session:
            logger.info(f"Starting database session for message: {message_sid}")

            # Get or create customer - make sure to handle both whatsapp: prefix and raw numbers
            # Normalize the phone number to handle all possible formats (with/without whatsapp:, +, etc.)
            normalized_from_number = from_number.replace('whatsapp:', '').replace('+', '').strip()

            # Also try to find customer using a more robust matching approach
            # This handles potential edge cases where the customer might exist with a different format
            result = await session.execute(
                select(Customer).where(
                    (Customer.phone_number == from_number) |
                    (Customer.phone_number == f"whatsapp:{normalized_from_number}") |
                    (Customer.phone_number == f"whatsapp:+{normalized_from_number}") |
                    (Customer.customer_id == normalized_from_number) |
                    (Customer.customer_id == f"whatsapp:{normalized_from_number}") |
                    (Customer.customer_id == f"+{normalized_from_number}")
                )
            )
            customer = result.scalar_one_or_none()

            if not customer:
                logger.info(f"Creating new customer for: {from_number}")
                # Create new customer with phone number - use normalized number for customer_id to ensure uniqueness
                # Use a consistent format for customer_id (without whatsapp: prefix)
                customer = Customer(
                    customer_id=normalized_from_number,  # Use normalized number as ID (without whatsapp: prefix)
                    phone_number=from_number,  # Store with whatsapp: prefix as received
                    name=form_data.get('ProfileName', ''),  # Use the profile name if available from Twilio
                    plan_type="free"
                )
                session.add(customer)
                await session.flush()
                logger.info(f"Created new customer: {from_number} with customer_id: {normalized_from_number}")
            else:
                logger.info(f"Found existing customer: {customer.customer_id}")

            # Create conversation with specific ID format for WhatsApp
            import time
            from datetime import datetime
            conversation_id = f"whatsapp_{normalized_from_number}_{int(time.time())}"
            logger.info(f"Creating conversation: {conversation_id}")

            conversation = Conversation(
                conversation_id=conversation_id,
                customer_id=customer.customer_id,
                channel=ChannelType.WHATSAPP,
                subject=body[:100] if len(body) > 100 else body,  # Use first 100 chars as subject
                status=ConversationStatus.OPEN
            )
            session.add(conversation)
            await session.flush()

            # Create initial message from customer
            message_id_db = f"msg_{conversation_id}_0"
            logger.info(f"Creating message: {message_id_db}")

            message = Message(
                message_id=message_id_db,
                conversation_id=conversation_id,
                sender="customer",
                channel=ChannelType.WHATSAPP,
                content=body,
                sentiment=None  # Will be analyzed by agent
            )
            session.add(message)

            # Update customer stats
            customer.total_conversations += 1
            customer.total_messages += 1
            customer.last_contact_date = datetime.utcnow()

            # Commit changes
            await session.commit()
            logger.info(f"Database commit successful for conversation: {conversation_id}")

            logger.info(f"WhatsApp message processed into conversation: {conversation_id}")

            # Now call the agent service to process the inquiry
            logger.info(f"Initializing AgentService for conversation: {conversation_id}")
            agent_service = AgentService(session)

            # Get the conversation again to ensure it's fresh
            result = await session.execute(
                select(Conversation).where(Conversation.conversation_id == conversation_id)
            )
            existing_conversation = result.scalar_one_or_none()

            if existing_conversation:
                logger.info(f"Processing inquiry with agent for: {conversation_id}")

                # Process with agent, using the existing conversation ID
                response = await agent_service.process_inquiry(
                    customer_id=normalized_from_number,  # Use normalized number
                    channel=ChannelType.WHATSAPP,
                    message_content=body,
                    subject=body[:100] if len(body) > 100 else body,
                    existing_conversation_id=conversation_id  # Use the existing conversation
                )

                logger.info(f"Agent response generated, should_escalate: {response.should_escalate}")

                # Get the conversation again to check status after agent processing
                result = await session.execute(
                    select(Conversation).where(Conversation.conversation_id == conversation_id)
                )
                updated_conversation = result.scalar_one_or_none()

                # Final check and update if needed
                if updated_conversation:
                    if response.should_escalate and not updated_conversation.escalated:
                        updated_conversation.status = ConversationStatus.ESCALATED
                        updated_conversation.escalated = True
                        logger.info(f"Conversation {conversation_id} escalated")
                    elif not response.should_escalate and updated_conversation.status != ConversationStatus.RESOLVED:
                        # Update to RESOLVED status after successful response generation
                        updated_conversation.status = ConversationStatus.RESOLVED
                        logger.info(f"Conversation {conversation_id} marked as resolved")

                await session.commit()
                logger.info(
                    f"WhatsApp inquiry processed: {conversation_id}, "
                    f"status={updated_conversation.status if updated_conversation else 'unknown'}, "
                    f"escalated={response.should_escalate}, "
                    f"sentiment={response.sentiment_score:.2f}"
                )

                # The agent service will handle sending the response via its _send_response method
                # We don't need to send another response here to avoid duplicates
                logger.info(f"Agent response processed, response will be sent via agent service for {from_number}")
            else:
                logger.error(f"Conversation {conversation_id} not found for agent processing")

    except Exception as e:
        logger.error(f"Error processing WhatsApp message {message_sid}: {e}", exc_info=True)
        logger.error(f"Full traceback:", exc_info=True)
        # Ensure we handle errors gracefully in the background task


@router.post("/gmail/setup-push")
async def setup_gmail_push_notifications():
    """
    Setup Gmail push notifications to enable real-time email processing
    This enables the Gmail API to send notifications to our webhook via Pub/Sub
    """
    try:
        from src.services.gmail_service import gmail_service

        # Enable push notifications to our Pub/Sub topic
        response = gmail_service.enable_push_notifications()

        if response:
            return {
                "status": "success",
                "message": "Gmail push notifications enabled",
                "response": response
            }
        else:
            return {
                "status": "failure",
                "message": "Failed to enable push notifications",
                "using_fallback": "polling"
            }

    except Exception as e:
        logger.error(f"Error setting up Gmail push notifications: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to setup Gmail push notifications: {str(e)}"
        )


# Additional endpoint for polling-based email checking (fallback mechanism)
@router.post("/gmail/poll")
async def poll_gmail_emails(
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Poll Gmail for new emails (fallback method when push notifications aren't available)
    """
    try:
        from src.services.gmail_service import gmail_service

        # Get only inbound emails (from customers, not sent by me)
        inbound_emails = gmail_service.get_inbound_emails(max_results=10)

        logger.info(f"Found {len(inbound_emails)} inbound emails to process")

        for email in inbound_emails:
            # Process in background - pass the message ID as the second parameter
            # The first parameter will be ignored when the ID is treated as a message ID in the updated function
            background_tasks.add_task(
                process_gmail_notification,
                "temp",  # Placeholder - will be ignored when processing message ID
                email.get('id', 'unknown')
            )

        return {
            "status": "success",
            "processed_emails": len(inbound_emails),
            "message": f"Queued {len(inbound_emails)} inbound emails for processing"
        }

    except Exception as e:
        logger.error(f"Error polling Gmail emails: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to poll Gmail emails: {str(e)}"
        )


@router.get("/gmail/poll/status")
async def get_polling_status():
    """
    Get the status of the Gmail polling task
    """
    try:
        from src.main import gmail_polling_task

        if gmail_polling_task:
            return {
                "status": "running" if gmail_polling_task.running else "stopped",
                "poll_interval_seconds": gmail_polling_task.poll_interval,
                "enabled": True
            }
        else:
            return {
                "status": "not_started",
                "poll_interval_seconds": int(os.getenv('POLL_INTERVAL_SECONDS', '60')),
                "enabled": os.getenv('ENABLE_EMAIL_POLLING', 'true').lower() == 'true'
            }
    except Exception as e:
        logger.error(f"Error getting polling status: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get polling status: {str(e)}"
        )