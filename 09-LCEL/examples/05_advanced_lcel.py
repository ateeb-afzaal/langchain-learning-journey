
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnableBranch,
    RunnablePassthrough,
)


# ==========================================
# PART 1: SEQUENTIAL COMPOSITION
# ==========================================

print("========== RUNNABLE SEQUENCE ==========")

double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)

sequence = double | add_five

print("Input: 5")
print("Output:", sequence.invoke(5))


# ==========================================
# PART 2: PARALLEL COMPOSITION
# ==========================================

print("\n========== RUNNABLE PARALLEL ==========")

parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2),
)

print("Input: 5")
print("Output:", parallel.invoke(5))


# ==========================================
# PART 3: CONDITIONAL ROUTING
# ==========================================

print("\n========== RUNNABLE BRANCH ==========")

local_branch = RunnableBranch(
    (
        lambda data: data["level"] == "beginner",
        RunnableLambda(lambda data: "Beginner workflow selected")
    ),
    (
        lambda data: data["level"] == "advanced",
        RunnableLambda(lambda data: "Advanced workflow selected")
    ),
    RunnableLambda(lambda data: "Default workflow selected")
)

for level in ["beginner", "advanced", "intermediate"]:
    result = local_branch.invoke({"level": level})
    print(f"{level}: {result}")


# ==========================================
# PART 4: ERROR HANDLING AND FALLBACK
# ==========================================

print("\n========== RUNNABLE FALLBACK ==========")

def failing_function(number):
    raise ValueError("Primary operation failed")


primary = RunnableLambda(failing_function)
fallback = RunnableLambda(lambda number: number * 2)

safe_chain = primary.with_fallbacks([fallback])

print("Input: 5")
print("Fallback Output:", safe_chain.invoke(5))


# ==========================================
# PART 5: ADVANCED LCEL WITH GROQ
# ==========================================

print("\n========== ADVANCED LCEL WITH GROQ ==========")

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# Step 1: Normalize and validate
def normalize_input(data):

    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary")

    topic = data.get("topic")
    level = data.get("level", "beginner")

    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("Topic cannot be empty")

    if not isinstance(level, str):
        raise TypeError("Level must be a string")

    level = level.strip().lower()

    if level not in {"beginner", "advanced"}:
        raise ValueError(
            "Level must be 'beginner' or 'advanced'"
        )

    return {
        "topic": topic.strip(),
        "level": level
    }


normalize = RunnableLambda(normalize_input)


# Step 2: Define prompts
beginner_prompt = PromptTemplate.from_template(
    "You are a friendly programming tutor. "
    "Explain {topic} to a beginner in 3 simple sentences."
)

advanced_prompt = PromptTemplate.from_template(
    "You are a senior software engineer. "
    "Explain {topic} to an advanced CS student "
    "using technical terminology and one practical example."
)

questions_prompt = PromptTemplate.from_template(
    "Generate exactly 3 interview questions about {topic}. "
    "Return only a numbered list."
)


# Step 3: Create model chains
beginner_chain = beginner_prompt | model | StrOutputParser()
advanced_chain = advanced_prompt | model | StrOutputParser()
questions_chain = questions_prompt | model | StrOutputParser()


# Step 4: Create conditional explanation branch
explanation_branch = RunnableBranch(
    (
        lambda data: data["level"] == "beginner",
        beginner_chain
    ),
    advanced_chain
)


# Step 5: Combine everything using LCEL
study_chain = (
    normalize
    | RunnablePassthrough.assign(
        display_label=lambda data: (
            f"{data['topic']} ({data['level']})"
        ),
        explanation=explanation_branch,
        questions=questions_chain,
    )
    | RunnablePassthrough.assign(
        explanation_length=lambda data: len(
            str(data["explanation"])
        )
    )
)


# Step 6: Execute
test_input = {
    "topic": "  Python Decorators  ",
    "level": "BEGINNER"
}

try:
    result = study_chain.invoke(test_input)

    print("\nTOPIC:", result["topic"])
    print("LEVEL:", result["level"])
    print("DISPLAY LABEL:", result["display_label"])

    print("\nEXPLANATION:")
    print(str(result["explanation"]))

    print("\nINTERVIEW QUESTIONS:")
    print(str(result["questions"]))

    print("\nEXPLANATION LENGTH:")
    print(result["explanation_length"])

    print("\nRESULT TYPE:")
    print(type(result))

    print("\nOUTPUT KEYS:")
    print(list(result.keys()))

except ValueError as error:
    print("Validation failed:", error)

except Exception as error:
    print("Advanced LCEL workflow failed:", error)


# ==========================================
# PART 6: TEST VALIDATION WITHOUT GROQ
# ==========================================

print("\n========== VALIDATION TEST ==========")

try:
    normalize.invoke({
        "topic": "   ",
        "level": "beginner"
    })

except ValueError as error:
    print("Expected validation error:", error)


print("\nAdvanced LCEL example completed!")
