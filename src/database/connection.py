"""
Database Connection and Session Management
Production-grade database setup with connection pooling (supports PostgreSQL and SQLite)
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool, StaticPool
from sqlalchemy import event, text
import logging

from .models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and sessions"""

    def __init__(self, database_url: str, pool_size: int = 20, max_overflow: int = 10):
        """
        Initialize database manager

        Args:
            database_url: PostgreSQL or SQLite connection URL
            pool_size: Number of connections to maintain
            max_overflow: Maximum overflow connections
        """
        # Configure engine based on database type
        if database_url.startswith("sqlite"):
            # Configure for async SQLite
            self.engine: AsyncEngine = create_async_engine(
                database_url,
                poolclass=StaticPool,
                connect_args={
                    "check_same_thread": False  # Required for SQLite
                },
                echo=False  # Set to True for SQL logging in development
            )

            # Add SQLite-specific pragmas for better performance (only for non-async engines)
            # For aiosqlite, we can't use event listeners the same way
            # SQLite pragmas will be handled automatically by aiosqlite
        else:
            # Convert postgresql:// to postgresql+asyncpg://
            if database_url.startswith("postgresql://"):
                database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

            self.engine: AsyncEngine = create_async_engine(
                database_url,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_pre_ping=True,  # Verify connections before using
                echo=False,  # Set to True for SQL logging in development
            )

        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

        logger.info(f"Database engine created with URL: {database_url}")

    async def create_tables(self):
        """Create all tables in the database"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")

    async def drop_tables(self):
        """Drop all tables (use with caution!)"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.warning("Database tables dropped")

    async def close(self):
        """Close database connections"""
        await self.engine.dispose()
        logger.info("Database connections closed")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get a database session

        Usage:
            async with db_manager.get_session() as session:
                result = await session.execute(query)
        """
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()

    async def health_check(self) -> bool:
        """Check database connectivity"""
        try:
            async with self.get_session() as session:
                if "sqlite" in str(self.engine.url):
                    await session.execute(text("SELECT 1"))
                else:
                    await session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global database manager instance
db_manager: DatabaseManager | None = None


def init_database(database_url: str, pool_size: int = 20, max_overflow: int = 10) -> DatabaseManager:
    """Initialize global database manager"""
    global db_manager
    db_manager = DatabaseManager(database_url, pool_size, max_overflow)
    return db_manager


def get_db_manager() -> DatabaseManager:
    """Get global database manager instance"""
    if db_manager is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return db_manager


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI endpoints

    Usage:
        @app.get("/customers/{customer_id}")
        async def get_customer(
            customer_id: str,
            session: AsyncSession = Depends(get_db_session)
        ):
            result = await session.execute(select(Customer).where(...))
    """
    db = get_db_manager()
    async with db.get_session() as session:
        yield session
