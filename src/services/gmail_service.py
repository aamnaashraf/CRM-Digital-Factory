"""
Gmail Integration Service
Handles OAuth2 authentication, sending emails, and processing incoming emails via Gmail API
"""
import os
import pickle
import base64
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import asyncio
from pathlib import Path

# Use simplified config by default for local development
# This allows switching between configurations without code changes
import os
if os.getenv('USE_SIMPLE_CONFIG', 'true').lower() == 'true':
    from src.config_simple import get_settings
else:
    from src.config import get_settings

logger = logging.getLogger(__name__)

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.send']

class GmailOAuthService:
    """Handles Gmail OAuth2 authentication flow"""

    def __init__(self):
        self.settings = get_settings()
        self.creds = None

    def load_credentials(self) -> Optional[Credentials]:
        """Load existing credentials from token file"""
        token_path = Path(self.settings.gmail_token_file)
        if token_path.exists():
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
                logger.info("Loaded existing Gmail credentials")
                return self.creds
        return None

    def save_credentials(self, credentials: Credentials):
        """Save credentials to token file"""
        token_path = Path(self.settings.gmail_token_file)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(credentials, token)
        logger.info("Saved Gmail credentials to token file")

    def authenticate(self) -> Credentials:
        """Authenticate and return Gmail API credentials"""
        # Load existing credentials
        self.creds = self.load_credentials()

        # If there are no (valid) credentials available, let the user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                logger.info("Refreshing expired Gmail credentials")
                # Refresh the token
                self.creds.refresh(Request())
                self.save_credentials(self.creds)
            else:
                logger.info("Initiating Gmail OAuth2 flow")
                # Run the OAuth2 flow
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.settings.gmail_credentials_file,
                    SCOPES
                )
                # We'll run this in a separate thread for async compatibility
                self.creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                self.save_credentials(self.creds)

        return self.creds

    def get_gmail_service(self):
        """Get authenticated Gmail API service"""
        creds = self.authenticate()
        return build('gmail', 'v1', credentials=creds)


class GmailService:
    """Main service for sending and receiving emails via Gmail API"""

    def __init__(self):
        self.oauth_service = GmailOAuthService()
        self.settings = get_settings()
        self._service = None

    def get_service(self):
        """Get Gmail service instance"""
        if self._service is None:
            self._service = self.oauth_service.get_gmail_service()
        return self._service

    def create_message(self, to: str, subject: str, body: str, sender: Optional[str] = None,
                      cc: Optional[list] = None, bcc: Optional[list] = None,
                      reply_to: Optional[str] = None, thread_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a message for sending via Gmail"""
        if sender is None:
            sender = self.settings.gmail_support_email

        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        message['from'] = sender

        if cc:
            message['cc'] = ', '.join(cc)
        if bcc:
            message['bcc'] = ', '.join(bcc)
        if reply_to:
            message['reply-to'] = reply_to

        # Add body to email
        message.attach(MIMEText(body, 'html' if '<html' in body.lower() else 'plain'))

        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        result = {'raw': raw_message}
        if thread_id:
            result['threadId'] = thread_id

        return result

    def send_email(self, to: str, subject: str, body: str, sender: Optional[str] = None,
                   cc: Optional[list] = None, bcc: Optional[list] = None,
                   reply_to: Optional[str] = None, thread_id: Optional[str] = None) -> Dict[str, Any]:
        """Send an email via Gmail API"""
        try:
            service = self.get_service()
            message = self.create_message(to, subject, body, sender, cc, bcc, reply_to, thread_id)
            sent_message = service.users().messages().send(
                userId="me",
                body=message
            ).execute()

            logger.info(f"Email sent successfully to {to}, message ID: {sent_message['id']}")
            return sent_message
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise

    def get_unread_messages(self, query: str = "is:unread", max_results: int = 10) -> list:
        """Get unread messages from Gmail"""
        try:
            service = self.get_service()
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            detailed_messages = []

            for message in messages:
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id']
                ).execute()

                detailed_messages.append(msg)

            return detailed_messages
        except Exception as e:
            logger.error(f"Error getting unread messages: {e}")
            return []

    def mark_as_read(self, message_id: str):
        """Mark a message as read by removing the UNREAD label"""
        try:
            service = self.get_service()
            # Modify the labels to remove the UNREAD label
            body = {
                'removeLabelIds': ['UNREAD'],
                'addLabelIds': []
            }
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body=body
            ).execute()
        except Exception as e:
            logger.error(f"Error marking message as read: {e}")

    def parse_email(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a Gmail message to extract relevant information"""
        headers = message.get('payload', {}).get('headers', [])

        email_data = {
            'id': message.get('id'),
            'thread_id': message.get('threadId'),
            'subject': None,
            'from_email': None,
            'from_name': None,
            'to_emails': [],
            'cc_emails': [],
            'timestamp': None,
            'body': None,
            'snippet': message.get('snippet', '')
        }

        for header in headers:
            name = header.get('name', '').lower()
            value = header.get('value', '')

            if name == 'subject':
                email_data['subject'] = value
            elif name == 'from':
                # Extract email and name from format: "Name <email@domain.com>"
                import re
                match = re.search(r'(.*)<(.*)>|(.*)', value)
                if match:
                    groups = match.groups()
                    if groups[1]:  # Has email format "Name <email>"
                        email_data['from_name'] = groups[0].strip().strip('"')
                        email_data['from_email'] = groups[1]
                    else:  # Just email address
                        email_data['from_email'] = groups[2]
            elif name == 'to':
                email_data['to_emails'] = [email.strip() for email in value.split(',')]
            elif name == 'cc':
                email_data['cc_emails'] = [email.strip() for email in value.split(',')]
            elif name == 'date':
                try:
                    import email.utils
                    parsed_date = email.utils.parsedate_to_datetime(value)
                    email_data['timestamp'] = parsed_date.isoformat()
                except:
                    email_data['timestamp'] = value

        # Get the message body
        payload = message.get('payload', {})
        parts = payload.get('parts', [])

        if not parts and 'body' in payload:
            # Message has no parts, body is directly in payload
            body_data = payload['body'].get('data', '')
            if body_data:
                import base64
                email_data['body'] = base64.urlsafe_b64decode(body_data).decode('utf-8')
        else:
            # Parse body from parts
            for part in parts:
                if part.get('mimeType') == 'text/plain' or part.get('mimeType') == 'text/html':
                    body_data = part.get('body', {}).get('data', '')
                    if body_data:
                        import base64
                        email_data['body'] = base64.urlsafe_b64decode(body_data).decode('utf-8')
                        break

        return email_data

    async def watch_email(self):
        """Set up email watching using Gmail Push Notifications (requires Pub/Sub)"""
        try:
            service = self.get_service()

            # Create watch request
            watch_body = {
                'labelIds': ['INBOX'],
                'topicName': 'projects/your-project-id/topics/gmail-notifications'  # This needs to be configured in Google Cloud Console
            }

            response = service.users().watch(userId='me', body=watch_body).execute()
            logger.info(f"Gmail watch setup: {response}")
            return response
        except Exception as e:
            logger.error(f"Error setting up Gmail watch: {e}")
            # Fallback to polling
            logger.info("Falling back to polling method for email checking")
            return None

    def poll_emails(self, query: str = "is:unread after:1d", max_results: int = 10) -> list:
        """Poll for new emails (fallback method)"""
        return self.get_unread_messages(query, max_results)

    def get_inbound_emails(self, max_results: int = 10) -> list:
        """Get only inbound emails (from customers, not sent by me)"""
        try:
            service = self.get_service()

            # Query to get only emails that are not from the user (inbound emails)
            # This query looks for unread emails in inbox that are not from the support email
            query = f"is:unread in:inbox -from:{self.settings.gmail_support_email}"

            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            detailed_messages = []

            for message in messages:
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id']
                ).execute()

                # Additional check to ensure the email is from a different address
                # This is a secondary check beyond the Gmail query filter
                parsed_email = self.parse_email(msg)
                sender_email = parsed_email.get('from_email', '')

                # Skip if the email is from our own address
                if sender_email and sender_email == self.settings.gmail_support_email:
                    logger.debug(f"Skipping email from own address: {sender_email}")
                    continue

                detailed_messages.append(msg)

            return detailed_messages
        except Exception as e:
            logger.error(f"Error getting inbound emails: {e}")
            return []


    def enable_push_notifications(self, topic_name: Optional[str] = None, label_ids: Optional[list] = None):
        """
        Enable Gmail push notifications to a Pub/Sub topic
        This allows real-time email notifications instead of polling
        """
        try:
            service = self.get_service()

            if topic_name is None:
                topic_name = f"projects/{self.settings.google_project_id}/topics/{self.settings.pubsub_topic_name}"

            if label_ids is None:
                label_ids = ["INBOX"]  # Monitor the inbox for new emails

            # Request Gmail to start watching for changes
            watch_body = {
                'labelIds': label_ids,
                'topicName': topic_name
            }

            response = service.users().watch(userId='me', body=watch_body).execute()

            logger.info(f"Gmail push notifications enabled: {response}")
            return response

        except Exception as e:
            logger.error(f"Error enabling Gmail push notifications: {e}")
            # Fallback to polling
            logger.info("Falling back to polling method")
            return None

    def stop_push_notifications(self):
        """Stop Gmail push notifications"""
        try:
            service = self.get_service()

            # Stop watching
            response = service.users().stop(userId='me').execute()

            logger.info("Gmail push notifications stopped")
            return response

        except Exception as e:
            logger.error(f"Error stopping Gmail push notifications: {e}")
            return None

    def get_history_since(self, start_history_id: str, max_results: int = 100):
        """
        Get Gmail history since a specific history ID
        This is used with push notifications to get the actual changes
        """
        try:
            service = self.get_service()

            results = service.users().history().list(
                userId='me',
                startHistoryId=start_history_id,
                historyTypes=['messageAdded'],
                maxResults=max_results
            ).execute()

            return results.get('history', [])

        except Exception as e:
            logger.error(f"Error getting Gmail history: {e}")
            return []


# Global Gmail service instance
gmail_service = GmailService()