
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Load Groq API key
load_dotenv()

# Step 2: Initialize the model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 3: Create prompt
prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in 3 sentences."
)

# Step 4: Initialize parser
parser = StrOutputParser()

# Step 5: Create simple chain
chain = prompt | model | parser

# Example 1: invoke()
print("========== INVOKE ==========")

result = chain.invoke({
    "topic": "Machine Learning"
})

print(str(result))


# Example 2: batch()
print("\n========== BATCH ==========")

topics = [
    {"topic": "Python"},
    {"topic": "Deep Learning"},
    {"topic": "Computer Vision"}
]

# Process up to two requests concurrently
results = chain.batch(
    topics,
    config={"max_concurrency": 2}
)

for topic, answer in zip(topics, results):
    print(f"\nTopic: {topic['topic']}")
    print(str(answer))


# Example 3: stream()
print("\n========== STREAM ==========")

for chunk in chain.stream({
    "topic": "Artificial Intelligence"
}):
    print(chunk, end="", flush=True)

print("\n\nAll examples completed!")
