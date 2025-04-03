from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from agentchat.api.endpoints import lifespan, router

app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    """Redirects the base endpoint to the API documentation."""
    return RedirectResponse(url="/docs")
