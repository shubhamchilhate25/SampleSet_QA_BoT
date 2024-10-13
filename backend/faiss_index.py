import faiss
import numpy as np
from langchain.embeddings import OpenAIEmbeddings

def initialize_faiss(docs, openai_api_key):
    doc_texts = [doc.page_content for doc in docs]
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    doc_embeddings = embeddings.embed_documents(doc_texts)
    
    dim = 1536  # Adjust to OpenAI embedding dimensions
    faiss_index = faiss.IndexFlatL2(dim)
    
    doc_embeddings_np = np.array(doc_embeddings).astype('float32')
    if len(doc_embeddings_np.shape) == 1:
        doc_embeddings_np = np.expand_dims(doc_embeddings_np, axis=0)

    faiss_index.add(doc_embeddings_np)
    
    return faiss_index, doc_texts

def search_faiss(query, faiss_index, embeddings, k=5):
    query_embedding = embeddings.embed_documents([query])[0]
    query_vector = np.array(query_embedding).astype('float32').reshape(1, -1)
    
    distances, indices = faiss_index.search(query_vector, k)
    return indices
