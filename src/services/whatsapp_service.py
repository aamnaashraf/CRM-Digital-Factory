"""
WhatsApp Service
Handles Twilio WhatsApp integration for message sending and webhook validation
"""

from typing import Optional
from twilio.rest import Client
from twilio.request_validator import RequestValidator
import logging
import os

from src.config_simple import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class WhatsAppService:
    """
    Service for handling WhatsApp integration with Twilio
    """

    def __init__(self):
        """
        Initialize WhatsApp service with Twilio client
        """
        if not settings.twilio_account_sid or not settings.twilio_auth_token:
            logger.warning("Twilio credentials not configured - WhatsApp functionality disabled")
            self.client = None
            self.validator = None
        else:
            self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            self.validator = RequestValidator(settings.twilio_auth_token)
            logger.info("WhatsApp service initialized with Twilio client")

    def send_message(self, to_number: str, message: str) -> Optional[dict]:
        """
        Send WhatsApp message via Twilio

        Args:
            to_number: Recipient phone number in format +1234567890 or whatsapp:+1234567890
            message: Message content to send

        Returns:
            Message SID if successful, None if failed
        """
        if not self.client:
            logger.error("Twilio client not initialized - could not send WhatsApp message")
            return None

        try:
            # Normalize the to_number to ensure it has the whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                # If it looks like a phone number, add the whatsapp: prefix
                if to_number.startswith('+') or to_number.replace('-', '').replace(' ', '').isdigit():
                    to_number = f"whatsapp:{to_number}"
                else:
                    # It might already be in the right format but missing the prefix
                    # Check if it's already in the right format but just missing 'whatsapp:'
                    to_number = f"whatsapp:{to_number}"

            # Use the configured WhatsApp number as the sender
            from_number = settings.twilio_whatsapp_number
            if not from_number:
                logger.error("Twilio WhatsApp number not configured")
                return None

            if not from_number.startswith('whatsapp:'):
                from_number = f"whatsapp:{from_number}"

            logger.info(f"Sending WhatsApp message from {from_number} to {to_number}")

            # Send the WhatsApp message
            twilio_message = self.client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )

            logger.info(f"WhatsApp message sent successfully: {twilio_message.sid} to {to_number}")
            return {
                'sid': twilio_message.sid,
                'status': twilio_message.status,
                'to': to_number,
                'from': from_number
            }

        except Exception as e:
            logger.error(f"Failed to send WhatsApp message to {to_number}: {e}", exc_info=True)
            logger.error(f"Error details: to_number='{to_number}', from_number='{from_number}', message_length={len(message)}")
            return None

    def validate_webhook(self, request_url: str, form_data: dict, signature: str) -> bool:
        """
        Validate incoming webhook request signature from Twilio

        Args:
            request_url: Full URL of the incoming request
            form_data: Form data from the request
            signature: X-Twilio-Signature header value

        Returns:
            True if signature is valid, False otherwise
        """
        if not self.validator:
            logger.error("Twilio validator not initialized")
            return False

        try:
            is_valid = self.validator.validate(
                request_url,
                form_data,
                signature
            )
            return is_valid
        except Exception as e:
            logger.error(f"Error validating webhook signature: {e}", exc_info=True)
            return False

# Global instance
whatsapp_service = WhatsAppService()


def format_whatsapp_response(response_text: str) -> str:
    """
    Format response text appropriately for WhatsApp channel
    Keep responses casual, conversational, and concise

    Args:
        response_text: Raw response from agent

    Returns:
        Formatted response suitable for WhatsApp
    """
    # Remove any HTML tags that might be in email responses
    import re
    clean_text = re.sub(r'<[^>]+>', '', response_text)

    # Clean up extra whitespace but preserve line breaks
    # First replace multiple spaces/tabs with single space
    clean_text = re.sub(r'[ \t]+', ' ', clean_text)
    # Then normalize multiple newlines to single newlines
    clean_text = re.sub(r'\n\s*\n', '\n', clean_text)

    # Remove leading/trailing whitespace
    clean_text = clean_text.strip()

    # Ensure response is appropriately concise for WhatsApp
    # WhatsApp messages have a 1600 character limit per message
    if len(clean_text) > 1500:  # Leave some buffer
        clean_text = clean_text[:1500] + "..."

    # Remove formal email signatures if present
    lines = clean_text.split('\n')
    # Remove lines that look like formal signatures
    filtered_lines = []
    for line in lines:
        line = line.strip()
        if line and not any(phrase in line.lower() for phrase in [
            'best regards', 'sincerely', 'thank you', 'this is an automated response',
            'do not reply', 'customer success team', 'support team'
        ]):
            filtered_lines.append(line)

    formatted_response = '\n'.join(filtered_lines).strip()

    return formatted_response

    return formatted_response