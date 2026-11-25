
import asyncio

from langchain_core.runnables import (
    RunnableLambda,
    RunnableSequence,
    RunnableParallel,
    RunnablePassthrough,
)

# 1. Basic RunnableLambda
print("========== RUNNABLE LAMBDA ==========")

double = RunnableLambda(lambda x: x * 2)

print("Input: 5")
print("Output:", double.invoke(5))


# 2. RunnableSequence
print("\n========== RUNNABLE SEQUENCE ==========")

add_five = RunnableLambda(lambda x: x + 5)

sequence = RunnableSequence(double, add_five)

print("Input: 10")
print("Output:", sequence.invoke(10))


# 3. RunnableParallel
print("\n========== RUNNABLE PARALLEL ==========")

parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2),
)

print("Input: 5")
print("Output:", parallel.invoke(5))


# 4. RunnablePassthrough
print("\n========== RUNNABLE PASSTHROUGH ==========")

passthrough = RunnablePassthrough()

print("Input: Hello LangChain")
print("Output:", passthrough.invoke("Hello LangChain"))


# 5. Batch
print("\n========== BATCH ==========")

print("Inputs:", [2, 3, 4, 5])
print("Outputs:", double.batch([2, 3, 4, 5]))


# 6. Async
print("\n========== ASYNC ==========")

async def main():
    result = await double.ainvoke(10)
    print("Async input: 10")
    print("Async output:", result)

asyncio.run(main())

print("\nAll Runnable basics tests completed!")
