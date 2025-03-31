import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
from llama_index.llms import Gemini
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
import chromadb
from config import api_key1

# Step 1: Load Data
def load_data(directory_path):
    documents = SimpleDirectoryReader(directory_path).load_data()
    return documents

# Step 2: Initialize ChromaDB
def initialize_chroma_db(collection_name):
    db = chromadb.PersistentClient(path="./embeddings/chroma_db")
    chroma_collection = db.get_or_create_collection(collection_name)
    return chroma_collection

# Step 3: Create Vector Store Index
def create_vector_store_index(documents, chroma_collection):
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(llm=Gemini())
    index = VectorStoreIndex.from_documents(documents, service_context=service_context, storage_context=storage_context)
    return index

# Step 4: Initialize Gemini Client
def initialize_gemini_client(api_key1):
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"), api_key=api_key1)
    return client

# Step 5: Create Chat Session
def create_chat_session(client, model_name):
    chat_session = client.chats.create(model=model_name)
    return chat_session

# Step 6: Chat with the Bot
def chat_with_bot(chat_session, index, query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response

if __name__ == "__main__":
    # Configuration
    directory_path = "path/to/your/documents"
    collection_name = "quickstart"
    api_key = "your_gemini_api_key"
    model_name = "gemini-1.5-flash-001"

    # Load data
    documents = load_data(directory_path)

    # Initialize ChromaDB
    chroma_collection = initialize_chroma_db(collection_name)

    # Create vector store index
    index = create_vector_store_index(documents, chroma_collection)

    # Initialize Gemini client
    client = initialize_gemini_client(api_key)

    # Create chat session
    chat_session = create_chat_session(client, model_name)

    # Chat with the bot
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = chat_with_bot(chat_session, index, query)
        print(f"Bot: {response}")