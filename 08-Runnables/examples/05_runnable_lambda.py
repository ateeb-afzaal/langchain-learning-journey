
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
)

# ==========================================
# PART 1: BASIC RUNNABLE LAMBDA
# ==========================================

print("========== BASIC RUNNABLE LAMBDA ==========")

double = RunnableLambda(lambda x: x * 2)

print("Input:", 5)
print("Output:", double.invoke(5))


# ==========================================
# PART 2: REGULAR PYTHON FUNCTION
# ==========================================

print("\n========== PYTHON FUNCTION ==========")

def clean_text(text):
    return text.strip().upper()

clean_runnable = RunnableLambda(clean_text)

text = "  hello langchain  "

print("Original:", repr(text))
print("Cleaned:", clean_runnable.invoke(text))


# ==========================================
# PART 3: RUNNABLE SEQUENCE
# ==========================================

print("\n========== RUNNABLE SEQUENCE ==========")

remove_spaces = RunnableLambda(
    lambda text: text.strip()
)

uppercase = RunnableLambda(
    lambda text: text.upper()
)

sequence = remove_spaces | uppercase

print("Output:", sequence.invoke("  hello python  "))


# ==========================================
# PART 4: RUNNABLE PARALLEL
# ==========================================

print("\n========== RUNNABLE PARALLEL ==========")

parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2),
    cube=RunnableLambda(lambda x: x ** 3),
)

result = parallel.invoke(5)

print("Input:", 5)
print("Result:", result)


# ==========================================
# PART 5: BATCH EXECUTION
# ==========================================

print("\n========== BATCH EXECUTION ==========")

numbers = [2, 3, 4, 5]

results = double.batch(numbers)

print("Inputs:", numbers)
print("Outputs:", results)


# ==========================================
# PART 6: RUNNABLE LAMBDA WITH GROQ
# ==========================================

print("\n========== RUNNABLE LAMBDA WITH GROQ ==========")

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Convert raw text into a cleaned prompt dictionary
def prepare_topic(topic):
    cleaned_topic = topic.strip().title()

    return {
        "topic": cleaned_topic
    }

prepare_input = RunnableLambda(prepare_topic)

prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in exactly 3 simple sentences."
)

# Add a heading to the model's generated explanation
def format_output(text):
    return "AI EXPLANATION:\n\n" + str(text).strip()

output_formatter = RunnableLambda(format_output)

# Create the complete workflow
ai_chain = (
    prepare_input
    | prompt
    | model
    | StrOutputParser()
    | output_formatter
)

try:
    result = ai_chain.invoke("  machine learning  ")

    print("\nFINAL RESULT:\n")
    print(result)

    print("\nRESULT TYPE:")
    print(type(result))

except Exception as error:
    print("Groq RunnableLambda example failed:", error)


print("\nRunnableLambda example completed!")
