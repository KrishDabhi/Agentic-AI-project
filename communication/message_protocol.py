# communication/message_protocol.py

import json
from typing import Any, Dict, List, Optional

class JSONRPCRequest:
    """Represents a JSON-RPC request."""
    
    def __init__(self, method: str, params: Optional[Dict[str, Any]] = None, request_id: Optional[int] = None):
        self.method = method
        self.params = params or {}
        self.id = request_id  # Can be int, str, or null

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "jsonrpc": "2.0",
            "method": self.method,
            "params": self.params,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JSONRPCRequest':
        """Create from dictionary."""
        return cls(
            method=data["method"],
            params=data.get("params", {}),
            request_id=data.get("id")
        )

class JSONRPCResponse:
    """Represents a JSON-RPC response."""
    
    def __init__(self, result: Any = None, error: Optional[Dict[str, Any]] = None, request_id: Optional[int] = None):
        self.result = result
        self.error = error
        self.id = request_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        response = {"jsonrpc": "2.0"}
        if self.error is not None:
            response["error"] = self.error
        else:
            response["result"] = self.result
        if self.id is not None:
            response["id"] = self.id
        return response

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JSONRPCResponse':
        """Create from dictionary."""
        return cls(
            result=data.get("result"),
            error=data.get("error"),
            request_id=data.get("id")
        )

# Define available methods(this is your API contract)
AVAILABLE_METHODS = {
    "planner.plan_monitoring_strategy": "Plan ESG monitoring strategy based on user query.",
    "executor.execute_task": "Execute a single monitoring task.",
    "validator.validate_result": "Validate execution results."
}

def create_error_response(error_code: int, error_message: str, request_id: Optional[int] = None) -> JSONRPCResponse:
    """Helper to create standardized error responses."""
    return JSONRPCResponse(
        error={
            "code": error_code,
            "message": error_message,
            "data": None
        },
        request_id=request_id
    )