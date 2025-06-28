from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

# 1. Load and process PDFs
base_dir = os.path.dirname(os.path.dirname(__file__))  # goes up to `engine/`
pdf_dir = os.path.join(base_dir, "engine/immigration_resources")
db_location = os.path.join(base_dir, "chroma_store")

all_pdfs = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
docs = []
for pdf_path in all_pdfs:
    loader = PyPDFLoader(pdf_path)
    loaded_docs = loader.load()
    for i, doc in enumerate(loaded_docs):
        doc.metadata["source"] = os.path.basename(pdf_path)
        doc.metadata["page_number"] = doc.metadata.get("page", i + 1)
    docs.extend(loaded_docs)

# 2. Chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 4. Load or create vector store
if not os.path.exists(db_location) or len(os.listdir(db_location)) == 0:
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="immigration_rag",
        persist_directory=db_location
    )
    vectorstore.persist()
    print("✅ Vector store created and persisted.")
else:
    vectorstore = Chroma(
        collection_name="immigration_rag",
        persist_directory=db_location,
        embedding_function=embeddings
    )
    print("✅ Existing vector store loaded.")

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
