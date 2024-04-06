from fastapi import APIRouter, HTTPException
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

router = APIRouter()

# OpenAI model for Counselor Agent
loader = DirectoryLoader('../knowledgebase', glob="**/*.md")
docs = loader.load()
model = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("Assist with counseling on {topic}")

# Route for counseling session initiation or interaction
@router.post("/counsel")
async def counsel(topic: str):
    try:
        # Integrate AI logic here. For now simple example.
        response = prompt|model
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
