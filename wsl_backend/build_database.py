import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("1. Reading all PDFs from 'Documents_DataScience' folder...")
loader = PyPDFDirectoryLoader("Documents_DataScience")
documents = loader.load()
print(f"Found {len(documents)} total pages of content.")

print("2. Chopping pages into small, readable chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} text chunks.")

print("3. Generating Neural Embeddings and building Vector Database...")
# This uses a fast, local embedding model that runs perfectly on your RTX 5090
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs={'device': 'cuda'})

# Save the database locally so the API can read it instantly
db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

print("\n[SUCCESS] Vector Database built and saved to './chroma_db'!")
print("Your AI Teacher now has a photographic memory of your syllabus.")
