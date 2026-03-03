"""
Settings Management Endpoints
API endpoints for managing application settings
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.database.connection import get_db_session
from src.config_simple import get_settings

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


class SettingsRequest(BaseModel):
    """Request model for updating settings"""
    auto_response: bool = None
    sentiment_analysis: bool = None
    escalation_alerts: bool = None
    daily_reports: bool = None
    openai_api_key: str = None
    openai_model: str = None


class SettingsResponse(BaseModel):
    """Response model for settings"""
    auto_response: bool
    sentiment_analysis: bool
    escalation_alerts: bool
    daily_reports: bool
    openai_api_key: str  # This will be masked
    openai_model: str


@router.get("/")
async def get_settings():
    """
    Get current application settings
    """
    try:
        # Return current settings from config
        # In a real implementation, you might load from database
        # For now, return defaults with some placeholder values
        return SettingsResponse(
            auto_response=True,
            sentiment_analysis=True,
            escalation_alerts=True,
            daily_reports=False,
            openai_api_key="sk-••••••••••••••••",  # Masked for security
            openai_model="llama3-70b-8192"
        )
    except Exception as e:
        logger.error(f"Get settings error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch settings"
        )


@router.post("/")
async def update_settings(settings_request: SettingsRequest):
    """
    Update application settings
    """
    try:
        # In a real implementation, you would save settings to database
        # For now, just return the updated settings without persisting

        # Create response with provided values or current values
        response_data = {
            "auto_response": settings_request.auto_response if settings_request.auto_response is not None
                            else True,
            "sentiment_analysis": settings_request.sentiment_analysis if settings_request.sentiment_analysis is not None
                                else True,
            "escalation_alerts": settings_request.escalation_alerts if settings_request.escalation_alerts is not None
                               else True,
            "daily_reports": settings_request.daily_reports if settings_request.daily_reports is not None
                           else False,
            "openai_api_key": settings_request.openai_api_key if settings_request.openai_api_key
                            else "sk-••••••••••••••••",
            "openai_model": settings_request.openai_model if settings_request.openai_model
                          else "llama3-70b-8192"
        }

        return SettingsResponse(**response_data)
    except Exception as e:
        logger.error(f"Update settings error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update settings"
        )