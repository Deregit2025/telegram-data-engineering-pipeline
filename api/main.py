from fastapi import FastAPI
from api.routers import reports, channels, search

app = FastAPI(
    title="Telegram Analytics API",
    description="Analytical API exposing insights from Telegram medical channels",
    version="1.0.0"
)

# Register routers
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(channels.router, prefix="/api/channels", tags=["Channels"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])


@app.get("/")
def root():
    return {"message": "Telegram Analytics API is running"}
