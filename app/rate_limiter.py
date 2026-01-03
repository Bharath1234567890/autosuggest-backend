import time
from .redis_client import redis_client

def rate_limit(key: str, limit=30, window=60):
    # Fail-open if Redis is unavailable
    if redis_client is None:
        return

    now = int(time.time())
    bucket = f"rl:{key}"

    current = redis_client.get(bucket)
    if current and int(current) >= limit:
        raise Exception("Rate limit exceeded")

    pipe = redis_client.pipeline()
    pipe.incr(bucket, 1)
    pipe.expire(bucket, window)
    pipe.execute()
