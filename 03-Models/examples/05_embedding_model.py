
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

# Step 1: Load a local Hugging Face embedding model
model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Step 2: Prepare example sentences
sentences = [
    "I love Python programming.",
    "I enjoy writing code in Python.",
    "I like eating pizza."
]

# Step 3: Convert all sentences into numerical vectors
vectors = model.embed_documents(sentences)

print("Number of embeddings:", len(vectors))
print("Vector dimensions:", len(vectors[0]))

# Step 4: Define cosine similarity
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return float(
        np.dot(a, b)
        / (np.linalg.norm(a) * np.linalg.norm(b))
    )

# Step 5: Compare the sentences
score_1 = cosine_similarity(vectors[0], vectors[1])
score_2 = cosine_similarity(vectors[0], vectors[2])

print("\nSimilarity Results:")
print("Python vs Python:", round(score_1, 4))
print("Python vs Pizza:", round(score_2, 4))

# Step 6: Identify the most similar sentence
if score_1 > score_2:
    print("\nThe two Python sentences are more similar.")
else:
    print("\nThe second comparison scored higher.")
