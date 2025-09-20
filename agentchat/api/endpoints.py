from fastapi import APIRouter, FastAPI, Request, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from typing import Any, AsyncGenerator
from langgraph.utils.runnable import RunnableConfig
from agentchat.api.schema import ChatInput, ChatResponse
from agentchat.core import settings
from agentchat.agents.chatbot import graph_builder

from .file_handler.validators import FileValidator
from .file_handler.file_processor import FileProcessor
from .file_handler.chat_service import ChatService
from .file_handler.response_serializer import ResponseSerializer

router = APIRouter()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
        "row_factory": dict_row,
    }
    async with AsyncConnectionPool(
        settings.CHECKPOINT_URL, kwargs=connection_kwargs
    ) as pool:
        await pool.wait()
        checkpointer = AsyncPostgresSaver(pool)  # type: ignore
        settings.logger.info("Setting up the checkpoint db.")
        await checkpointer.setup()  # TOOD: run only the first time
        yield {"checkpointer": checkpointer}
        settings.logger.info("Closing the connection pool.")

@router.post("/message", response_model=ChatResponse)
async def chat(input: ChatInput, request: Request) -> dict[str, Any] | Any:
    config = RunnableConfig(configurable={"thread_id": input.thread_id})
    chat_instance = graph_builder.compile(checkpointer=request.state.checkpointer)
    async for event in chat_instance.astream(
        {"messages": [{"role": "user", "content": input.message}]},
        config=config,
        stream_mode="values",
    ):
        last_event = event
    return last_event  # Return only the last event

@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...), 
    thread_id: str = Form(...)
):
    """
    Upload a text file and send its content to the chat endpoint.
    Only .txt files are supported. Maximum file size: 5MB.
    Requires thread_id to specify which conversation to send the content to.
    """
    
    # Validate file
    FileValidator.validate_file_presence(file)
    FileValidator.validate_file_extension(file.filename)
    FileValidator.validate_content_type(file.content_type)
    
    if file.size:
        FileValidator.validate_file_size(file.size)
    
    try:
        # Process file
        text_content = await FileProcessor.read_and_validate_file(file)
        
        # Send to chat
        try:
            message_content = ChatService.create_upload_message(file.filename, text_content)
            last_event = await ChatService.send_to_chat(request, message_content, thread_id, graph_builder)
            
            chat_response = ResponseSerializer.serialize_chat_response(last_event)
            response_data = ResponseSerializer.create_success_response(
                file.filename, thread_id, len(text_content), chat_response
            )
            
            return JSONResponse(status_code=200, content=response_data)
            
        except Exception as e:
            settings.logger.error(f"Error sending file content to chat: {str(e)}")
            
            content_preview = text_content[:200] + "..." if len(text_content) > 200 else text_content
            response_data = ResponseSerializer.create_partial_success_response(
                file.filename, thread_id, len(text_content), content_preview
            )
            
            return JSONResponse(status_code=200, content=response_data)
    
    except Exception as e:
        settings.logger.error(f"Error processing uploaded file: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Error processing uploaded file"
        )