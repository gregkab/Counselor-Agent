from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

app=FastAPI(
    title="LangChain Demo with OPENAI API",
    version="1.0",
    description="A simple API server"
)
add_routes(app, ChatOpenAI(), path="/openai")

model=ChatOpenAI()
prompt=ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")

add_routes(app, prompt|model, path="/essay")

if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=8000)
