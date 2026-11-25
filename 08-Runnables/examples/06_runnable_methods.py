
import asyncio
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda


# ==========================================
# PART 1: BASIC RUNNABLE METHODS
# ==========================================

double = RunnableLambda(lambda x: x * 2)

print("========== INVOKE ==========")

result = double.invoke(5)
print("Input: 5")
print("Output:", result)


print("\n========== BATCH ==========")

numbers = [2, 3, 4, 5]
results = double.batch(numbers)

print("Inputs:", numbers)
print("Outputs:", results)


print("\n========== STREAM ==========")

for chunk in double.stream(10):
    print("Chunk:", chunk)


# ==========================================
# PART 2: ASYNC RUNNABLE METHODS
# ==========================================

async def basic_async_examples():

    print("\n========== AINVOKE ==========")

    result = await double.ainvoke(5)
    print("Input: 5")
    print("Output:", result)

    print("\n========== ABATCH ==========")

    results = await double.abatch([2, 3, 4, 5])
    print("Results:", results)

    print("\n========== ASTREAM ==========")

    async for chunk in double.astream(10):
        print("Async Chunk:", chunk)


asyncio.run(basic_async_examples())


# ==========================================
# PART 3: RUNNABLE METHODS WITH GROQ
# ==========================================

print("\n========== GROQ RUNNABLE METHODS ==========")

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in 2 short sentences."
)

chain = prompt | model | StrOutputParser()


# 1. GROQ INVOKE
print("\n========== GROQ INVOKE ==========")

try:
    result = chain.invoke({
        "topic": "Machine Learning"
    })

    print(str(result))

except Exception as error:
    print("Invoke failed:", error)


# 2. GROQ BATCH
print("\n========== GROQ BATCH ==========")

try:
    topics = [
        {"topic": "Python"},
        {"topic": "SQL"}
    ]

    results = chain.batch(
        topics,
        config={"max_concurrency": 2}
    )

    for topic, result in zip(topics, results):
        print(f"\nTopic: {topic['topic']}")
        print(str(result))

except Exception as error:
    print("Batch failed:", error)


# 3. GROQ STREAM
print("\n========== GROQ STREAM ==========")

try:
    for chunk in chain.stream({
        "topic": "Artificial Intelligence"
    }):
        print(str(chunk), end="", flush=True)

    print()

except Exception as error:
    print("\nStream failed:", error)


# ==========================================
# PART 4: ASYNC GROQ METHODS
# ==========================================

async def groq_async_examples():

    # 4. GROQ AINVOKE
    print("\n========== GROQ AINVOKE ==========")

    try:
        result = await chain.ainvoke({
            "topic": "Deep Learning"
        })

        print(str(result))

    except Exception as error:
        print("Ainvoke failed:", error)

    # 5. GROQ ABATCH
    print("\n========== GROQ ABATCH ==========")

    try:
        results = await chain.abatch(
            [
                {"topic": "Computer Vision"},
                {"topic": "Natural Language Processing"}
            ],
            config={"max_concurrency": 2}
        )

        for result in results:
            print("\n", str(result))

    except Exception as error:
        print("Abatch failed:", error)

    # 6. GROQ ASTREAM
    print("\n========== GROQ ASTREAM ==========")

    try:
        async for chunk in chain.astream({
            "topic": "Neural Networks"
        }):
            print(str(chunk), end="", flush=True)

        print()

    except Exception as error:
        print("\nAstream failed:", error)


asyncio.run(groq_async_examples())

print("\nAll six Runnable methods demonstrated!")
