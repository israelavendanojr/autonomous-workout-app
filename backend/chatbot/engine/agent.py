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

result = chain.invoke({
    "resources": "https://www.aclu.org/know-your-rights/immigrants-rights#i-want-to-share-this-information-on-social-media",
    "question": "What to do if I am detained near the border by Border Patrol?"
})

print(result)
