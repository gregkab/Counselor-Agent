import os
from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Environment variables for Astra DB credentials
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE") or None

# Initialize embeddings and AstraDBVectorStore
embe = OpenAIEmbeddings()
vstore = AstraDBVectorStore(
    embedding=embe,
    collection_name="counselor_agent_knowledge",
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    namespace=ASTRA_DB_KEYSPACE,
)

def load_and_store_documents(directory_path):
    loader = DirectoryLoader(directory_path, glob="**/*.txt")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Load documents
    docs = loader.load()
    splits = text_splitter.split_documents(docs)

    prepared_docs = []
    for split in splits:
        prepared_docs.append(Document(page_content=split.page_content, metadata=split.metadata))

    # Add documents in batches to AstraDB
    try:
        inserted_ids = vstore.add_documents(prepared_docs)
        print(f"Successfully stored {len(inserted_ids)} documents in Astra DB.")
    except Exception as e:
        print(f"Error storing documents: {e}")

if __name__ == "__main__":
    knowledgebase_path = './knowledgebase'
    load_and_store_documents(knowledgebase_path)