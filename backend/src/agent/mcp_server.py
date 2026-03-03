"""
TaskFlow AI Customer Success Agent - MCP Server
Exercise 1.4: Model Context Protocol Server

This MCP server exposes agent capabilities as tools:
1. search_kb - Search knowledge base for relevant documentation
2. create_ticket - Create a support ticket in the system
3. get_customer_history - Retrieve customer conversation history
4. escalate_to_human - Escalate conversation to human agent
5. send_response - Send response via appropriate channel
6. analyze_sentiment - Analyze sentiment of customer message
"""

import json
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.core_agent import KnowledgeBase, Channel
from agent.state_manager import StateManager, SentimentAnalyzer


class ToolName(Enum):
    SEARCH_KB = "search_kb"
    CREATE_TICKET = "create_ticket"
    GET_CUSTOMER_HISTORY = "get_customer_history"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    SEND_RESPONSE = "send_response"
    ANALYZE_SENTIMENT = "analyze_sentiment"


@dataclass
class ToolParameter:
    """Parameter definition for a tool"""
    name: str
    type: str
    description: str
    required: bool = True
    enum: Optional[List[str]] = None


@dataclass
class Tool:
    """Tool definition for MCP"""
    name: str
    description: str
    parameters: List[ToolParameter]

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'parameters': [
                {
                    'name': p.name,
                    'type': p.type,
                    'description': p.description,
                    'required': p.required,
                    'enum': p.enum
                }
                for p in self.parameters
            ]
        }


@dataclass
class ToolResult:
    """Result from tool execution"""
    success: bool
    data: Any
    error: Optional[str] = None

    def to_dict(self):
        return {
            'success': self.success,
            'data': self.data,
            'error': self.error
        }


class MCPServer:
    """MCP Server that exposes agent capabilities as tools"""

    def __init__(self, kb_path: str, state_path: str = "data/state.json"):
        self.kb = KnowledgeBase(kb_path)
        self.state = StateManager(state_path)
        self.tools = self._define_tools()

    def _define_tools(self) -> Dict[str, Tool]:
        """Define all available tools"""
        return {
            ToolName.SEARCH_KB.value: Tool(
                name=ToolName.SEARCH_KB.value,
                description="Search the knowledge base for relevant product documentation and help articles",
                parameters=[
                    ToolParameter(
                        name="query",
                        type="string",
                        description="The search query or customer question"
                    ),
                    ToolParameter(
                        name="max_results",
                        type="integer",
                        description="Maximum number of results to return",
                        required=False
                    )
                ]
            ),

            ToolName.CREATE_TICKET.value: Tool(
                name=ToolName.CREATE_TICKET.value,
                description="Create a support ticket for tracking customer issues",
                parameters=[
                    ToolParameter(
                        name="customer_id",
                        type="string",
                        description="Customer email or phone number"
                    ),
                    ToolParameter(
                        name="subject",
                        type="string",
                        description="Ticket subject/title"
                    ),
                    ToolParameter(
                        name="description",
                        type="string",
                        description="Detailed description of the issue"
                    ),
                    ToolParameter(
                        name="channel",
                        type="string",
                        description="Channel where issue was reported",
                        enum=["email", "whatsapp", "web"]
                    ),
                    ToolParameter(
                        name="priority",
                        type="string",
                        description="Ticket priority level",
                        enum=["low", "medium", "high", "urgent"],
                        required=False
                    )
                ]
            ),

            ToolName.GET_CUSTOMER_HISTORY.value: Tool(
                name=ToolName.GET_CUSTOMER_HISTORY.value,
                description="Retrieve conversation history and context for a customer",
                parameters=[
                    ToolParameter(
                        name="customer_id",
                        type="string",
                        description="Customer email or phone number"
                    ),
                    ToolParameter(
                        name="limit",
                        type="integer",
                        description="Maximum number of messages to retrieve",
                        required=False
                    )
                ]
            ),

            ToolName.ESCALATE_TO_HUMAN.value: Tool(
                name=ToolName.ESCALATE_TO_HUMAN.value,
                description="Escalate conversation to a human agent",
                parameters=[
                    ToolParameter(
                        name="conversation_id",
                        type="string",
                        description="ID of the conversation to escalate"
                    ),
                    ToolParameter(
                        name="reason",
                        type="string",
                        description="Reason for escalation",
                        enum=["billing", "security", "legal", "compliance",
                              "enterprise_sales", "technical", "churn_threat"]
                    ),
                    ToolParameter(
                        name="notes",
                        type="string",
                        description="Additional context for human agent",
                        required=False
                    )
                ]
            ),

            ToolName.SEND_RESPONSE.value: Tool(
                name=ToolName.SEND_RESPONSE.value,
                description="Send a response to customer via appropriate channel",
                parameters=[
                    ToolParameter(
                        name="customer_id",
                        type="string",
                        description="Customer email or phone number"
                    ),
                    ToolParameter(
                        name="channel",
                        type="string",
                        description="Channel to send response through",
                        enum=["email", "whatsapp", "web"]
                    ),
                    ToolParameter(
                        name="message",
                        type="string",
                        description="Message content to send"
                    ),
                    ToolParameter(
                        name="conversation_id",
                        type="string",
                        description="ID of the conversation",
                        required=False
                    )
                ]
            ),

            ToolName.ANALYZE_SENTIMENT.value: Tool(
                name=ToolName.ANALYZE_SENTIMENT.value,
                description="Analyze sentiment of customer message",
                parameters=[
                    ToolParameter(
                        name="text",
                        type="string",
                        description="Text to analyze for sentiment"
                    )
                ]
            )
        }

    def list_tools(self) -> List[Dict]:
        """List all available tools"""
        return [tool.to_dict() for tool in self.tools.values()]

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """Execute a tool with given parameters"""
        if tool_name not in self.tools:
            return ToolResult(
                success=False,
                data=None,
                error=f"Unknown tool: {tool_name}"
            )

        try:
            # Route to appropriate handler
            if tool_name == ToolName.SEARCH_KB.value:
                return self._search_kb(parameters)
            elif tool_name == ToolName.CREATE_TICKET.value:
                return self._create_ticket(parameters)
            elif tool_name == ToolName.GET_CUSTOMER_HISTORY.value:
                return self._get_customer_history(parameters)
            elif tool_name == ToolName.ESCALATE_TO_HUMAN.value:
                return self._escalate_to_human(parameters)
            elif tool_name == ToolName.SEND_RESPONSE.value:
                return self._send_response(parameters)
            elif tool_name == ToolName.ANALYZE_SENTIMENT.value:
                return self._analyze_sentiment(parameters)
            else:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Tool not implemented: {tool_name}"
                )

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"Tool execution error: {str(e)}"
            )

    def _search_kb(self, params: Dict) -> ToolResult:
        """Search knowledge base"""
        query = params.get('query', '')
        max_results = params.get('max_results', 3)

        results = self.kb.search(query)[:max_results]

        return ToolResult(
            success=True,
            data={
                'query': query,
                'results': results,
                'count': len(results)
            }
        )

    def _create_ticket(self, params: Dict) -> ToolResult:
        """Create a support ticket"""
        customer_id = params['customer_id']
        subject = params['subject']
        description = params['description']
        channel = params['channel']
        priority = params.get('priority', 'medium')

        # Get or create customer
        customer = self.state.get_or_create_customer(
            customer_id,
            channel=channel
        )

        # Create conversation (acts as ticket)
        conversation = self.state.get_or_create_conversation(
            customer_id,
            channel=channel,
            subject=subject
        )

        # Add initial message
        sentiment = SentimentAnalyzer.analyze(description)
        self.state.add_message_to_conversation(
            conversation,
            sender="customer",
            content=description,
            sentiment=sentiment,
            channel=channel
        )

        # Save state
        self.state.save_state()

        return ToolResult(
            success=True,
            data={
                'ticket_id': conversation.conversation_id,
                'customer_id': customer_id,
                'subject': subject,
                'priority': priority,
                'status': conversation.status,
                'created_at': conversation.created_at
            }
        )

    def _get_customer_history(self, params: Dict) -> ToolResult:
        """Get customer conversation history"""
        customer_id = params['customer_id']
        limit = params.get('limit', 10)

        context = self.state.get_customer_context(customer_id)

        if not context:
            return ToolResult(
                success=False,
                data=None,
                error=f"Customer not found: {customer_id}"
            )

        return ToolResult(
            success=True,
            data=context
        )

    def _escalate_to_human(self, params: Dict) -> ToolResult:
        """Escalate conversation to human agent"""
        conversation_id = params['conversation_id']
        reason = params['reason']
        notes = params.get('notes', '')

        # Find conversation
        conversation = self.state.conversations.get(conversation_id)

        if not conversation:
            return ToolResult(
                success=False,
                data=None,
                error=f"Conversation not found: {conversation_id}"
            )

        # Escalate
        escalation_reason = f"{reason}: {notes}" if notes else reason
        self.state.escalate_conversation(conversation, escalation_reason)
        self.state.save_state()

        return ToolResult(
            success=True,
            data={
                'conversation_id': conversation_id,
                'escalated': True,
                'reason': escalation_reason,
                'status': conversation.status
            }
        )

    def _send_response(self, params: Dict) -> ToolResult:
        """Send response to customer"""
        customer_id = params['customer_id']
        channel = params['channel']
        message = params['message']
        conversation_id = params.get('conversation_id')

        # Get or create conversation
        if conversation_id and conversation_id in self.state.conversations:
            conversation = self.state.conversations[conversation_id]
        else:
            conversation = self.state.get_or_create_conversation(
                customer_id,
                channel=channel
            )

        # Add agent message
        sentiment = 0.5  # Agent messages are generally positive/helpful
        self.state.add_message_to_conversation(
            conversation,
            sender="agent",
            content=message,
            sentiment=sentiment,
            channel=channel
        )

        self.state.save_state()

        # In production, this would actually send via email/WhatsApp/web
        return ToolResult(
            success=True,
            data={
                'sent': True,
                'customer_id': customer_id,
                'channel': channel,
                'conversation_id': conversation.conversation_id,
                'message_length': len(message)
            }
        )

    def _analyze_sentiment(self, params: Dict) -> ToolResult:
        """Analyze sentiment of text"""
        text = params['text']
        sentiment_score = SentimentAnalyzer.analyze(text)

        # Classify sentiment
        if sentiment_score >= 0.5:
            classification = "positive"
        elif sentiment_score >= 0.2:
            classification = "slightly_positive"
        elif sentiment_score >= -0.2:
            classification = "neutral"
        elif sentiment_score >= -0.5:
            classification = "slightly_negative"
        else:
            classification = "negative"

        return ToolResult(
            success=True,
            data={
                'text': text[:100] + "..." if len(text) > 100 else text,
                'sentiment_score': sentiment_score,
                'classification': classification,
                'requires_attention': sentiment_score < -0.5
            }
        )


def test_mcp_server():
    """Test MCP server functionality"""
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 80)
    print("MCP SERVER TEST")
    print("=" * 80)
    print()

    # Initialize server
    kb_path = os.path.join('context', 'product-docs.md')
    server = MCPServer(kb_path, "data/mcp_test_state.json")

    # Test 1: List tools
    print("Test 1: List Available Tools")
    print("-" * 80)
    tools = server.list_tools()
    for tool in tools:
        print(f"✓ {tool['name']}: {tool['description']}")
    print(f"\nTotal tools: {len(tools)}")
    print()

    # Test 2: Search KB
    print("Test 2: Search Knowledge Base")
    print("-" * 80)
    result = server.execute_tool(ToolName.SEARCH_KB.value, {
        'query': 'How do I set up recurring tasks?',
        'max_results': 2
    })
    print(f"Success: {result.success}")
    print(f"Results found: {result.data['count']}")
    if result.data['results']:
        print(f"First result preview: {result.data['results'][0][:100]}...")
    print()

    # Test 3: Create ticket
    print("Test 3: Create Support Ticket")
    print("-" * 80)
    result = server.execute_tool(ToolName.CREATE_TICKET.value, {
        'customer_id': 'test.user@example.com',
        'subject': 'Slack integration not working',
        'description': 'I connected Slack but notifications are not coming through. Very frustrated!',
        'channel': 'email',
        'priority': 'high'
    })
    print(f"Success: {result.success}")
    print(f"Ticket ID: {result.data['ticket_id']}")
    print(f"Status: {result.data['status']}")
    ticket_id = result.data['ticket_id']
    print()

    # Test 4: Analyze sentiment
    print("Test 4: Analyze Sentiment")
    print("-" * 80)
    test_messages = [
        "This is amazing! Love the new features!",
        "The app is okay, nothing special.",
        "This is terrible. I want a refund immediately!"
    ]
    for msg in test_messages:
        result = server.execute_tool(ToolName.ANALYZE_SENTIMENT.value, {
            'text': msg
        })
        print(f"Message: {msg}")
        print(f"  Score: {result.data['sentiment_score']:.2f}")
        print(f"  Classification: {result.data['classification']}")
        print(f"  Requires attention: {result.data['requires_attention']}")
        print()

    # Test 5: Get customer history
    print("Test 5: Get Customer History")
    print("-" * 80)
    result = server.execute_tool(ToolName.GET_CUSTOMER_HISTORY.value, {
        'customer_id': 'test.user@example.com',
        'limit': 5
    })
    print(f"Success: {result.success}")
    print(f"Customer: {result.data['customer']['name']}")
    print(f"Total messages: {len(result.data['recent_messages'])}")
    print(f"Average sentiment: {result.data['average_sentiment']:.2f}")
    print()

    # Test 6: Escalate to human
    print("Test 6: Escalate to Human")
    print("-" * 80)
    result = server.execute_tool(ToolName.ESCALATE_TO_HUMAN.value, {
        'conversation_id': ticket_id,
        'reason': 'technical',
        'notes': 'Customer frustrated, integration issue requires engineering review'
    })
    print(f"Success: {result.success}")
    print(f"Escalated: {result.data['escalated']}")
    print(f"Reason: {result.data['reason']}")
    print()

    # Test 7: Send response
    print("Test 7: Send Response")
    print("-" * 80)
    result = server.execute_tool(ToolName.SEND_RESPONSE.value, {
        'customer_id': 'test.user@example.com',
        'channel': 'email',
        'message': 'Thank you for your patience. Our engineering team is investigating the Slack integration issue.',
        'conversation_id': ticket_id
    })
    print(f"Success: {result.success}")
    print(f"Sent: {result.data['sent']}")
    print(f"Channel: {result.data['channel']}")
    print()

    print("=" * 80)
    print("MCP SERVER TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_mcp_server()
