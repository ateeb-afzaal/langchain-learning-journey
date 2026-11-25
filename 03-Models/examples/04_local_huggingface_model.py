
from transformers import pipeline

# Load a small open-weight model for local CPU inference
generator = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
    device=-1
)

# Ask a question
messages = [
    {"role": "user", "content": "What is machine learning? Answer briefly."}
]

# Generate a response
result = generator(
    messages,
    max_new_tokens=80,
    do_sample=False
)

# Display the result
print(result[0]["generated_text"])
