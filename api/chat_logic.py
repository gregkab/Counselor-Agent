from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ["LANGCHAIN_API_KEY"]

router = APIRouter()

# OpenAI model for Counselor Agent
def counselorAgent(topic):
    loader = DirectoryLoader('./knowledgebase', glob="**/*.txt")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(topic)

# Route for counseling session initiation or interaction
@router.post("/counsel")
async def counsel(topic: str):
    try:
        # Integrate AI logic here. For now simple example.
        response = counselorAgent(topic)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
