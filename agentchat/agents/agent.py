# Import relevant functionality
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from agentchat.core import settings
from langchain_core.prompts import ChatPromptTemplate

from agentchat.agents.tools import tools_for_agent

# Create the agent
model = ChatOpenAI(
    model_name=settings.MODEL_NAME, api_key=settings.OPENAI_API_KEY, temperature=0.6
)

# Get the prompt to use - you can modify this!
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a React-based AI assistant with access to some basic tools.

         Be sure to input a good defined question to the tool.
""",
        ),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(model, tools_for_agent, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools_for_agent,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=2,
)
