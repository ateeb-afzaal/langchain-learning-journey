
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda


# ==========================================
# PART 1: BASIC PIPE OPERATOR
# ==========================================

print("========== BASIC PIPE OPERATOR ==========")

double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)

chain = double | add_five

print("Input:", 10)
print("Result:", chain.invoke(10))


# ==========================================
# PART 2: ORDER OF OPERATIONS
# ==========================================

print("\n========== ORDER OF OPERATIONS ==========")

chain_a = double | add_five
chain_b = add_five | double

print("Double then Add Five:", chain_a.invoke(10))
print("Add Five then Double:", chain_b.invoke(10))


# ==========================================
# PART 3: THREE-STEP CHAIN
# ==========================================

print("\n========== THREE-STEP CHAIN ==========")

square = RunnableLambda(lambda x: x ** 2)

three_step_chain = double | add_five | square

print("Input:", 3)
print("Result:", three_step_chain.invoke(3))


# ==========================================
# PART 4: TEXT PROCESSING
# ==========================================

print("\n========== TEXT PROCESSING ==========")

clean_text = RunnableLambda(lambda text: text.strip())
uppercase = RunnableLambda(lambda text: text.upper())

add_prefix = RunnableLambda(
    lambda text: "Processed: " + text
)

text_chain = clean_text | uppercase | add_prefix

result = text_chain.invoke("  hello langchain  ")

print("Result:", result)


# ==========================================
# PART 5: DATA TYPE COMPATIBILITY
# ==========================================

print("\n========== DATA TYPE COMPATIBILITY ==========")

convert_to_string = RunnableLambda(lambda x: str(x))

compatible_chain = double | convert_to_string | uppercase

result = compatible_chain.invoke(5)

print("Result:", result)
print("Result Type:", type(result))


# ==========================================
# PART 6: BATCH EXECUTION
# ==========================================

print("\n========== BATCH EXECUTION ==========")

numbers = [1, 2, 3, 4]

results = three_step_chain.batch(numbers)

for number, result in zip(numbers, results):
    print(f"Input: {number} -> Output: {result}")


# ==========================================
# PART 7: PIPE OPERATOR WITH GROQ
# ==========================================

print("\n========== PIPE OPERATOR WITH GROQ ==========")

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Prepare raw user input for the prompt
def prepare_topic(topic):
    cleaned_topic = topic.strip().title()

    if not cleaned_topic:
        raise ValueError("Topic cannot be empty")

    return {"topic": cleaned_topic}


prepare_input = RunnableLambda(prepare_topic)

prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in exactly 3 simple sentences."
)

parser = StrOutputParser()


# Format the generated response
def format_answer(text):
    return "AI EXPLANATION:\n\n" + str(text).strip()


output_formatter = RunnableLambda(format_answer)


# Complete LCEL workflow
ai_chain = (
    prepare_input
    | prompt
    | model
    | parser
    | output_formatter
)


try:
    result = ai_chain.invoke("  machine learning  ")

    print("\nFINAL OUTPUT:\n")
    print(result)

    print("\nRESULT TYPE:")
    print(type(result))

    print("\nCHAIN TYPE:")
    print(type(ai_chain))

    print("\nNUMBER OF STEPS:")
    print(len(ai_chain.steps))

    print("\nCHAIN COMPONENTS:")
    for index, step in enumerate(ai_chain.steps, start=1):
        print(f"Step {index}: {type(step).__name__}")

except Exception as error:
    print("Groq LCEL execution failed:", error)


print("\nPipe Operator example completed!")
