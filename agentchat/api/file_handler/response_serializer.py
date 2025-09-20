class ResponseSerializer:
    @staticmethod
    def serialize_chat_response(last_event):
        if last_event and "messages" in last_event:
            serialized_messages = []
            for msg in last_event["messages"]:
                if hasattr(msg, 'content') and hasattr(msg, 'type'):
                    serialized_messages.append({
                        "type": msg.type,
                        "content": msg.content
                    })
                else:
                    serialized_messages.append(str(msg))
            return {"messages": serialized_messages}
        else:
            return {"raw_response": str(last_event) if last_event else None}

    @staticmethod
    def create_success_response(filename: str, thread_id: str, content_size: int, chat_response):
        return {
            "message": "File uploaded and sent to chat successfully",
            "filename": filename,
            "thread_id": thread_id,
            "size": content_size,
            "chat_response": chat_response
        }

    @staticmethod
    def create_partial_success_response(filename: str, thread_id: str, content_size: int, content_preview: str):
        return {
            "message": "File uploaded successfully, but failed to send to chat",
            "filename": filename,
            "thread_id": thread_id,
            "size": content_size,
            "error": "Chat processing failed",
            "content_preview": content_preview
        }