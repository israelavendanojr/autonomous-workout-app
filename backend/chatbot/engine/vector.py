from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

# 1. Load PDFs
base_dir = os.path.dirname(os.path.dirname(__file__))  # goes up to `engine/`
pdf_dir = os.path.join(base_dir, "engine/immigration_resources")
all_pdfs = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

docs = []
for pdf_path in all_pdfs:
    loader = PyPDFLoader(pdf_path)
    docs.extend(loader.load())

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. Set up vector store config and embeddings
db_location = os.path.join(base_dir, "chroma_store")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma(
    collection_name="immigration_rag",
    persist_directory=db_location,
    embedding_function=embeddings
)

# 4. Add documents to vector store if not already added
if not os.path.exists(db_location):
    documents = []
    ids = []

    for i, chunk in enumerate(chunks):
        # Add source filename and page number if available
        chunk.metadata["source"] = chunk.metadata.get("source", "unknown").split("/")[-1]
        chunk.metadata["page_number"] = chunk.metadata.get("page", "unknown")

        documents.append(chunk)
        ids.append(f"doc_{i}")

    vectorstore.add_documents(documents=documents, ids=ids)
    vectorstore.persist()

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

print("PDFs added and stored in Chroma vector DB.")