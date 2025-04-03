from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

from agentchat.agents.agent import agent_executor


class ChatState(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(ChatState)


def chatbot(state: ChatState) -> ChatState:
    """Chatbot function that invokes the inner graph."""
    answer = agent_executor.invoke({"input": state["messages"]}).get("output")
    return {"messages": [{"role": "ai", "content": answer}]}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
