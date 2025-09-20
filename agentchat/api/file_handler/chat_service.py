from langgraph.utils.runnable import RunnableConfig
from fastapi import Request

class ChatService:
    @staticmethod
    def create_upload_message(filename: str, content: str) -> str:
        return f"""I've uploaded a file: {filename}

File content:
{content}

Please let me know what you'd like me to do with this file. For example:
- Analyze the content for fitness/workout information
- Create a workout plan based on the information
- Answer questions about the content
- Summarize the key points
- Or any other specific instructions you have

What would you like me to help you with regarding this file?"""

    @staticmethod
    async def send_to_chat(request: Request, message_content: str, thread_id: str, graph_builder):
        config = RunnableConfig(configurable={"thread_id": thread_id})
        chat_instance = graph_builder.compile(checkpointer=request.state.checkpointer)
        
        async for event in chat_instance.astream(
            {"messages": [{"role": "user", "content": message_content}]},
            config=config,
            stream_mode="values",
        ):
            last_event = event
        
        return last_event