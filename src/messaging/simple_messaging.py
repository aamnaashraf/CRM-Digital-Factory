"""
Simple In-Memory Messaging System
Alternative to Kafka for local development without external dependencies
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from threading import Lock
from queue import Queue, Empty
import asyncio

from src.config_simple import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Global message queue for in-memory messaging
message_queue = Queue()
processing_lock = Lock()


@dataclass
class Message:
    """Simplified message structure"""
    topic: str
    key: str
    value: Dict[str, Any]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class SimpleMessageProducer:
    """Simple in-memory message producer (alternative to Kafka)"""

    def __init__(self):
        """Initialize in-memory message producer"""
        logger.info("Simple message producer initialized (in-memory)")

    def publish_inquiry(self, customer_id: str, message_data: Dict[str, Any]) -> bool:
        """
        Publish customer inquiry to in-memory queue

        Args:
            customer_id: Customer identifier
            message_data: Message payload

        Returns:
            True if published successfully
        """
        try:
            # Add metadata
            message_data['published_at'] = datetime.utcnow().isoformat()
            message_data['customer_id'] = customer_id
            message_data['type'] = 'inquiry'

            # Create message and put in queue
            message = Message(
                topic=settings.kafka_topic_inquiries,
                key=customer_id,
                value=message_data
            )

            message_queue.put(message)
            logger.info(f"Published inquiry to in-memory queue: customer={customer_id}")
            return True

        except Exception as e:
            logger.error(f"Simple producer publish error: {e}", exc_info=True)
            return False

    def publish_response(self, customer_id: str, response_data: Dict[str, Any]) -> bool:
        """
        Publish agent response to in-memory queue

        Args:
            customer_id: Customer identifier
            response_data: Response payload

        Returns:
            True if published successfully
        """
        try:
            response_data['published_at'] = datetime.utcnow().isoformat()
            response_data['customer_id'] = customer_id
            response_data['type'] = 'response'

            message = Message(
                topic=settings.kafka_topic_responses,
                key=customer_id,
                value=response_data
            )

            message_queue.put(message)
            logger.info(f"Published response to in-memory queue: customer={customer_id}")
            return True

        except Exception as e:
            logger.error(f"Simple producer publish error: {e}", exc_info=True)
            return False

    def close(self):
        """Close producer (no-op for in-memory)"""
        logger.info("Simple message producer closed")


class SimpleMessageConsumer:
    """Simple in-memory message consumer (alternative to Kafka)"""

    def __init__(self, polling_interval: float = 0.1):
        """
        Initialize in-memory consumer

        Args:
            polling_interval: How often to check for new messages (seconds)
        """
        self.polling_interval = polling_interval
        self.running = False
        self.consumer_group = settings.kafka_consumer_group

        logger.info(f"Simple message consumer initialized: group={self.consumer_group}")

    def consume_messages(self, callback: Callable, max_messages: Optional[int] = None):
        """
        Consume messages from in-memory queue and process with callback

        Args:
            callback: Function to process each message
            max_messages: Maximum messages to process (None = infinite)
        """
        processed = 0
        self.running = True

        try:
            while self.running:
                try:
                    # Try to get a message from the queue (non-blocking with timeout)
                    message: Message = message_queue.get(timeout=self.polling_interval)

                    try:
                        # Process message
                        logger.info(
                            f"Consuming message: topic={message.topic}, "
                            f"key={message.key}, type={message.value.get('type', 'unknown')}"
                        )

                        # Call callback with message data
                        callback(message.value)

                        processed += 1

                        # Check if reached max
                        if max_messages and processed >= max_messages:
                            logger.info(f"Reached max messages: {max_messages}")
                            break

                    except Exception as e:
                        logger.error(f"Message processing error: {e}", exc_info=True)
                    finally:
                        # Mark message as processed
                        message_queue.task_done()

                except Empty:
                    # No messages available, continue loop
                    continue

        except KeyboardInterrupt:
            logger.info("Simple consumer interrupted by user")
        finally:
            self.running = False
            logger.info(f"Simple consumer processed {processed} messages")

    def close(self):
        """Close consumer"""
        self.running = False
        logger.info("Simple message consumer closed")


# Global producer instance
_producer: Optional[SimpleMessageProducer] = None


def get_producer() -> SimpleMessageProducer:
    """Get global simple message producer instance"""
    global _producer
    if _producer is None:
        _producer = SimpleMessageProducer()
    return _producer


def close_producer():
    """Close global producer"""
    global _producer
    if _producer:
        _producer.close()
        _producer = None