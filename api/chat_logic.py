from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os

# Environment variables for API keys and Astra DB credentials
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

# Initialize the API router and AstraDBVectorStore
router = APIRouter()
embe = OpenAIEmbeddings()
vstore = AstraDBVectorStore(
    embedding=embe,
    collection_name="counselor_agent_knowledge",
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    namespace=ASTRA_DB_KEYSPACE,
)

class TopicModel(BaseModel):
    topic: str

@router.post("/counsel")
async def counsel(body: TopicModel):
    try:
        # Initialize the ChatOpenAI model with your chosen GPT model
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=os.getenv("OPENAI_API_KEY"))

        # Set up the retriever with AstraDBVectorStore
        retriever = vstore.as_retriever(search_kwargs={"k": 3})

        # Define the prompt template for university counseling context
        counseling_template = """
        You are a university counselor with in-depth knowledge of academic resources, programs, and advice. Use the provided context to offer guidance and support for students' queries. Your responses should be informative, supportive, and directly address the students' concerns.

        CONTEXT:
        {context}

        QUESTION: {question}

        YOUR ANSWER:
        """
        counseling_prompt = ChatPromptTemplate.from_template(counseling_template)

        # Form the RAG chain
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | counseling_prompt
            | llm
            | StrOutputParser()
        )

        # Invoke the chain with the user's question
        response = chain.invoke(body.topic)

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
