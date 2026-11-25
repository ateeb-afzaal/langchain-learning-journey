
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

# Step 1: Load the Groq API key
load_dotenv()

# Step 2: Initialize the LLM
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 3: Create three different prompts
beginner_prompt = PromptTemplate.from_template(
    "Explain {topic} to a complete beginner. "
    "Use simple English and one everyday example."
)

advanced_prompt = PromptTemplate.from_template(
    "Explain {topic} to an advanced computer science student. "
    "Include technical details and one practical example."
)

default_prompt = PromptTemplate.from_template(
    "Explain {topic} clearly for a general audience."
)

# Step 4: Create independent chains
beginner_chain = beginner_prompt | model | StrOutputParser()
advanced_chain = advanced_prompt | model | StrOutputParser()
default_chain = default_prompt | model | StrOutputParser()

# Step 5: Define conditions
def is_beginner(data):
    return str(data.get("level", "")).lower() == "beginner"

def is_advanced(data):
    return str(data.get("level", "")).lower() == "advanced"

# Step 6: Create conditional chain
conditional_chain = RunnableBranch(
    (is_beginner, beginner_chain),
    (is_advanced, advanced_chain),
    default_chain
)

# Step 7: Prepare test cases
test_cases = [
    {"topic": "Neural Networks", "level": "beginner"},
    {"topic": "Neural Networks", "level": "advanced"},
    {"topic": "Neural Networks", "level": "intermediate"},
]

# Step 8: Execute each test case
for data in test_cases:
    print("\n" + "=" * 50)
    print("Topic:", data["topic"])
    print("Level:", data["level"])
    print("=" * 50)

    try:
        result = conditional_chain.invoke(data)
        print(str(result))
    except Exception as error:
        print("Chain failed:", error)
