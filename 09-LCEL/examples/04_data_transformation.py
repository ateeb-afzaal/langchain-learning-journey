
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
)


# ==========================================
# PART 1: BASIC TEXT TRANSFORMATION
# ==========================================

print("========== BASIC TRANSFORMATION ==========")

clean = RunnableLambda(lambda text: text.strip())
uppercase = RunnableLambda(lambda text: text.upper())
add_prefix = RunnableLambda(
    lambda text: "Processed: " + text
)

text_chain = clean | uppercase | add_prefix

result = text_chain.invoke("  hello langchain  ")

print("Result:", result)


# ==========================================
# PART 2: INPUT VALIDATION
# ==========================================

print("\n========== INPUT VALIDATION ==========")

def validate_topic(text):
    if not isinstance(text, str):
        raise TypeError("Topic must be a string")

    cleaned = text.strip()

    if not cleaned:
        raise ValueError("Topic cannot be empty")

    return cleaned


validator = RunnableLambda(validate_topic)

print("Valid input:", validator.invoke("  Python  "))

try:
    validator.invoke("   ")
except ValueError as error:
    print("Invalid input:", error)


# ==========================================
# PART 3: DICTIONARY TRANSFORMATION
# ==========================================

print("\n========== DICTIONARY TRANSFORMATION ==========")

def normalize_input(data):
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary")

    topic = data.get("topic")
    level = data.get("level", "beginner")

    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("Topic must be a non-empty string")

    if not isinstance(level, str):
        raise TypeError("Level must be a string")

    level = level.strip().lower()

    if level not in {"beginner", "intermediate", "advanced"}:
        raise ValueError("Invalid learning level")

    return {
        "topic": topic.strip().title(),
        "level": level,
    }


normalize = RunnableLambda(normalize_input)

raw_input = {
    "topic": "  machine learning  ",
    "level": "BEGINNER",
}

normalized_result = normalize.invoke(raw_input)

print("Raw Input:", raw_input)
print("Normalized:", normalized_result)


# ==========================================
# PART 4: PASSTHROUGH ASSIGN
# ==========================================

print("\n========== PASSTHROUGH ASSIGN ==========")

add_label = RunnablePassthrough.assign(
    display_label=lambda data: (
        f"{data['topic']} ({data['level']})"
    )
)

transformation_chain = normalize | add_label

result = transformation_chain.invoke(raw_input)

print("Result:", result)


# ==========================================
# PART 5: MULTI-STAGE DATA ENRICHMENT
# ==========================================

print("\n========== MULTI-STAGE ENRICHMENT ==========")

enrichment_chain = (
    normalize
    | RunnablePassthrough.assign(
        display_label=lambda data: (
            f"{data['topic']} ({data['level']})"
        )
    )
    | RunnablePassthrough.assign(
        label_length=lambda data: len(data["display_label"])
    )
)

result = enrichment_chain.invoke(raw_input)

print("Result:", result)


# ==========================================
# PART 6: DATA TRANSFORMATION WITH GROQ
# ==========================================

print("\n========== GROQ DATA TRANSFORMATION ==========")

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = PromptTemplate.from_template(
    "You are a programming tutor.\n"
    "Explain {topic} to a {level} student.\n"
    "Use exactly 3 simple sentences."
)

answer_chain = prompt | model | StrOutputParser()

# Normalize input, preserve fields, and add an AI answer
ai_chain = (
    normalize
    | RunnablePassthrough.assign(
        display_label=lambda data: (
            f"{data['topic']} ({data['level']})"
        ),
        explanation=answer_chain,
    )
    | RunnablePassthrough.assign(
        explanation_length=lambda data: len(
            str(data["explanation"])
        )
    )
)

try:
    result = ai_chain.invoke(raw_input)

    print("\nTOPIC:", result["topic"])
    print("LEVEL:", result["level"])
    print("DISPLAY LABEL:", result["display_label"])

    print("\nAI EXPLANATION:")
    print(str(result["explanation"]))

    print("\nEXPLANATION LENGTH:")
    print(result["explanation_length"])

    print("\nOUTPUT KEYS:")
    print(list(result.keys()))

    print("\nRESULT TYPE:")
    print(type(result))

except Exception as error:
    print("Groq data transformation failed:", error)


print("\nData Transformation example completed!")
