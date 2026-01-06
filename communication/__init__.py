"""Communication module for agent-to-agent interaction."""

from .rpc_handler import RPCHandler
from .message_protocol import MessageProtocol, MessageType

__all__ = ['RPCHandler', 'MessageProtocol', 'MessageType']
