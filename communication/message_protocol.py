"""JSON-RPC communication protocol for agent-to-agent communication."""

import json
from typing import Dict, Any, List
from enum import Enum


class MessageType(Enum):
    """Message types for agent communication."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


class MessageProtocol:
    """Define message format and protocol for agent communication."""

    @staticmethod
    def create_request(method: str, params: Dict[str, Any], request_id: str = None) -> Dict[str, Any]:
        """
        Create a JSON-RPC request message.
        
        Args:
            method: Method name to invoke
            params: Parameters for the method
            request_id: Unique request identifier
            
        Returns:
            Formatted request message
        """
        import uuid
        return {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id or str(uuid.uuid4()),
        }

    @staticmethod
    def create_response(result: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """
        Create a JSON-RPC response message.
        
        Args:
            result: Result data
            request_id: Original request ID
            
        Returns:
            Formatted response message
        """
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id,
        }

    @staticmethod
    def create_error(error_code: int, error_message: str, request_id: str = None) -> Dict[str, Any]:
        """
        Create a JSON-RPC error message.
        
        Args:
            error_code: Error code
            error_message: Error description
            request_id: Original request ID
            
        Returns:
            Formatted error message
        """
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": error_code,
                "message": error_message,
            },
            "id": request_id,
        }

    @staticmethod
    def create_notification(method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a JSON-RPC notification message (no response expected).
        
        Args:
            method: Method name to invoke
            params: Parameters for the method
            
        Returns:
            Formatted notification message
        """
        return {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
        }

    @staticmethod
    def validate_message(message: Dict[str, Any]) -> bool:
        """
        Validate message format.
        
        Args:
            message: Message to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["jsonrpc", "method"] if "method" in message else ["jsonrpc", "id"]
        return all(field in message for field in required_fields)

    @staticmethod
    def serialize_message(message: Dict[str, Any]) -> str:
        """
        Serialize message to JSON string.
        
        Args:
            message: Message dictionary
            
        Returns:
            JSON string representation
        """
        return json.dumps(message)

    @staticmethod
    def deserialize_message(json_string: str) -> Dict[str, Any]:
        """
        Deserialize message from JSON string.
        
        Args:
            json_string: JSON string representation
            
        Returns:
            Message dictionary
        """
        return json.loads(json_string)
