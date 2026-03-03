"""
Database Models - SQLAlchemy ORM
Production-grade database schema for TaskFlow CRM
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text,
    DateTime, ForeignKey, Index, Enum as SQLEnum
)
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
import enum


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


class ChannelType(str, enum.Enum):
    """Communication channels"""
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    WEB = "web"


class ConversationStatus(str, enum.Enum):
    """Conversation status"""
    OPEN = "open"
    PENDING = "pending"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, enum.Enum):
    """Ticket priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class EscalationReason(str, enum.Enum):
    """Reasons for escalation"""
    BILLING = "billing"
    SECURITY = "security"
    LEGAL = "legal"
    COMPLIANCE = "compliance"
    ENTERPRISE_SALES = "enterprise_sales"
    TECHNICAL = "technical"
    CHURN_THREAT = "churn_threat"
    BUG_REPORT = "bug_report"


class Customer(Base):
    """Customer profile with contact information and history"""
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    primary_email: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    company: Mapped[str] = mapped_column(String(255), default="")
    plan_type: Mapped[str] = mapped_column(String(50), default="free")

    # Statistics
    total_conversations: Mapped[int] = mapped_column(Integer, default=0)
    total_messages: Mapped[int] = mapped_column(Integer, default=0)
    average_sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    escalation_count: Mapped[int] = mapped_column(Integer, default=0)

    # Timestamps
    last_contact_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    conversations: Mapped[List["Conversation"]] = relationship(
        "Conversation",
        back_populates="customer",
        cascade="all, delete-orphan"
    )
    tickets: Mapped[List["Ticket"]] = relationship(
        "Ticket",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Customer(id={self.customer_id}, name={self.name})>"


class Conversation(Base):
    """Conversation thread with a customer"""
    __tablename__ = "conversations"

    conversation_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    customer_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("customers.customer_id", ondelete="CASCADE"),
        index=True
    )
    channel: Mapped[ChannelType] = mapped_column(SQLEnum(ChannelType), nullable=False)
    status: Mapped[ConversationStatus] = mapped_column(
        SQLEnum(ConversationStatus),
        default=ConversationStatus.OPEN,
        index=True
    )

    # Content
    subject: Mapped[str] = mapped_column(Text, default="")

    # Escalation
    escalated: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    escalation_reason: Mapped[Optional[str]] = mapped_column(Text)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    customer: Mapped["Customer"] = relationship("Customer", back_populates="conversations")
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.timestamp"
    )
    tickets: Mapped[List["Ticket"]] = relationship(
        "Ticket",
        back_populates="conversation"
    )
    escalations: Mapped[List["Escalation"]] = relationship(
        "Escalation",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Conversation(id={self.conversation_id}, status={self.status})>"


class Message(Base):
    """Individual message in a conversation"""
    __tablename__ = "messages"

    message_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    conversation_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("conversations.conversation_id", ondelete="CASCADE"),
        index=True
    )
    sender: Mapped[str] = mapped_column(String(50), nullable=False)  # 'customer' or 'agent'
    channel: Mapped[ChannelType] = mapped_column(SQLEnum(ChannelType), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sentiment: Mapped[Optional[float]] = mapped_column(Float)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )

    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.message_id}, sender={self.sender})>"


class Ticket(Base):
    """Support ticket for tracking issues"""
    __tablename__ = "tickets"

    ticket_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    conversation_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("conversations.conversation_id", ondelete="CASCADE")
    )
    customer_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("customers.customer_id", ondelete="CASCADE"),
        index=True
    )

    subject: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[TicketPriority] = mapped_column(
        SQLEnum(TicketPriority),
        default=TicketPriority.MEDIUM,
        index=True
    )
    status: Mapped[ConversationStatus] = mapped_column(
        SQLEnum(ConversationStatus),
        default=ConversationStatus.OPEN,
        index=True
    )

    assigned_to: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    customer: Mapped["Customer"] = relationship("Customer", back_populates="tickets")
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket(id={self.ticket_id}, priority={self.priority})>"


class Escalation(Base):
    """Escalation to human agent"""
    __tablename__ = "escalations"

    escalation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("conversations.conversation_id", ondelete="CASCADE"),
        index=True
    )

    reason: Mapped[EscalationReason] = mapped_column(
        SQLEnum(EscalationReason),
        nullable=False
    )
    target_team: Mapped[str] = mapped_column(String(100), nullable=False)
    urgency: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    escalated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="escalations")

    def __repr__(self):
        return f"<Escalation(id={self.escalation_id}, reason={self.reason})>"


# Indexes for performance
Index('idx_customer_email', Customer.primary_email)
Index('idx_customer_phone', Customer.phone_number)
Index('idx_conversation_customer', Conversation.customer_id)
Index('idx_conversation_status', Conversation.status)
Index('idx_conversation_escalated', Conversation.escalated)
Index('idx_message_conversation', Message.conversation_id)
Index('idx_message_timestamp', Message.timestamp)
Index('idx_ticket_customer', Ticket.customer_id)
Index('idx_ticket_status', Ticket.status)
Index('idx_ticket_priority', Ticket.priority)
Index('idx_escalation_conversation', Escalation.conversation_id)
Index('idx_escalation_urgency', Escalation.urgency)
