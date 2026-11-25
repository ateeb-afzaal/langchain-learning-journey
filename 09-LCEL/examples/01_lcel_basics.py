
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

# ==========================================
# PART 1: LCEL WITHOUT AN LLM
# ==========================================

print("========== LCEL BASICS ==========")

double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)

chain = double | add_five

print("Input:", 10)
print("Output:", chain.invoke(10))
print("Chain Type:", type(chain))


# ==========================================
# PART 2: TEXT PROCESSING WITH LCEL
# ==========================================

print("\n========== TEXT PROCESSING ==========")

clean = RunnableLambda(lambda text: text.strip())
uppercase = RunnableLambda(lambda text: text.upper())
add_prefix = RunnableLambda(
    lambda text: "Processed: " + text
)

text_chain = clean | uppercase | add_prefix

result = text_chain.invoke("  hello langchain  ")

print("Result:", result)


# ==========================================
# PART 3: BATCH EXECUTION
# ==========================================

print("\n========== BATCH ==========")

numbers = [1, 2, 3, 4]

results = chain.batch(numbers)

print("Inputs:", numbers)
print("Outputs:", results)


# ==========================================
# PART 4: INSPECTING THE CHAIN
# ==========================================

print("\n========== CHAIN INSPECTION ==========")

print("Chain Type:", type(chain))
print("Number of Steps:", len(chain.steps))

for index, step in enumerate(chain.steps, start=1):
    print(f"Step {index}: {type(step).__name__}")

try:
    graph = chain.get_graph()
    print("\nChain Graph:")
    print(graph.draw_ascii())
except ImportError:
    print("ASCII graph requires an optional dependency.")
    print("Try: python -m pip install grandalf")
except Exception as error:
    print("Graph visualization unavailable:", error)


# ==========================================
# PART 5: LCEL WITH GROQ
# ==========================================

print("\n========== LCEL WITH GROQ ==========")

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in 3 simple sentences."
)

ai_chain = prompt | model | StrOutputParser()

try:
    result = ai_chain.invoke({
        "topic": "Machine Learning"
    })

    print("\nAI Explanation:")
    print(str(result))

    print("\nAI Chain Type:")
    print(type(ai_chain))

except Exception as error:
    print("Groq LCEL execution failed:", error)


print("\nLCEL Basics example completed!")
