"""
TaskFlow AI Customer Success Agent - State Management
Exercise 1.3: Memory and Conversation State

This module adds:
1. Conversation history tracking
2. Customer context management
3. Sentiment tracking over time
4. Topic/issue tracking
5. Channel switching detection
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class SentimentScore(Enum):
    VERY_POSITIVE = 1.0
    POSITIVE = 0.5
    NEUTRAL = 0.0
    NEGATIVE = -0.5
    VERY_NEGATIVE = -1.0


@dataclass
class Message:
    """Individual message in a conversation"""
    message_id: str
    timestamp: str
    channel: str
    sender: str  # "customer" or "agent"
    content: str
    sentiment: float

    def to_dict(self):
        return asdict(self)


@dataclass
class CustomerProfile:
    """Customer profile with contact methods and history"""
    customer_id: str
    primary_email: Optional[str] = None
    phone_number: Optional[str] = None
    name: str = ""
    company: str = ""
    plan_type: str = "free"

    # Tracking
    total_conversations: int = 0
    total_messages: int = 0
    average_sentiment: float = 0.0
    escalation_count: int = 0
    last_contact_date: str = ""

    # Contact methods
    contact_channels: List[str] = None

    def __post_init__(self):
        if self.contact_channels is None:
            self.contact_channels = []

    def to_dict(self):
        return asdict(self)


@dataclass
class Conversation:
    """A conversation thread with a customer"""
    conversation_id: str
    customer_id: str
    channel: str
    status: str  # "open", "pending", "escalated", "resolved"
    created_at: str
    updated_at: str

    # Content
    subject: str = ""
    messages: List[Message] = None

    # Tracking
    sentiment_history: List[float] = None
    topics: List[str] = None
    escalated: bool = False
    escalation_reason: str = ""
    resolution_notes: str = ""

    def __post_init__(self):
        if self.messages is None:
            self.messages = []
        if self.sentiment_history is None:
            self.sentiment_history = []
        if self.topics is None:
            self.topics = []

    def add_message(self, message: Message):
        """Add a message to the conversation"""
        self.messages.append(message)
        self.sentiment_history.append(message.sentiment)
        self.updated_at = message.timestamp

    def get_average_sentiment(self) -> float:
        """Calculate average sentiment for this conversation"""
        if not self.sentiment_history:
            return 0.0
        return sum(self.sentiment_history) / len(self.sentiment_history)

    def get_latest_sentiment(self) -> float:
        """Get the most recent sentiment score"""
        if not self.sentiment_history:
            return 0.0
        return self.sentiment_history[-1]

    def to_dict(self):
        data = asdict(self)
        data['messages'] = [msg.to_dict() if hasattr(msg, 'to_dict') else msg for msg in self.messages]
        return data


class StateManager:
    """Manages customer profiles and conversation state"""

    def __init__(self, storage_path: str = "data/state.json"):
        self.storage_path = storage_path
        self.customers: Dict[str, CustomerProfile] = {}
        self.conversations: Dict[str, Conversation] = {}
        self.load_state()

    def load_state(self):
        """Load state from disk"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Load customers
                for cust_id, cust_data in data.get('customers', {}).items():
                    self.customers[cust_id] = CustomerProfile(**cust_data)

                # Load conversations
                for conv_id, conv_data in data.get('conversations', {}).items():
                    # Reconstruct messages
                    messages = [Message(**msg) for msg in conv_data.get('messages', [])]
                    conv_data['messages'] = messages
                    self.conversations[conv_id] = Conversation(**conv_data)
        except FileNotFoundError:
            # First run, no state file yet
            pass

    def save_state(self):
        """Save state to disk"""
        import os
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

        data = {
            'customers': {cid: cust.to_dict() for cid, cust in self.customers.items()},
            'conversations': {cid: conv.to_dict() for cid, conv in self.conversations.items()}
        }

        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def get_or_create_customer(self, customer_id: str, name: str = "",
                               channel: str = "email") -> CustomerProfile:
        """Get existing customer or create new profile"""
        if customer_id not in self.customers:
            # Determine if email or phone
            is_email = '@' in customer_id

            customer = CustomerProfile(
                customer_id=customer_id,
                primary_email=customer_id if is_email else None,
                phone_number=customer_id if not is_email else None,
                name=name,
                contact_channels=[channel]
            )
            self.customers[customer_id] = customer
        else:
            customer = self.customers[customer_id]
            # Update contact channels if new
            if channel not in customer.contact_channels:
                customer.contact_channels.append(channel)

        return customer

    def get_or_create_conversation(self, customer_id: str, channel: str,
                                   subject: str = "") -> Conversation:
        """Get active conversation or create new one"""
        # Look for open conversation with this customer on this channel
        for conv in self.conversations.values():
            if (conv.customer_id == customer_id and
                conv.channel == channel and
                conv.status in ["open", "pending"]):
                return conv

        # Create new conversation
        conv_id = f"conv_{customer_id}_{len(self.conversations)}"
        now = datetime.now().isoformat()

        conversation = Conversation(
            conversation_id=conv_id,
            customer_id=customer_id,
            channel=channel,
            status="open",
            created_at=now,
            updated_at=now,
            subject=subject
        )

        self.conversations[conv_id] = conversation
        return conversation

    def add_message_to_conversation(self, conversation: Conversation,
                                    sender: str, content: str,
                                    sentiment: float, channel: str):
        """Add a message to a conversation"""
        msg_id = f"msg_{conversation.conversation_id}_{len(conversation.messages)}"

        message = Message(
            message_id=msg_id,
            timestamp=datetime.now().isoformat(),
            channel=channel,
            sender=sender,
            content=content,
            sentiment=sentiment
        )

        conversation.add_message(message)

        # Update customer stats
        customer = self.customers[conversation.customer_id]
        customer.total_messages += 1
        customer.last_contact_date = message.timestamp

        # Recalculate average sentiment
        all_sentiments = []
        for conv in self.conversations.values():
            if conv.customer_id == customer.customer_id:
                all_sentiments.extend(conv.sentiment_history)

        if all_sentiments:
            customer.average_sentiment = sum(all_sentiments) / len(all_sentiments)

    def escalate_conversation(self, conversation: Conversation, reason: str):
        """Mark conversation as escalated"""
        conversation.escalated = True
        conversation.escalation_reason = reason
        conversation.status = "escalated"

        # Update customer escalation count
        customer = self.customers[conversation.customer_id]
        customer.escalation_count += 1

    def get_conversation_history(self, customer_id: str, limit: int = 10) -> List[Message]:
        """Get recent message history for a customer"""
        all_messages = []

        for conv in self.conversations.values():
            if conv.customer_id == customer_id:
                all_messages.extend(conv.messages)

        # Sort by timestamp and return most recent
        all_messages.sort(key=lambda m: m.timestamp, reverse=True)
        return all_messages[:limit]

    def detect_channel_switch(self, customer_id: str, current_channel: str) -> bool:
        """Detect if customer switched channels"""
        history = self.get_conversation_history(customer_id, limit=5)

        if len(history) < 2:
            return False

        # Check if previous message was on different channel
        previous_channel = history[1].channel if len(history) > 1 else None
        return previous_channel and previous_channel != current_channel

    def get_customer_context(self, customer_id: str) -> Dict:
        """Get full context for a customer"""
        customer = self.customers.get(customer_id)
        if not customer:
            return {}

        # Get active conversations
        active_convs = [
            conv for conv in self.conversations.values()
            if conv.customer_id == customer_id and conv.status in ["open", "pending"]
        ]

        # Get recent history
        recent_messages = self.get_conversation_history(customer_id, limit=10)

        return {
            'customer': customer.to_dict(),
            'active_conversations': len(active_convs),
            'recent_messages': [msg.to_dict() for msg in recent_messages],
            'average_sentiment': customer.average_sentiment,
            'escalation_count': customer.escalation_count,
            'channels_used': customer.contact_channels
        }


class SentimentAnalyzer:
    """Simple sentiment analysis based on keywords"""

    POSITIVE_WORDS = ['love', 'great', 'awesome', 'excellent', 'thank', 'thanks', 'perfect',
                      'amazing', 'wonderful', 'fantastic', 'happy', 'pleased']
    NEGATIVE_WORDS = ['terrible', 'awful', 'worst', 'hate', 'frustrated', 'angry', 'disappointed',
                      'unacceptable', 'horrible', 'useless', 'broken', 'crash', 'slow']
    VERY_NEGATIVE_WORDS = ['cancel', 'refund', 'lawsuit', 'lawyer', 'sue', 'fraud']

    @staticmethod
    def analyze(text: str) -> float:
        """Analyze sentiment of text, return score between -1.0 and 1.0"""
        text_lower = text.lower()

        # Count positive and negative words
        positive_count = sum(1 for word in SentimentAnalyzer.POSITIVE_WORDS if word in text_lower)
        negative_count = sum(1 for word in SentimentAnalyzer.NEGATIVE_WORDS if word in text_lower)
        very_negative_count = sum(1 for word in SentimentAnalyzer.VERY_NEGATIVE_WORDS if word in text_lower)

        # Check for very negative
        if very_negative_count > 0:
            return -1.0

        # Calculate score
        if positive_count == 0 and negative_count == 0:
            return 0.0  # Neutral

        score = (positive_count - negative_count * 1.5) / (positive_count + negative_count + 1)

        # Clamp between -1 and 1
        return max(-1.0, min(1.0, score))


def test_state_management():
    """Test state management functionality"""
    import os
    import sys

    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 80)
    print("STATE MANAGEMENT TEST")
    print("=" * 80)
    print()

    # Initialize state manager
    state = StateManager("data/test_state.json")

    # Test 1: Create customer and conversation
    print("Test 1: Creating customer and conversation")
    print("-" * 80)
    customer = state.get_or_create_customer(
        "sarah.johnson@techstartup.io",
        name="Sarah Johnson",
        channel="email"
    )
    print(f"Created customer: {customer.name} ({customer.customer_id})")

    conv = state.get_or_create_conversation(
        customer.customer_id,
        channel="email",
        subject="Slack integration issue"
    )
    print(f"Created conversation: {conv.conversation_id}")
    print()

    # Test 2: Add messages with sentiment
    print("Test 2: Adding messages with sentiment tracking")
    print("-" * 80)

    messages_to_add = [
        ("customer", "Hi, my Slack integration isn't working. This is frustrating.", "email"),
        ("agent", "Hi Sarah, I'd be happy to help you troubleshoot the Slack integration.", "email"),
        ("customer", "Thanks! I've tried reconnecting but still no notifications.", "email"),
        ("agent", "Let me check your settings. Can you verify the webhook URL?", "email"),
        ("customer", "Yes, it's configured correctly. Still not working.", "email"),
    ]

    for sender, content, channel in messages_to_add:
        sentiment = SentimentAnalyzer.analyze(content)
        state.add_message_to_conversation(conv, sender, content, sentiment, channel)
        print(f"{sender.upper()}: {content[:60]}... (sentiment: {sentiment:.2f})")

    print()
    print(f"Conversation sentiment: {conv.get_average_sentiment():.2f}")
    print(f"Total messages: {len(conv.messages)}")
    print()

    # Test 3: Channel switching
    print("Test 3: Channel switching detection")
    print("-" * 80)

    # Customer switches to WhatsApp
    whatsapp_conv = state.get_or_create_conversation(
        customer.customer_id,
        channel="whatsapp",
        subject=""
    )

    sentiment = SentimentAnalyzer.analyze("Hey, still waiting on that Slack fix!")
    state.add_message_to_conversation(
        whatsapp_conv, "customer",
        "Hey, still waiting on that Slack fix!",
        sentiment, "whatsapp"
    )

    switched = state.detect_channel_switch(customer.customer_id, "whatsapp")
    print(f"Channel switch detected: {switched}")
    print(f"Customer now using channels: {customer.contact_channels}")
    print()

    # Test 4: Customer context
    print("Test 4: Customer context retrieval")
    print("-" * 80)
    context = state.get_customer_context(customer.customer_id)
    print(f"Customer: {context['customer']['name']}")
    print(f"Active conversations: {context['active_conversations']}")
    print(f"Total messages: {len(context['recent_messages'])}")
    print(f"Average sentiment: {context['average_sentiment']:.2f}")
    print(f"Channels used: {', '.join(context['channels_used'])}")
    print()

    # Test 5: Escalation
    print("Test 5: Escalation tracking")
    print("-" * 80)
    state.escalate_conversation(conv, "Technical issue requiring engineering team")
    print(f"Conversation escalated: {conv.escalated}")
    print(f"Escalation reason: {conv.escalation_reason}")
    print(f"Customer escalation count: {customer.escalation_count}")
    print()

    # Save state
    print("Saving state to disk...")
    state.save_state()
    print("✓ State saved successfully")
    print()

    # Test 6: Load state
    print("Test 6: Loading state from disk")
    print("-" * 80)
    state2 = StateManager("data/test_state.json")
    print(f"Loaded {len(state2.customers)} customers")
    print(f"Loaded {len(state2.conversations)} conversations")

    loaded_customer = state2.customers.get(customer.customer_id)
    if loaded_customer:
        print(f"✓ Customer data persisted: {loaded_customer.name}")
        print(f"  Average sentiment: {loaded_customer.average_sentiment:.2f}")
        print(f"  Escalation count: {loaded_customer.escalation_count}")

    print()
    print("=" * 80)
    print("STATE MANAGEMENT TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_state_management()
