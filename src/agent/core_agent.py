"""
TaskFlow AI Customer Success Agent - Core Prototype
Exercise 1.2: Core Message Processing Loop

This prototype demonstrates:
1. Message normalization across channels
2. Knowledge base search
3. Channel-aware response generation
4. Escalation decision logic
"""

import json
import re
from typing import Dict, Tuple, List
from enum import Enum
from dataclasses import dataclass


class Channel(Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    WEB = "web"


class EscalationReason(Enum):
    BILLING = "billing"
    SECURITY = "security"
    LEGAL = "legal"
    COMPLIANCE = "compliance"
    ENTERPRISE_SALES = "enterprise_sales"
    NEGATIVE_SENTIMENT = "negative_sentiment"
    CHURN_THREAT = "churn_threat"
    NONE = "none"


@dataclass
class NormalizedMessage:
    """Normalized message format across all channels"""
    customer_id: str
    customer_name: str
    channel: Channel
    message: str
    subject: str = ""
    timestamp: str = ""
    priority: str = "medium"


@dataclass
class AgentResponse:
    """Agent response with escalation decision"""
    response: str
    should_escalate: bool
    escalation_reason: EscalationReason
    confidence: float
    matched_topics: List[str]


class KnowledgeBase:
    """Simple knowledge base for product documentation"""

    def __init__(self, docs_path: str):
        self.docs_path = docs_path
        self.docs_content = self._load_docs()

    def _load_docs(self) -> str:
        """Load product documentation"""
        try:
            with open(self.docs_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def search(self, query: str) -> List[str]:
        """Simple keyword-based search in documentation"""
        query_lower = query.lower()
        keywords = self._extract_keywords(query_lower)

        # Split docs into sections
        sections = self.docs_content.split('\n## ')
        relevant_sections = []

        for section in sections:
            section_lower = section.lower()
            # Check if any keyword appears in this section
            if any(keyword in section_lower for keyword in keywords):
                relevant_sections.append(section.strip())

        return relevant_sections[:3]  # Return top 3 relevant sections

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from query"""
        # Remove common words
        stop_words = {'how', 'do', 'i', 'can', 'the', 'a', 'an', 'is', 'to', 'in', 'for', 'of', 'and', 'or'}
        words = re.findall(r'\b\w+\b', text)
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords


class EscalationEngine:
    """Decides whether to escalate based on rules"""

    # Keywords that trigger escalation
    BILLING_KEYWORDS = ['billing', 'charged', 'charge', 'refund', 'invoice', 'payment', 'subscription', 'price', 'pricing']
    SECURITY_KEYWORDS = ['security', 'password', 'login', 'access', 'locked', 'unauthorized', 'hack', 'breach']
    LEGAL_KEYWORDS = ['legal', 'gdpr', 'compliance', 'terms', 'privacy', 'data export', 'lawyer', 'attorney']
    ENTERPRISE_KEYWORDS = ['enterprise', 'sso', 'saml', 'okta', 'azure ad', 'custom sla', 'dedicated', 'migration']
    CHURN_KEYWORDS = ['cancel', 'cancellation', 'refund', 'terrible', 'worst', 'switching', 'competitor']

    @staticmethod
    def decide(message: NormalizedMessage) -> Tuple[bool, EscalationReason]:
        """Decide if message should be escalated"""
        text_lower = (message.message + " " + message.subject).lower()

        # Check for churn threats (highest priority)
        if any(word in text_lower for word in EscalationEngine.CHURN_KEYWORDS):
            if 'cancel' in text_lower or 'refund' in text_lower:
                return True, EscalationReason.CHURN_THREAT

        # Check for security issues
        if any(word in text_lower for word in EscalationEngine.SECURITY_KEYWORDS):
            if 'locked' in text_lower or 'unauthorized' in text_lower or 'breach' in text_lower:
                return True, EscalationReason.SECURITY

        # Check for legal/compliance
        if any(word in text_lower for word in EscalationEngine.LEGAL_KEYWORDS):
            return True, EscalationReason.LEGAL

        # Check for enterprise opportunities
        if any(word in text_lower for word in EscalationEngine.ENTERPRISE_KEYWORDS):
            if 'enterprise' in text_lower or 'sso' in text_lower or 'migration' in text_lower:
                return True, EscalationReason.ENTERPRISE_SALES

        # Check for billing issues
        if any(word in text_lower for word in EscalationEngine.BILLING_KEYWORDS):
            if 'charged twice' in text_lower or 'duplicate' in text_lower or 'refund' in text_lower:
                return True, EscalationReason.BILLING

        # Check priority level
        if message.priority == "urgent":
            return True, EscalationReason.NEGATIVE_SENTIMENT

        return False, EscalationReason.NONE


class ResponseGenerator:
    """Generates channel-appropriate responses"""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def generate(self, message: NormalizedMessage, kb_results: List[str]) -> str:
        """Generate response based on channel and knowledge base results"""

        # Extract relevant information from KB
        if kb_results:
            answer = self._extract_answer(message.message, kb_results)
        else:
            answer = "I don't have specific information about that in our documentation."

        # Format response based on channel
        if message.channel == Channel.EMAIL:
            return self._format_email_response(message, answer)
        elif message.channel == Channel.WHATSAPP:
            return self._format_whatsapp_response(message, answer)
        else:  # WEB
            return self._format_web_response(message, answer)

    def _extract_answer(self, query: str, kb_results: List[str]) -> str:
        """Extract relevant answer from KB results"""
        # Simple extraction - in production, use LLM here
        if kb_results:
            # Return first relevant section (simplified)
            return kb_results[0][:500] + "..."
        return ""

    def _format_email_response(self, message: NormalizedMessage, answer: str) -> str:
        """Format response for email - formal and structured"""
        name = message.customer_name.split()[0] if message.customer_name else "there"

        response = f"Hi {name},\n\n"
        response += f"Thank you for reaching out to TaskFlow support.\n\n"
        response += f"{answer}\n\n"
        response += "If you need any further assistance, please don't hesitate to ask.\n\n"
        response += "Best regards,\n"
        response += "TaskFlow Support Team"

        return response

    def _format_whatsapp_response(self, message: NormalizedMessage, answer: str) -> str:
        """Format response for WhatsApp - casual and concise"""
        name = message.customer_name.split()[0] if message.customer_name else "there"

        # Simplify answer for WhatsApp
        short_answer = answer[:200] if len(answer) > 200 else answer

        response = f"Hey {name}! 👋\n\n"
        response += f"{short_answer}\n\n"
        response += "Let me know if you need anything else!"

        return response

    def _format_web_response(self, message: NormalizedMessage, answer: str) -> str:
        """Format response for web form - professional and direct"""
        name = message.customer_name.split()[0] if message.customer_name else "there"

        response = f"Hi {name},\n\n"
        response += f"{answer}\n\n"
        response += "Need more help? Feel free to reach out."

        return response


class CustomerSuccessAgent:
    """Main agent that orchestrates the entire flow"""

    def __init__(self, docs_path: str):
        self.kb = KnowledgeBase(docs_path)
        self.response_generator = ResponseGenerator(self.kb)

    def process_message(self, message_data: Dict) -> AgentResponse:
        """
        Main processing loop:
        1. Normalize message
        2. Search knowledge base
        3. Generate response
        4. Decide escalation
        """

        # Step 1: Normalize message
        normalized = self._normalize_message(message_data)

        # Step 2: Check for escalation first
        should_escalate, escalation_reason = EscalationEngine.decide(normalized)

        # Step 3: Search knowledge base
        kb_results = self.kb.search(normalized.message)
        matched_topics = [result[:50] + "..." for result in kb_results]

        # Step 4: Generate response
        response_text = self.response_generator.generate(normalized, kb_results)

        # Step 5: Calculate confidence
        confidence = 0.9 if kb_results else 0.3
        if should_escalate:
            confidence = 0.5  # Lower confidence when escalating

        return AgentResponse(
            response=response_text,
            should_escalate=should_escalate,
            escalation_reason=escalation_reason,
            confidence=confidence,
            matched_topics=matched_topics
        )

    def _normalize_message(self, data: Dict) -> NormalizedMessage:
        """Normalize message from any channel into standard format"""
        return NormalizedMessage(
            customer_id=data.get('customer_id', ''),
            customer_name=data.get('customer_name', ''),
            channel=Channel(data.get('channel', 'email')),
            message=data.get('message', ''),
            subject=data.get('subject', ''),
            timestamp=data.get('timestamp', ''),
            priority=data.get('priority', 'medium')
        )


def test_agent():
    """Test the agent with sample tickets"""
    import os
    import sys

    # Fix Windows console encoding for emojis
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    # Initialize agent
    docs_path = os.path.join('context', 'product-docs.md')
    agent = CustomerSuccessAgent(docs_path)

    # Test cases from sample tickets
    test_cases = [
        {
            "name": "Simple How-To (WhatsApp)",
            "data": {
                "channel": "whatsapp",
                "customer_id": "+447700900123",
                "customer_name": "James Chen",
                "message": "Hey! Quick q - how do I set up recurring tasks? Need weekly standup reminders",
                "priority": "low"
            }
        },
        {
            "name": "Billing Issue (Web) - Should Escalate",
            "data": {
                "channel": "web",
                "customer_id": "maria.garcia@designagency.com",
                "customer_name": "Maria Garcia",
                "subject": "Billing issue - charged twice",
                "message": "I was charged twice for our Business plan subscription this month. Please refund the duplicate charge immediately.",
                "priority": "high"
            }
        },
        {
            "name": "Integration Question (Email)",
            "data": {
                "channel": "email",
                "customer_id": "sarah.johnson@techstartup.io",
                "customer_name": "Sarah Johnson",
                "subject": "Slack integration not syncing",
                "message": "Hi TaskFlow team,\n\nI've connected our Slack workspace to TaskFlow, but notifications aren't coming through. Could you help me troubleshoot this?\n\nThanks,\nSarah",
                "priority": "medium"
            }
        },
        {
            "name": "Enterprise Inquiry (Email) - Should Escalate",
            "data": {
                "channel": "email",
                "customer_id": "david.kim@consultingfirm.com",
                "customer_name": "David Kim",
                "subject": "Enterprise pricing inquiry",
                "message": "We're a consulting firm with 150 employees looking to migrate to TaskFlow. We need SSO integration with Okta and custom SLA. Could you provide enterprise pricing?",
                "priority": "high"
            }
        }
    ]

    print("=" * 80)
    print("TASKFLOW AI CUSTOMER SUCCESS AGENT - PROTOTYPE TEST")
    print("=" * 80)
    print()

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print(f"{'=' * 80}")
        print(f"\nChannel: {test_case['data']['channel'].upper()}")
        print(f"Customer: {test_case['data']['customer_name']}")
        print(f"Message: {test_case['data']['message'][:100]}...")
        print()

        # Process message
        response = agent.process_message(test_case['data'])

        print(f"AGENT RESPONSE:")
        print(f"{'-' * 80}")
        print(response.response)
        print(f"{'-' * 80}")
        print()
        print(f"Should Escalate: {response.should_escalate}")
        if response.should_escalate:
            print(f"Escalation Reason: {response.escalation_reason.value}")
        print(f"Confidence: {response.confidence:.2f}")
        print(f"Matched Topics: {len(response.matched_topics)}")
        print()


if __name__ == "__main__":
    test_agent()
