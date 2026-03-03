"""
Tests for Production Agent
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from src.agent.production_agent import ProductionAgent, AgentContext, AgentResponse
from src.database.models import ChannelType, EscalationReason


@pytest.fixture
def mock_session():
    """Mock database session"""
    return AsyncMock()


@pytest.fixture
def agent(mock_session):
    """Create agent instance with mocked dependencies"""
    with patch('src.agent.production_agent.AsyncOpenAI'):
        return ProductionAgent(mock_session)


@pytest.mark.asyncio
async def test_sentiment_analysis_positive(agent):
    """Test sentiment analysis with positive message"""
    text = "I love this product! It's amazing and works perfectly!"

    with patch.object(agent.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_create.return_value = Mock(
            choices=[Mock(message=Mock(content="0.8"))]
        )

        score = await agent._analyze_sentiment(text)

        assert score == 0.8
        assert mock_create.called


@pytest.mark.asyncio
async def test_sentiment_analysis_negative(agent):
    """Test sentiment analysis with negative message"""
    text = "This is terrible! I want a refund immediately!"

    with patch.object(agent.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_create.return_value = Mock(
            choices=[Mock(message=Mock(content="-0.9"))]
        )

        score = await agent._analyze_sentiment(text)

        assert score == -0.9


@pytest.mark.asyncio
async def test_escalation_churn_threat(agent):
    """Test escalation detection for churn threat"""
    context = AgentContext(
        customer_id="test@example.com",
        customer_name="Test User",
        channel=ChannelType.EMAIL,
        message="I want to cancel my subscription and get a refund!",
        subject="Cancellation"
    )

    should_escalate, reason = await agent._check_escalation(context, -0.8)

    assert should_escalate is True
    assert reason == EscalationReason.CHURN_THREAT


@pytest.mark.asyncio
async def test_escalation_security(agent):
    """Test escalation detection for security issue"""
    context = AgentContext(
        customer_id="test@example.com",
        customer_name="Test User",
        channel=ChannelType.EMAIL,
        message="My account has been locked and I can't access it!",
        subject="Account locked"
    )

    should_escalate, reason = await agent._check_escalation(context, -0.3)

    assert should_escalate is True
    assert reason == EscalationReason.SECURITY


@pytest.mark.asyncio
async def test_escalation_billing(agent):
    """Test escalation detection for billing issue"""
    context = AgentContext(
        customer_id="test@example.com",
        customer_name="Test User",
        channel=ChannelType.WEB,
        message="I was charged twice this month!",
        subject="Billing issue"
    )

    should_escalate, reason = await agent._check_escalation(context, -0.5)

    assert should_escalate is True
    assert reason == EscalationReason.BILLING


@pytest.mark.asyncio
async def test_no_escalation_simple_question(agent):
    """Test no escalation for simple question"""
    context = AgentContext(
        customer_id="test@example.com",
        customer_name="Test User",
        channel=ChannelType.WHATSAPP,
        message="How do I set up recurring tasks?",
        subject=""
    )

    should_escalate, reason = await agent._check_escalation(context, 0.0)

    assert should_escalate is False
    assert reason is None


@pytest.mark.asyncio
async def test_channel_adaptation_email(agent):
    """Test response formatting for email channel"""
    context = AgentContext(
        customer_id="test@example.com",
        customer_name="John Doe",
        channel=ChannelType.EMAIL,
        message="How do I export data?",
        subject="Data export"
    )

    response = await agent._generate_escalation_response(
        context,
        EscalationReason.TECHNICAL
    )

    assert "Hi John" in response
    assert "Best regards" in response
    assert "TaskFlow Support Team" in response
    assert len(response) > 100  # Email should be longer


@pytest.mark.asyncio
async def test_channel_adaptation_whatsapp(agent):
    """Test response formatting for WhatsApp channel"""
    context = AgentContext(
        customer_id="+1234567890",
        customer_name="Jane Smith",
        channel=ChannelType.WHATSAPP,
        message="Need help!",
        subject=""
    )

    response = await agent._generate_escalation_response(
        context,
        EscalationReason.TECHNICAL
    )

    assert "Hey Jane" in response or "Hi Jane" in response
    assert "👋" in response  # Should have emoji
    assert len(response) < 200  # WhatsApp should be shorter


@pytest.mark.asyncio
async def test_fallback_response(agent):
    """Test fallback response when AI fails"""
    response = agent._get_fallback_response(ChannelType.EMAIL)

    assert "technical difficulties" in response.lower()
    assert "TaskFlow" in response


@pytest.mark.asyncio
async def test_process_message_success(agent):
    """Test full message processing"""
    context = AgentContext(
        customer_id="test@example.com",
        customer_name="Test User",
        channel=ChannelType.WEB,
        message="How do I create a project?",
        subject="Project creation"
    )

    with patch.object(agent, '_analyze_sentiment', return_value=0.0):
        with patch.object(agent, '_check_escalation', return_value=(False, None)):
            with patch.object(agent, '_generate_response', return_value="Here's how to create a project..."):

                response = await agent.process_message(context)

                assert isinstance(response, AgentResponse)
                assert response.should_escalate is False
                assert response.response_text == "Here's how to create a project..."
                assert response.sentiment_score == 0.0
                assert response.processing_time_ms > 0


@pytest.mark.asyncio
async def test_process_message_with_escalation(agent):
    """Test message processing with escalation"""
    context = AgentContext(
        customer_id="test@example.com",
        customer_name="Test User",
        channel=ChannelType.EMAIL,
        message="I want a refund!",
        subject="Refund request"
    )

    with patch.object(agent, '_analyze_sentiment', return_value=-0.8):
        with patch.object(agent, '_check_escalation', return_value=(True, EscalationReason.CHURN_THREAT)):
            with patch.object(agent, '_generate_escalation_response', return_value="We've escalated your request..."):

                response = await agent.process_message(context)

                assert response.should_escalate is True
                assert response.escalation_reason == EscalationReason.CHURN_THREAT
                assert response.sentiment_score == -0.8
