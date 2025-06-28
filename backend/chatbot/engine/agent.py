from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are a helpful legal assistant answering questions about immigration.
Do not fabricate PDF titles or page numbers. If metadata is missing, say 'source unknown.'

Respond clearly, citing the PDF source and page when applicable.

Use direct quotes or summaries from the documents. Always cite the source filename if available.

### Resources:
{resources}

### Question:
{question}

### Answer:


"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# flatten docs into readable format for citation
def format_docs(docs):
    return "\n\n".join(
        f"{i+1}. {doc.page_content.strip()}\n(Source: {doc.metadata.get('source', 'unknown')}, Page: {doc.metadata.get('page_number', '?')})"
        for i, doc in enumerate(docs)
    )


while True:
    print("\n\n")
    question = input("Ask your question (q to quit): ")
    if question.lower() == "q":
        break
    
    rag_docs = retriever.invoke(question)
    print(f"Retrieved {len(rag_docs)} docs")
    print("🔎 Sources passed to model:")
    for doc in rag_docs:
        print(f"- Source: {doc.metadata.get('source', 'unknown')} | Page: {doc.metadata.get('page_number', '?')}")

    result = chain.invoke({
        "resources": format_docs(rag_docs),
        "question": question
    })

    print(result)

