from app.llm import llm


response = llm.invoke(
    "What is artificial intelligence? Explain in two sentences."
)

print(response.content)