
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

# Step 1: Load Groq API key
load_dotenv()

# Step 2: Initialize the LLM
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 3: Prompt for the English explanation
explanation_prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in exactly 3 simple English sentences."
)

# Step 4: Create the first chain
explanation_chain = (
    explanation_prompt
    | model
    | StrOutputParser()
)

# Step 5: Prompt for translation
translation_prompt = PromptTemplate.from_template(
    "Translate the following explanation into natural Urdu. "
    "Preserve the technical meaning. "
    "Return only the Urdu translation.\n\n{text}"
)

# Step 6: Create the second chain
translation_chain = (
    translation_prompt
    | model
    | StrOutputParser()
)

# Step 7: Connect both chains sequentially
sequential_chain = (
    explanation_chain
    | RunnableLambda(lambda text: {"text": str(text)})
    | translation_chain
)

# Step 8: Execute the complete workflow
print("========== SEQUENTIAL CHAIN ==========")

try:
    result = sequential_chain.invoke({
        "topic": "Machine Learning"
    })

    print("\nFINAL URDU EXPLANATION:\n")
    print(str(result))

except Exception as error:
    print("Chain failed:", error)
