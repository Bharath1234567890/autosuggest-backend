from fastapi import FastAPI, Request
from .rate_limiter import rate_limit
from .suggest import get_suggestions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/suggest")
async def suggest(q: str, request: Request):
    if len(q) < 2:
        return []

    rate_limit(request.client.host)

    return await get_suggestions(q)
