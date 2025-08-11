import chromadb
from chromadb.utils import embedding_functions
import openai
import pandas as pd
import os

# Initialize Chroma client and collection
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("documents")

# OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY")
)

def extract_text_from_file(uploaded_file):
    """
    Extracts text from a text, CSV, or Excel file.
    Returns a string.
    """
    if uploaded_file.name.endswith('.txt'):
        return uploaded_file.read().decode('utf-8')
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        return df.to_csv(index=False)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
        return df.to_csv(index=False)
    else:
        return None

def add_document_to_chroma(doc_id, content, metadata=None):
    """
    Adds a document to the Chroma collection with OpenAI embedding.
    """
    collection.add(
        documents=[content],
        ids=[doc_id],
        metadatas=[metadata or {}],
        embedding_function=openai_ef
    )

def query_chroma(query, n_results=3):
    """
    Queries Chroma for the most relevant documents to the query string.
    Returns a list of (content, metadata, score).
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        embedding_function=openai_ef
    )
    docs = results['documents'][0]
    metas = results['metadatas'][0]
    scores = results['distances'][0]
    return list(zip(docs, metas, scores))
