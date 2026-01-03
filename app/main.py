import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .rate_limiter import rate_limit
from .suggest import get_suggestions

app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-frontend-domain.vercel.app",  # add later
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- HEALTH ----------
@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"health": "ok"}

# ---------- API ----------
@app.get("/api/suggest")
async def suggest(q: str, request: Request):
    if len(q) < 2:
        return []

    rate_limit(request.client.host)
    return await get_suggestions(q)

# ---------- ENTRYPOINT ----------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
