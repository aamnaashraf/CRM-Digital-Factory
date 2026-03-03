"""
Database Module
SQLAlchemy models and connection management
"""

from .models import (
    Base,
    Customer,
    Conversation,
    Message,
    Ticket,
    Escalation,
    ChannelType,
    ConversationStatus,
    TicketPriority,
    EscalationReason
)
from .connection import (
    DatabaseManager,
    init_database,
    get_db_manager,
    get_db_session
)

__all__ = [
    "Base",
    "Customer",
    "Conversation",
    "Message",
    "Ticket",
    "Escalation",
    "ChannelType",
    "ConversationStatus",
    "TicketPriority",
    "EscalationReason",
    "DatabaseManager",
    "init_database",
    "get_db_manager",
    "get_db_session",
]
