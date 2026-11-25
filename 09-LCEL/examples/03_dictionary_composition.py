
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)


# ==========================================
# PART 1: BASIC DICTIONARY COMPOSITION
# ==========================================

print("========== BASIC DICTIONARY COMPOSITION ==========")

identity = RunnableLambda(lambda x: x)
double = RunnableLambda(lambda x: x * 2)
square = RunnableLambda(lambda x: x ** 2)

chain = identity | {
    "double": double,
    "square": square
}

result = chain.invoke(5)

print("Input:", 5)
print("Result:", result)
print("Result Type:", type(result))
print("Chain Type:", type(chain))


# ==========================================
# PART 2: DICTIONARY AFTER TRANSFORMATION
# ==========================================

print("\n========== DICTIONARY AFTER TRANSFORMATION ==========")

add_one = RunnableLambda(lambda x: x + 1)

transformed_chain = add_one | {
    "double": double,
    "square": square
}

result = transformed_chain.invoke(5)

print("Input:", 5)
print("Result:", result)


# ==========================================
# PART 3: DIFFERENT OUTPUT TYPES
# ==========================================

print("\n========== DIFFERENT OUTPUT TYPES ==========")

text_chain = identity | {
    "original": RunnablePassthrough(),
    "length": RunnableLambda(lambda text: len(text)),
    "uppercase": RunnableLambda(lambda text: text.upper())
}

result = text_chain.invoke("python")

print("Result:", result)
print("Length Type:", type(result["length"]))


# ==========================================
# PART 4: RUNNABLEPASSTHROUGH.ASSIGN()
# ==========================================

print("\n========== PASSTHROUGH ASSIGN ==========")

assign_chain = RunnablePassthrough.assign(
    double=lambda data: data["number"] * 2,
    square=lambda data: data["number"] ** 2
)

result = assign_chain.invoke({"number": 5})

print("Result:", result)


# ==========================================
# PART 5: NESTED PARALLEL
# ==========================================

print("\n========== NESTED PARALLEL ==========")

nested_chain = RunnableParallel(
    original=RunnablePassthrough(),
    calculations=RunnableParallel(
        double=double,
        square=square
    )
)

result = nested_chain.invoke(5)

print("Result:", result)


# ==========================================
# PART 6: DICTIONARY COMPOSITION WITH GROQ
# ==========================================

print("\n========== DICTIONARY COMPOSITION WITH GROQ ==========")

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

summary_prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in exactly 3 simple sentences."
)

questions_prompt = PromptTemplate.from_template(
    "Generate exactly 3 interview questions about {topic}. "
    "Return only a numbered list of questions."
)

summary_chain = summary_prompt | model | StrOutputParser()
questions_chain = questions_prompt | model | StrOutputParser()

# Preserve the input dictionary and add two model-generated fields
ai_chain = RunnablePassthrough.assign(
    summary=summary_chain,
    questions=questions_chain
)

try:
    result = ai_chain.invoke({
        "topic": "Python Decorators"
    })

    print("\nTOPIC:")
    print(result["topic"])

    print("\nSUMMARY:")
    print(str(result["summary"]))

    print("\nINTERVIEW QUESTIONS:")
    print(str(result["questions"]))

    print("\nRESULT TYPE:")
    print(type(result))

    print("\nOUTPUT KEYS:")
    print(list(result.keys()))

except Exception as error:
    print("Groq dictionary composition failed:", error)


print("\nDictionary Composition example completed!")
