#chat_logic.py
from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os

# Environment variables for API keys and Astra DB credentials
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ["LANGCHAIN_API_KEY"]
# Data Model
class TopicModel(BaseModel):
    topic: str

# Initialize API Router
router = APIRouter()

# Initialize OpenAI Embeddings and AstraDBVectorStore
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

# Statefully manage chat history ###
store = {}

# API Endpoints
@router.post("/counsel")
async def counsel(body: TopicModel):
    try:
        # Initialize the ChatOpenAI model with your chosen GPT model
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=os.getenv("OPENAI_API_KEY"))

        # Set up the retriever with AstraDBVectorStore
        retriever = vstore.as_retriever(search_kwargs={"k": 3})

        ### Contextualize question ###
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )
        
        ### Answer question ###
        counselor_system_prompt = """
        You are a university counselor dedicated to assisting students with academic challenges.
        Utilize the information provided below to guide or advise the student.
        If the solution is unclear, admit your limitations.
        Limit your advice to three sentences to maintain clarity and brevity.

        {context}"""
        counselor_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", counselor_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        counselor_chain = create_stuff_documents_chain(llm, counselor_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, counselor_chain)

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in store:
                store[session_id] = ChatMessageHistory()
            return store[session_id]


        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        response = conversational_rag_chain.invoke(
            {"input": body.topic},
            config={
                "configurable": {"session_id": "abc123"}
            },  # constructs a key "abc123" in `store`.
        )["answer"]

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
