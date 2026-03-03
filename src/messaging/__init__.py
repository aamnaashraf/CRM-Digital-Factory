"""
Messaging Module
Kafka producer and consumer for async message processing (with fallback to in-memory)
"""

import os
from typing import Union

# Import based on configuration
if os.getenv('USE_SIMPLE_CONFIG', 'true').lower() == 'true':
    from src.config_simple import get_settings
else:
    from src.config import get_settings

settings = get_settings()
use_kafka = bool(settings.kafka_bootstrap_servers)

if use_kafka:
    # Use Kafka implementation
    from .kafka_client import (
        MessageProducer,
        MessageConsumer,
        get_producer,
        close_producer
    )
else:
    # Use in-memory implementation
    from .simple_messaging import (
        SimpleMessageProducer as MessageProducer,
        SimpleMessageConsumer as MessageConsumer,
        get_producer,
        close_producer
    )

__all__ = [
    "MessageProducer",
    "MessageConsumer",
    "get_producer",
    "close_producer"
]
