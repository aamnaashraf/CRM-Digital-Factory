"""
Test Configuration
Pytest configuration and fixtures
"""

import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.database.models import Base


# Test database URL (use in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create test database session

    Creates a fresh in-memory database for each test
    """
    # Create engine
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session

    # Cleanup
    await engine.dispose()


@pytest.fixture
def sample_customer_data():
    """Sample customer data for tests"""
    return {
        "customer_id": "test@example.com",
        "primary_email": "test@example.com",
        "name": "Test User",
        "company": "Test Company",
        "plan_type": "pro"
    }


@pytest.fixture
def sample_message_data():
    """Sample message data for tests"""
    return {
        "channel": "email",
        "message": "How do I set up recurring tasks?",
        "subject": "Recurring tasks question",
        "priority": "medium"
    }
