
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel

# ==========================================
# PART 1: RUNNABLE PARALLEL WITHOUT LLM
# ==========================================

print("========== BASIC RUNNABLE PARALLEL ==========")

parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2),
    cube=RunnableLambda(lambda x: x ** 3)
)

result = parallel.invoke(5)

print("Input:", 5)
print("Result:", result)
print("Result Type:", type(result))

print("\nIndividual Results:")
print("Double:", result["double"])
print("Square:", result["square"])
print("Cube:", result["cube"])


# ==========================================
# PART 2: RUNNABLE SEQUENCE VS PARALLEL
# ==========================================

print("\n========== SEQUENCE VS PARALLEL ==========")

double = RunnableLambda(lambda x: x * 2)
square = RunnableLambda(lambda x: x ** 2)

sequential = double | square

parallel_comparison = RunnableParallel(
    double=double,
    square=square
)

print("Input:", 5)
print("Sequential Result:", sequential.invoke(5))
print("Parallel Result:", parallel_comparison.invoke(5))


# ==========================================
# PART 3: BATCH EXECUTION
# ==========================================

print("\n========== BATCH EXECUTION ==========")

numbers = [2, 3, 4]

results = parallel.batch(
    numbers,
    config={"max_concurrency": 2}
)

for number, output in zip(numbers, results):
    print(f"Input: {number} -> {output}")


# ==========================================
# PART 4: RUNNABLE PARALLEL WITH GROQ
# ==========================================

print("\n========== GROQ RUNNABLE PARALLEL ==========")

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
    "Return only the questions."
)

summary_chain = (
    summary_prompt
    | model
    | StrOutputParser()
)

questions_chain = (
    questions_prompt
    | model
    | StrOutputParser()
)

ai_parallel = RunnableParallel(
    summary=summary_chain,
    questions=questions_chain
)

try:
    ai_result = ai_parallel.invoke({
        "topic": "Python decorators"
    })

    print("\nSUMMARY:\n")
    print(str(ai_result["summary"]))

    print("\nINTERVIEW QUESTIONS:\n")
    print(str(ai_result["questions"]))

    print("\nAI Result Type:", type(ai_result))

except Exception as error:
    print("Groq parallel execution failed:", error)

print("\nRunnableParallel example completed!")

