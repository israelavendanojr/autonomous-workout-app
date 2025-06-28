from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")

template = """
You are a helpful assistant that can answer questions about immigration.

Here are some relevant resources about immigration: {resources}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


while True:
    print("\n\n")
    question = input("Ask your question (q to quit): ")
    if question.lower() == "q":
        break

    result = chain.invoke({
        "resources": [],
        "question": question
    })

    print(result)
