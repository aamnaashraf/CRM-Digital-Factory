"""
Kafka Message Producer and Consumer
Handles message queue for async processing
"""

from typing import Dict, Any, Optional
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import logging
from datetime import datetime

# Use simplified config by default for local development
# This allows switching between configurations without code changes
import os
if os.getenv('USE_SIMPLE_CONFIG', 'true').lower() == 'true':
    from src.config_simple import get_settings
else:
    from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class MessageProducer:
    """Kafka message producer for publishing customer inquiries"""

    def __init__(self):
        """Initialize Kafka producer"""
        self.producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers.split(','),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas
            retries=3,
            max_in_flight_requests_per_connection=1
        )
        logger.info(f"Kafka producer initialized: {settings.kafka_bootstrap_servers}")

    def publish_inquiry(self, customer_id: str, message_data: Dict[str, Any]) -> bool:
        """
        Publish customer inquiry to Kafka topic

        Args:
            customer_id: Customer identifier (used as partition key)
            message_data: Message payload

        Returns:
            True if published successfully
        """
        try:
            # Add metadata
            message_data['published_at'] = datetime.utcnow().isoformat()
            message_data['customer_id'] = customer_id

            # Publish to topic
            future = self.producer.send(
                settings.kafka_topic_inquiries,
                key=customer_id,
                value=message_data
            )

            # Wait for confirmation
            record_metadata = future.get(timeout=10)

            logger.info(
                f"Published inquiry to Kafka: topic={record_metadata.topic}, "
                f"partition={record_metadata.partition}, offset={record_metadata.offset}"
            )

            return True

        except KafkaError as e:
            logger.error(f"Kafka publish error: {e}", exc_info=True)
            return False

    def publish_response(self, customer_id: str, response_data: Dict[str, Any]) -> bool:
        """
        Publish agent response to Kafka topic

        Args:
            customer_id: Customer identifier
            response_data: Response payload

        Returns:
            True if published successfully
        """
        try:
            response_data['published_at'] = datetime.utcnow().isoformat()
            response_data['customer_id'] = customer_id

            future = self.producer.send(
                settings.kafka_topic_responses,
                key=customer_id,
                value=response_data
            )

            record_metadata = future.get(timeout=10)

            logger.info(
                f"Published response to Kafka: topic={record_metadata.topic}, "
                f"partition={record_metadata.partition}, offset={record_metadata.offset}"
            )

            return True

        except KafkaError as e:
            logger.error(f"Kafka publish error: {e}", exc_info=True)
            return False

    def close(self):
        """Close producer connection"""
        self.producer.close()
        logger.info("Kafka producer closed")


class MessageConsumer:
    """Kafka message consumer for processing customer inquiries"""

    def __init__(self, group_id: Optional[str] = None):
        """
        Initialize Kafka consumer

        Args:
            group_id: Consumer group ID (defaults to settings)
        """
        self.group_id = group_id or settings.kafka_consumer_group

        self.consumer = KafkaConsumer(
            settings.kafka_topic_inquiries,
            bootstrap_servers=settings.kafka_bootstrap_servers.split(','),
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset='earliest',  # Start from beginning if no offset
            enable_auto_commit=False,  # Manual commit for reliability
            max_poll_records=10
        )

        logger.info(
            f"Kafka consumer initialized: group={self.group_id}, "
            f"topic={settings.kafka_topic_inquiries}"
        )

    def consume_messages(self, callback, max_messages: Optional[int] = None):
        """
        Consume messages and process with callback

        Args:
            callback: Function to process each message
            max_messages: Maximum messages to process (None = infinite)
        """
        processed = 0

        try:
            for message in self.consumer:
                try:
                    # Process message
                    logger.info(
                        f"Consuming message: partition={message.partition}, "
                        f"offset={message.offset}, key={message.key}"
                    )

                    # Call callback with message data
                    callback(message.value)

                    # Commit offset
                    self.consumer.commit()

                    processed += 1

                    # Check if reached max
                    if max_messages and processed >= max_messages:
                        logger.info(f"Reached max messages: {max_messages}")
                        break

                except Exception as e:
                    logger.error(f"Message processing error: {e}", exc_info=True)
                    # Continue to next message (don't commit offset)

        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user")

        finally:
            self.close()

        logger.info(f"Processed {processed} messages")

    def close(self):
        """Close consumer connection"""
        self.consumer.close()
        logger.info("Kafka consumer closed")


# Global producer instance
_producer: Optional[MessageProducer] = None


def get_producer() -> MessageProducer:
    """Get global Kafka producer instance"""
    global _producer
    if _producer is None:
        _producer = MessageProducer()
    return _producer


def close_producer():
    """Close global producer"""
    global _producer
    if _producer:
        _producer.close()
        _producer = None
