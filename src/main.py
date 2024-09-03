import uvicorn
from fastapi import FastAPI

from api.v1.router import api_router as chat_router

app = FastAPI(
    title="Chat",
    openapi_url="/chat/openapi.json",
    docs_url="/chat/docs",
)


app.include_router(chat_router, prefix="/chat")
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        proxy_headers=True,
    )
