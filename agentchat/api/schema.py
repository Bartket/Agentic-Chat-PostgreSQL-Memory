from typing import Dict, List, Optional

from pydantic import UUID4, BaseModel


class ChatInput(BaseModel):
    message: str
    thread_id: str


class Message(BaseModel):
    content: str
    additional_kwargs: Dict  # Empty dictionary in your example
    response_metadata: Dict  # Empty dictionary in your example
    type: str  # "human" or "ai"
    name: Optional[str] = None
    id: UUID4  # Ensures the ID is a valid UUID
    example: bool
    tool_calls: Optional[List] = None  # Only present in "ai" messages
    invalid_tool_calls: Optional[List] = None  # Only present in "ai" messages
    usage_metadata: Optional[Dict] = None  # Only present in "ai" messages


class ChatResponse(BaseModel):
    messages: List[Message]
