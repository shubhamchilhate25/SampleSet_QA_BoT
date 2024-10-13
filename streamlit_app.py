import os
import streamlit as st
from backend.doc_loader import load_documents
from backend.faiss_index import initialize_faiss, search_faiss
from backend.openai_queries import generate_answer
import tempfile

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Fetch API keys from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.title("Interactive QA Bot with Document Upload")
st.sidebar.title("Upload Your Documents")

uploaded_files = st.sidebar.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
process_docs_clicked = st.sidebar.button("Process Documents")

# FAISS Index setup
faiss_index, all_documents = None, []

if process_docs_clicked:
    if uploaded_files and len(uploaded_files) <= 5:
        docs = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            data = load_documents(tmp_file_path)
            docs.extend(data)
            os.remove(tmp_file_path)

        faiss_index, all_documents = initialize_faiss(docs)
        st.success("Documents processed and embeddings generated!")
    else:
        st.error("Please upload up to 5 PDF documents.")

# Query Input
query = st.text_input("Ask a question:")
if query and faiss_index:
    answer = generate_answer(query, faiss_index, all_documents, openai_api_key)
    st.write("Answer:", answer)
