
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSequence

# ==========================================
# PART 1: RUNNABLE SEQUENCE WITHOUT LLM
# ==========================================

print("========== BASIC RUNNABLE SEQUENCE ==========")

double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)
square = RunnableLambda(lambda x: x ** 2)

# Method 1: Explicit RunnableSequence
sequence_explicit = RunnableSequence(
    double,
    add_five,
    square
)

# Method 2: LCEL pipe operator
sequence_pipe = double | add_five | square

number = 3

print("Input:", number)
print("Explicit sequence result:", sequence_explicit.invoke(number))
print("Pipe sequence result:", sequence_pipe.invoke(number))

# Check the Runnable type
print("Sequence type:", type(sequence_pipe))


# ==========================================
# PART 2: BATCH EXECUTION
# ==========================================

print("\n========== BATCH ==========")

numbers = [1, 2, 3, 4]

results = sequence_pipe.batch(numbers)

for number, result in zip(numbers, results):
    print(f"Input: {number} -> Output: {result}")


# ==========================================
# PART 3: RUNNABLE SEQUENCE WITH GROQ
# ==========================================

print("\n========== GROQ RUNNABLE SEQUENCE ==========")

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in exactly 3 simple sentences."
)

parser = StrOutputParser()

# Create a sequence using LCEL
ai_sequence = prompt | model | parser

try:
    result = ai_sequence.invoke({
        "topic": "Machine Learning"
    })

    print("\nAI Explanation:\n")
    print(str(result))

    print("\nAI Sequence Type:")
    print(type(ai_sequence))

except Exception as error:
    print("Groq sequence failed:", error)


print("\nRunnableSequence example completed!")
