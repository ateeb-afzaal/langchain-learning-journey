
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
)

# ==========================================
# PART 1: BASIC RUNNABLE PASSTHROUGH
# ==========================================

print("========== BASIC PASSTHROUGH ==========")

passthrough = RunnablePassthrough()

result = passthrough.invoke("Hello LangChain")

print("Input: Hello LangChain")
print("Output:", result)


# ==========================================
# PART 2: PASSTHROUGH WITH PARALLEL
# ==========================================

print("\n========== PASSTHROUGH + PARALLEL ==========")

parallel = RunnableParallel(
    original=RunnablePassthrough(),
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2),
)

result = parallel.invoke(5)

print("Input:", 5)
print("Output:", result)


# ==========================================
# PART 3: PASSTHROUGH ASSIGN
# ==========================================

print("\n========== PASSTHROUGH ASSIGN ==========")

assign_chain = RunnablePassthrough.assign(
    double=lambda data: data["number"] * 2,
    square=lambda data: data["number"] ** 2,
)

result = assign_chain.invoke({
    "number": 5
})

print("Input: {'number': 5}")
print("Output:", result)


# ==========================================
# PART 4: PASSTHROUGH WITH GROQ
# ==========================================

print("\n========== PASSTHROUGH WITH GROQ ==========")

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = PromptTemplate.from_template(
    "Answer the following question in 3 simple sentences: {question}"
)

answer_chain = prompt | model | StrOutputParser()

# Preserve the question and add an AI-generated answer
ai_chain = RunnablePassthrough.assign(
    answer=answer_chain
)

try:
    result = ai_chain.invoke({
        "question": "What is Machine Learning?"
    })

    print("\nORIGINAL QUESTION:")
    print(result["question"])

    print("\nAI ANSWER:")
    print(str(result["answer"]))

    print("\nRESULT TYPE:")
    print(type(result))

except Exception as error:
    print("Groq passthrough example failed:", error)


print("\nRunnablePassthrough example completed!")
