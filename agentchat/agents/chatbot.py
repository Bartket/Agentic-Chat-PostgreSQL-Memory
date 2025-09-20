from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

from agentchat.agents.chain import chain


class ChatState(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(ChatState)


def chatbot(state: ChatState) -> ChatState:
    """Chatbot function that invokes the inner graph."""
    # Pass the latest human message to the chain
    ai_message = chain.invoke({"input": state["messages"]})
    # ai_message is an AIMessage object
    answer = ai_message.content
    return {"messages": [{"role": "ai", "content": answer}]}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
