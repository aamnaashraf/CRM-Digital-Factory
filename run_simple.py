"""
Simple Startup Script for TaskFlow AI Customer Success Agent
This script runs the application with simplified configuration (SQLite, no Kafka, etc.)
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

def setup_environment():
    """Set up environment variables for simplified configuration"""
    # Set default environment variables for simplified setup
    os.environ['USE_SIMPLE_CONFIG'] = 'true'  # Use simplified config

    if not os.getenv('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./taskflow_crm.db'  # Use async SQLite

    if not os.getenv('KAFKA_BOOTSTRAP_SERVERS'):
        os.environ['KAFKA_BOOTSTRAP_SERVERS'] = ''  # Empty means disabled

    if not os.getenv('REDIS_URL'):
        os.environ['REDIS_URL'] = ''  # Empty means disabled

    if not os.getenv('APP_ENV'):
        os.environ['APP_ENV'] = 'development'

    if not os.getenv('DEBUG'):
        os.environ['DEBUG'] = 'true'

    if not os.getenv('ENABLE_METRICS'):
        os.environ['ENABLE_METRICS'] = 'false'

    if not os.getenv('USE_GROQ'):
        os.environ['USE_GROQ'] = 'true'  # Use Groq by default in simplified mode

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'openai',
        'pydantic',
        'pydantic_settings',  # Changed from pydantic-settings to pydantic_settings
        'sqlalchemy.ext.asyncio'  # Changed format
    ]

    missing_packages = []
    for package in required_packages:
        try:
            # Handle the import differently based on package name
            if package == 'sqlalchemy.ext.asyncio':
                __import__('sqlalchemy.ext.asyncio')
            elif package == 'pydantic_settings':
                __import__('pydantic_settings')
            else:
                __import__(package.split('.')[0])  # Just import the main package name
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements-simple.txt")
        return False
    return True

async def run_migrations():
    """Run database migrations to create tables"""
    print("Running database migrations...")
    try:
        # Make sure we're using the simplified config
        from src.config_simple import get_settings
        from src.database.connection import init_database, get_db_manager

        settings = get_settings()
        print(f"Using database URL: {settings.database_url}")
        init_database(settings.database_url)
        db_manager = get_db_manager()
        await db_manager.create_tables()
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error running migrations: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to start the simplified application"""
    print("Starting TaskFlow AI Customer Success Agent (Simplified Version)")
    print("=" * 65)
    print("Configuration: SQLite database, in-memory messaging, OpenAI integration")
    print("=" * 65)

    # Setup environment
    setup_environment()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Run migrations
    if not asyncio.run(run_migrations()):
        print("Failed to run database migrations. Exiting...")
        sys.exit(1)

    # Start the application
    print("\nStarting FastAPI application on http://localhost:8000")
    print("Press Ctrl+C to stop the server\n")

    try:
        from src.config_simple import get_settings
        settings = get_settings()

        import uvicorn
        uvicorn.run(
            "src.main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=settings.is_development,
            log_level=settings.log_level.lower()
        )
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()