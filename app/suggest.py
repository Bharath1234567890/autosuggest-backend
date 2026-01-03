from .redis_client import redis_client
from .serpapi_client import fetch_suggestions

CACHE_TTL = 120

def normalize(q: str):
    return q.strip().lower()

async def get_suggestions(q: str):
    key = f"suggest:{normalize(q)}"

    cached = redis_client.get(key)
    if cached:
        return eval(cached)

    suggestions = await fetch_suggestions(q)

    suggestions = suggestions[:8]
    redis_client.setex(key, 120, str(suggestions))

    return suggestions
