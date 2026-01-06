# communication/rpc_handler.py

import json
import http.server
import socketserver
import threading
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse, parse_qs
import requests

from .message_protocol import JSONRPCRequest, JSONRPCResponse, AVAILABLE_METHODS, create_error_response
from utils.logger import get_logger

logger = get_logger(__name__)

class JSONRPCServer(http.server.BaseHTTPRequestHandler):
    """Simple HTTP-based JSON-RPC server."""
    
    # Class-level storage for registered handlers (for demo purposes)
    _handlers = {}

    @classmethod
    def register_method(cls, method_name: str, handler_func):
        """Register a function to handle a specific RPC method."""
        cls._handlers[method_name] = handler_func
        logger.info(f"Registered RPC method: {method_name}")

    def do_POST(self):
        """Handle POST requests containing JSON-RPC calls."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            request_json = json.loads(post_data)
            request = JSONRPCRequest.from_dict(request_json)
        except Exception as e:
            logger.error(f"Invalid JSON-RPC request: {e}")
            error_response = create_error_response(-32700, "Parse error", None)
            self._send_response(error_response.to_dict())
            return

        # Validate method
        if request.method not in self._handlers:
            error_response = create_error_response(-32601, f"Method not found: {request.method}", request.id)
            self._send_response(error_response.to_dict())
            return

        # Execute method
        try:
            result = self._handlers[request.method](**request.params)
            response = JSONRPCResponse(result=result, request_id=request.id)
        except Exception as e:
            logger.error(f"Error executing method '{request.method}': {e}")
            error_response = create_error_response(-32603, f"Internal error: {str(e)}", request.id)
            self._send_response(error_response.to_dict())
            return

        self._send_response(response.to_dict())

    def _send_response(self, response_data: Dict[str, Any]):
        """Send JSON-RPC response back to client."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

class JSONRPCClient:
    """Client to send JSON-RPC requests to a server."""
    
    def __init__(self, server_url: str):
        self.server_url = server_url

    def call(self, method: str, params: Optional[Dict[str, Any]] = None, request_id: Optional[int] = None) -> Any:
        """Call a remote method via JSON-RPC."""
        request = JSONRPCRequest(method=method, params=params, request_id=request_id)
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(self.server_url, data=json.dumps(request.to_dict()), headers=headers)
            response.raise_for_status()
            response_json = response.json()
            response_obj = JSONRPCResponse.from_dict(response_json)

            if response_obj.error:
                raise Exception(f"RPC Error {response_obj.error.get('code')}: {response_obj.error.get('message')}")

            return response_obj.result

        except Exception as e:
            logger.error(f"RPC Client error calling {method}: {e}")
            raise

# --- Example usage for Agent Coordination ---

# Global server instance (for demo; in real system, each agent might run its own server)
_server_instance = None
_server_thread = None

def start_rpc_server(host: str = "localhost", port: int = 8000):
    """Start the JSON-RPC server in a separate thread."""
    global _server_instance, _server_thread
    if _server_instance is None:
        with socketserver.TCPServer((host, port), JSONRPCServer) as server:
            _server_instance = server
            logger.info(f"JSON-RPC Server started at http://{host}:{port}")
            _server_thread = threading.Thread(target=server.serve_forever)
            _server_thread.daemon = True
            _server_thread.start()

def stop_rpc_server():
    """Stop the JSON-RPC server."""
    global _server_instance, _server_thread
    if _server_instance:
        _server_instance.shutdown()
        _server_thread.join()
        logger.info("JSON-RPC Server stopped.")

# --- Helper to Register Agents' Methods ---

def register_agent_methods(planner_agent, executor_agent, validator_agent):
    """Register agent methods with the RPC server."""
    
    # Planner Agent Method
    def plan_monitoring_strategy(user_query: str) -> Dict[str, Any]:
        return planner_agent.plan_monitoring_strategy(user_query)

    # Executor Agent Method
    def execute_task(task: Dict[str, Any]) -> Dict[str, Any]:
        return executor_agent.execute_task(task)

    # Validator Agent Method
    def validate_result(result: Dict[str, Any]) -> Dict[str, Any]:
        return validator_agent.validate_result(result)

    # Register methods
    JSONRPCServer.register_method("planner.plan_monitoring_strategy", plan_monitoring_strategy)
    JSONRPCServer.register_method("executor.execute_task", execute_task)
    JSONRPCServer.register_method("validator.validate_result", validate_result)

    logger.info("All agent methods registered with RPC server.")