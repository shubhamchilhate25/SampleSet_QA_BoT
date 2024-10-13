from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)
    
    return split_docs
