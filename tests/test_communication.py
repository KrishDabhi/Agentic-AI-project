"""Test suite for JSON-RPC communication."""

import unittest
import json
from communication import MessageProtocol, RPCHandler
from utils import get_logger

logger = get_logger(__name__)


class TestMessageProtocol(unittest.TestCase):
    """Test JSON-RPC message protocol."""

    def test_create_request(self):
        """Test creating a JSON-RPC request."""
        request = MessageProtocol.create_request("monitor_esg", {"company": "TestCorp"})
        
        self.assertEqual(request["jsonrpc"], "2.0")
        self.assertEqual(request["method"], "monitor_esg")
        self.assertIn("id", request)
        self.assertIn("params", request)

    def test_create_response(self):
        """Test creating a JSON-RPC response."""
        response = MessageProtocol.create_response({"result": "success"}, "123")
        
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["id"], "123")
        self.assertIn("result", response)

    def test_create_error(self):
        """Test creating a JSON-RPC error."""
        error = MessageProtocol.create_error(-32601, "Method not found", "123")
        
        self.assertEqual(error["jsonrpc"], "2.0")
        self.assertIn("error", error)
        self.assertEqual(error["error"]["code"], -32601)

    def test_validate_message(self):
        """Test message validation."""
        valid_request = {"jsonrpc": "2.0", "method": "test"}
        invalid_message = {"jsonrpc": "2.0"}
        
        self.assertTrue(MessageProtocol.validate_message(valid_request))
        self.assertFalse(MessageProtocol.validate_message(invalid_message))

    def test_serialize_deserialize(self):
        """Test message serialization and deserialization."""
        original = MessageProtocol.create_request("test", {"data": "value"})
        
        serialized = MessageProtocol.serialize_message(original)
        deserialized = MessageProtocol.deserialize_message(serialized)
        
        self.assertEqual(original["method"], deserialized["method"])


class TestRPCHandler(unittest.TestCase):
    """Test RPC handler functionality."""

    def setUp(self):
        """Set up test handler."""
        self.handler = RPCHandler("test_agent")
        self.handler.register_method("add", lambda a, b: a + b)
        self.handler.register_method("greet", lambda name: f"Hello, {name}!")

    def test_register_method(self):
        """Test method registration."""
        self.assertIn("add", self.handler.methods)
        self.assertIn("greet", self.handler.methods)

    def test_queue_notification(self):
        """Test notification queueing."""
        self.handler.queue_notification("status_update", {"status": "idle"})
        
        messages = self.handler.get_queued_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["method"], "status_update")


if __name__ == "__main__":
    unittest.main()
