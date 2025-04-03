from fastapi import APIRouter, FastAPI, Request
from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from typing import Any, AsyncGenerator
from langgraph.utils.runnable import RunnableConfig

from agentchat.api.schema import ChatInput, ChatResponse
from agentchat.core import settings
from agentchat.agents.chatbot import graph_builder

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
