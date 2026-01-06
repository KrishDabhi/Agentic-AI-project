"""JSON-RPC server and client implementation for agent communication."""

import json
import asyncio
from typing import Dict, Any, Callable, Optional
from utils.logger import get_logger
from .message_protocol import MessageProtocol

logger = get_logger(__name__)


class RPCHandler:
    """Handle JSON-RPC requests and responses between agents."""

    def __init__(self, agent_name: str):
        """
        Initialize the RPC Handler.
        
        Args:
            agent_name: Name of the agent using this handler
        """
        self.agent_name = agent_name
        self.methods: Dict[str, Callable] = {}
        self.message_queue = []
        logger.info(f"Initialized RPC Handler for {agent_name}")

    def register_method(self, method_name: str, handler: Callable) -> None:
        """
        Register a method to be callable via RPC.
        
        Args:
            method_name: Name of the method
            handler: Callable handler function
        """
        self.methods[method_name] = handler
        logger.info(f"Registered method: {method_name}")

    async def handle_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming RPC request.
        
        Args:
            message: JSON-RPC message
            
        Returns:
            Response message
        """
        request_id = message.get("id")
        method_name = message.get("method")
        params = message.get("params", {})

        if method_name not in self.methods:
            return MessageProtocol.create_error(
                -32601, f"Method '{method_name}' not found", request_id
            )

        try:
            handler = self.methods[method_name]
            if asyncio.iscoroutinefunction(handler):
                result = await handler(**params)
            else:
                result = handler(**params)
            
            return MessageProtocol.create_response(result, request_id)
        except Exception as e:
            logger.error(f"Error executing {method_name}: {str(e)}")
            return MessageProtocol.create_error(
                -32603, f"Internal error: {str(e)}", request_id
            )

    async def send_request(self, target_agent: str, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send RPC request to another agent.
        
        Args:
            target_agent: Name of target agent
            method: Method to invoke
            params: Parameters for the method
            
        Returns:
            Response from target agent
        """
        message = MessageProtocol.create_request(method, params)
        logger.info(f"Sending request to {target_agent}: {method}")
        
        # In a real implementation, this would send via network/queue
        # For now, simulate response
        return {"status": "sent", "message_id": message["id"]}

    def queue_notification(self, method: str, params: Dict[str, Any]) -> None:
        """
        Queue a notification to be sent (no response expected).
        
        Args:
            method: Method name
            params: Parameters
        """
        message = MessageProtocol.create_notification(method, params)
        self.message_queue.append(message)
        logger.info(f"Queued notification: {method}")

    def get_queued_messages(self) -> list:
        """Get all queued messages and clear queue."""
        messages = self.message_queue.copy()
        self.message_queue.clear()
        return messages

    def serialize_message(self, message: Dict[str, Any]) -> str:
        """Serialize message to JSON."""
        return MessageProtocol.serialize_message(message)

    def deserialize_message(self, json_string: str) -> Dict[str, Any]:
        """Deserialize message from JSON."""
        return MessageProtocol.deserialize_message(json_string)
