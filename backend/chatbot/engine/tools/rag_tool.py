from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

def get_pdf_paths(pdf_dir: str) -> list[str]:
    return [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

def load_and_tag_documents(pdf_paths: list[str]) -> list:
    docs = []
    for pdf_path in pdf_paths:
        loader = PyPDFLoader(pdf_path)
        loaded_docs = loader.load()
        for i, doc in enumerate(loaded_docs):
            doc.metadata["source"] = os.path.basename(pdf_path)
            doc.metadata["page_number"] = doc.metadata.get("page", i + 1)
        docs.extend(loaded_docs)
    return docs

def chunk_documents(docs: list, chunk_size: int = 500, chunk_overlap: int = 50) -> list:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)

def create_or_load_vectorstore(chunks: list, db_location: str, collection_name: str, embeddings) -> Chroma:
    if not os.path.exists(db_location) or len(os.listdir(db_location)) == 0:
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=collection_name,
            persist_directory=db_location
        )
        vectorstore.persist()
        print("Vector store created and persisted.")
    else:
        vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=db_location,
            embedding_function=embeddings
        )
        print("Existing vector store loaded.")
    return vectorstore

# === Main Logic ===
def setup_rag_pipeline():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Goes up to `engine/`
    pdf_dir = os.path.join(base_dir, "immigration_resources")
    db_location = os.path.join(base_dir, "chroma_store")

    pdf_paths = get_pdf_paths(pdf_dir)
    docs = load_and_tag_documents(pdf_paths)
    chunks = chunk_documents(docs)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = create_or_load_vectorstore(chunks, db_location, "immigration_rag", embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 5})

# This is what other files can import
retriever = setup_rag_pipeline()
