import httpx

async def fetch_suggestions(query: str):
    async with httpx.AsyncClient(timeout=2) as client:
        try:
            res = await client.get(
                "https://suggestqueries.google.com/complete/search",
                params={
                    "client": "firefox",
                    "q": query,
                },
            )
            res.raise_for_status()
            data = res.json()
            return data[1] if len(data) > 1 else []
        except Exception:
            return []
