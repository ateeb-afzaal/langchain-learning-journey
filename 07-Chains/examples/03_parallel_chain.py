
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

# Step 1: Load Groq API key
load_dotenv()

# Step 2: Initialize the model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 3: Create summary prompt
summary_prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in 3 simple sentences."
)

# Step 4: Create interview questions prompt
questions_prompt = PromptTemplate.from_template(
    "Generate exactly 3 interview questions about {topic}. "
    "Return a numbered list without answers."
)

# Step 5: Create two independent chains
summary_chain = (
    summary_prompt
    | model
    | StrOutputParser()
)

questions_chain = (
    questions_prompt
    | model
    | StrOutputParser()
)

# Step 6: Combine chains using RunnableParallel
parallel_chain = RunnableParallel(
    summary=summary_chain,
    questions=questions_chain
)

# Step 7: Run both branches
try:
    result = parallel_chain.invoke({
        "topic": "Python decorators"
    })

    print("========== PARALLEL CHAIN ==========")

    print("\nSUMMARY:\n")
    print(str(result["summary"]))

    print("\nINTERVIEW QUESTIONS:\n")
    print(str(result["questions"]))

    print("\nRESULT TYPE:")
    print(type(result))

except Exception as error:
    print("Parallel chain failed:", error)
