from fastapi import FastAPI
import uvicorn
from api.chat_logic import chat_router

app = FastAPI(
    title="Counselor Agent with OPENAI API",
    version="1.0",
    description="A simple API server for counselor agent interactions"
)

app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
