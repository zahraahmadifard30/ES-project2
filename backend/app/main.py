from fastapi import FastAPI

app = FastAPI(title="Digital Library API", version="0.1.0")


@app.get("/health/live")
async def health_live() -> dict[str, str]:
    return {"status": "ok"}
