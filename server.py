import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from time_server import mcp as time_mcp
from wetterwarnungen import mcp as ww_mcp

# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(time_mcp.session_manager.run())
        await stack.enter_async_context(ww_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/time", time_mcp.streamable_http_app())
app.mount("/ww", ww_mcp.streamable_http_app())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

PORT = os.environ.get("PORT", 10000)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)