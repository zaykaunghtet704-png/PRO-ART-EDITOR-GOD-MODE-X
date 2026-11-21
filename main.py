"""HTTP API and health endpoints for Render Web Service."""
from fastapi import FastAPI
from config import APP_NAME, APP_ENV

app = FastAPI(
    title=APP_NAME,
    version="0.1.0",
    description="Creative editing platform API.",
)


@app.get("/")
async def home():
    return {
        "ok": True,
        "service": APP_NAME,
        "environment": APP_ENV,
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    return {"ok": True, "service": "api"}
