"""
Production Agent Implementation
OpenAI-powered customer success agent with full capabilities
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
from datetime import datetime

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Use simplified config by default for local development
# This allows switching between configurations without code changes
import os
if os.getenv('USE_SIMPLE_CONFIG', 'true').lower() == 'true':
    from src.config_simple import get_settings
else:
    from src.config import get_settings
from src.database.models import (
    Customer, Conversation, Message, Ticket, Escalation,
    ChannelType, ConversationStatus, EscalationReason
)

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class AgentContext:
    """Context for agent processing"""
    customer_id: str
    customer_name: str
    channel: ChannelType
    message: str
    subject: str = ""
    conversation_history: List[Dict] = None
    customer_profile: Optional[Customer] = None


@dataclass
class AgentResponse:
    """Agent response with metadata"""
    response_text: str
    should_escalate: bool
    escalation_reason: Optional[EscalationReason]
    sentiment_score: float
    confidence: float
    processing_time_ms: float


class ProductionAgent:
    """
    Production-grade AI Customer Success Agent

    Uses OpenAI GPT-4 for natural language understanding and generation.
    Integrates with database for customer context and conversation history.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize production agent

        Args:
            session: Database session for queries
        """
        self.session = session

        # Configure client based on settings (OpenAI or Groq)
        if settings.use_groq:
            # Use Groq API with custom base URL
            self.client = AsyncOpenAI(
                api_key=settings.openai_api_key,
                base_url=settings.groq_base_url
            )
        else:
            # Use OpenAI API
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)

        self.model = settings.openai_model

        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()

        # Load escalation rules
        self.escalation_rules = self._load_escalation_rules()

        # Load brand voice
        self.brand_voice = self._load_brand_voice()

    def _load_knowledge_base(self) -> str:
        """Load product documentation"""
        try:
            with open("context/product-docs.md", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Product docs not found")
            return ""

    def _load_escalation_rules(self) -> str:
        """Load escalation rules"""
        try:
            with open("context/escalation-rules.md", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Escalation rules not found")
            return ""

    def _load_brand_voice(self) -> str:
        """Load brand voice guidelines"""
        try:
            with open("context/brand-voice.md", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Brand voice not found")
            return ""

    async def process_message(self, context: AgentContext) -> AgentResponse:
        """
        Process customer message and generate response

        Args:
            context: Agent context with customer info and message

        Returns:
            AgentResponse with generated response and metadata
        """
        start_time = datetime.now()

        try:
            # Step 1: Analyze sentiment
            sentiment_score = await self._analyze_sentiment(context.message)
            logger.info(f"Sentiment score: {sentiment_score}")

            # Step 2: Check for immediate escalation
            should_escalate, escalation_reason = await self._check_escalation(
                context, sentiment_score
            )

            if should_escalate:
                logger.info(f"Escalation required: {escalation_reason}")
                response_text = await self._generate_escalation_response(
                    context, escalation_reason
                )
            else:
                # Step 3: Generate response using OpenAI
                response_text = await self._generate_response(context, sentiment_score)

            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000

            return AgentResponse(
                response_text=response_text,
                should_escalate=should_escalate,
                escalation_reason=escalation_reason if should_escalate else None,
                sentiment_score=sentiment_score,
                confidence=0.9 if not should_escalate else 0.5,
                processing_time_ms=processing_time
            )

        except Exception as e:
            logger.error(f"Agent processing error: {e}", exc_info=True)
            # Fallback response
            return AgentResponse(
                response_text=self._get_fallback_response(context.channel),
                should_escalate=True,
                escalation_reason=EscalationReason.TECHNICAL,
                sentiment_score=0.0,
                confidence=0.0,
                processing_time_ms=0.0
            )

    async def _analyze_sentiment(self, text: str) -> float:
        """
        Analyze sentiment using OpenAI

        Returns:
            Sentiment score between -1.0 (very negative) and 1.0 (very positive)
        """
        if not settings.enable_sentiment_analysis:
            return 0.0

        try:
            response = await self.client.chat.completions.create(
                model=self.model,  # Use configured model for sentiment
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze the sentiment of customer messages. Return a score between -1.0 (very negative) and 1.0 (very positive). Only return the number."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                max_tokens=10,
                temperature=0.0
            )

            score_text = response.choices[0].message.content.strip()
            return float(score_text)

        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return 0.0

    async def _check_escalation(
        self,
        context: AgentContext,
        sentiment_score: float
    ) -> tuple[bool, Optional[EscalationReason]]:
        """
        Check if message should be escalated

        Returns:
            (should_escalate, reason)
        """
        if not settings.enable_auto_escalation:
            return False, None

        text_lower = ((context.message or "") + " " + (context.subject or "")).lower()

        # Churn threat (highest priority)
        churn_keywords = ["cancel", "refund", "terrible", "worst", "switching"]
        if any(word in text_lower for word in churn_keywords) and sentiment_score < -0.5:
            return True, EscalationReason.CHURN_THREAT

        # Security issues
        security_keywords = ["locked", "unauthorized", "breach", "hacked", "security"]
        if any(word in text_lower for word in security_keywords):
            return True, EscalationReason.SECURITY

        # Legal/compliance
        legal_keywords = ["gdpr", "legal", "lawyer", "compliance", "data export"]
        if any(word in text_lower for word in legal_keywords):
            return True, EscalationReason.LEGAL

        # Billing issues
        billing_keywords = ["charged twice", "duplicate charge", "billing error", "wrong amount"]
        if any(phrase in text_lower for phrase in billing_keywords):
            return True, EscalationReason.BILLING

        # Enterprise sales
        enterprise_keywords = ["enterprise", "sso", "custom sla", "150 users", "migration"]
        if any(word in text_lower for word in enterprise_keywords):
            return True, EscalationReason.ENTERPRISE_SALES

        # Very negative sentiment
        if sentiment_score < -0.7:
            return True, EscalationReason.CHURN_THREAT

        return False, None

    async def _generate_response(
        self,
        context: AgentContext,
        sentiment_score: float
    ) -> str:
        """
        Generate response using OpenAI GPT-4
        """
        # Build conversation history
        history_text = ""
        if context.conversation_history:
            history_text = "\n".join([
                f"{msg['sender']}: {msg['content']}"
                for msg in context.conversation_history[-5:]  # Last 5 messages
            ])

        # Build system prompt
        system_prompt = f"""You are a helpful customer success agent for TaskFlow, a project management SaaS platform.

BRAND VOICE:
{self.brand_voice[:500]}

CHANNEL: {context.channel.value}
- Email: Formal, 150-300 words, with greeting and signature
- WhatsApp: Casual, 50-100 words, friendly with emojis
- Web: Professional, 100-200 words, direct

KNOWLEDGE BASE:
{self.knowledge_base[:2000]}

CONVERSATION HISTORY:
{history_text}

CUSTOMER: {context.customer_name}
SENTIMENT: {sentiment_score:.2f}

Respond to the customer's message appropriately for the {context.channel.value} channel."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context.message}
                ],
                max_tokens=settings.openai_max_tokens,
                temperature=settings.openai_temperature
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._get_fallback_response(context.channel)

    async def _generate_escalation_response(
        self,
        context: AgentContext,
        reason: EscalationReason
    ) -> str:
        """Generate acknowledgment response for escalated issues"""

        name = context.customer_name.split()[0] if context.customer_name else "there"

        # Channel-specific formatting
        if context.channel == ChannelType.EMAIL:
            return f"""Hi {name},

Thank you for reaching out to TaskFlow support.

I understand this is an important matter that requires immediate attention from our team. I've escalated your request to our {self._get_team_name(reason)} team, and they will respond within 15 minutes.

We appreciate your patience and will resolve this as quickly as possible.

Best regards,
TaskFlow Support Team"""

        elif context.channel == ChannelType.WHATSAPP:
            return f"""Hey {name}! 👋

I've escalated this to our {self._get_team_name(reason)} team. They'll reach out within 15 minutes to help you out.

Thanks for your patience!"""

        else:  # WEB
            return f"""Hi {name},

I've escalated your request to our {self._get_team_name(reason)} team. They'll respond within 15 minutes.

Thank you for your patience."""

    def _get_team_name(self, reason: EscalationReason) -> str:
        """Get human-readable team name"""
        team_map = {
            EscalationReason.BILLING: "billing",
            EscalationReason.SECURITY: "security",
            EscalationReason.LEGAL: "legal",
            EscalationReason.COMPLIANCE: "compliance",
            EscalationReason.ENTERPRISE_SALES: "sales",
            EscalationReason.TECHNICAL: "engineering",
            EscalationReason.CHURN_THREAT: "customer success",
            EscalationReason.BUG_REPORT: "engineering"
        }
        return team_map.get(reason, "support")

    def _get_fallback_response(self, channel: ChannelType) -> str:
        """Get fallback response when AI fails"""
        if channel == ChannelType.EMAIL:
            return """Hi there,

Thank you for contacting TaskFlow support.

I'm currently experiencing technical difficulties, but I've notified our team about your request. A human agent will respond shortly.

We apologize for any inconvenience.

Best regards,
TaskFlow Support Team"""

        elif channel == ChannelType.WHATSAPP:
            return "Hey! I'm having some technical issues. Our team has been notified and will help you out shortly. Thanks for your patience!"

        else:
            return "We've received your request. Our team will respond shortly. Thank you for your patience."


async def create_agent(session: AsyncSession) -> ProductionAgent:
    """Factory function to create agent instance"""
    return ProductionAgent(session)
