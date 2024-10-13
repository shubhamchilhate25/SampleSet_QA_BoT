import openai
import numpy as np

def generate_answer(query, faiss_index, all_documents, openai_api_key):
    openai.api_key = openai_api_key
    
    from backend.faiss_index import search_faiss
    from langchain.embeddings import OpenAIEmbeddings
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    indices = search_faiss(query, faiss_index, embeddings, k=3)

    relevant_docs = [all_documents[i] for i in indices[0]]

    context = " ".join(relevant_docs)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Answer the following based on the context:\n\n{context}\n\nQuestion: {query}"}
        ],
        max_tokens=100
    )
    
    return response['choices'][0]['message']['content'].strip()
