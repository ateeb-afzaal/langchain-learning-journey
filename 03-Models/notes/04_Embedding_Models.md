# 04 — Embedding Models in LangChain

## 1. What Is an Embedding Model?

An embedding model converts information, such as text, into a numerical representation called a **vector**.

In simple words, an embedding model transforms text into numbers so that computers can compare its meaning with other text.

### Example

Input:

```text
"Python is a programming language."
```

Illustrative output:

```text
[0.12, -0.45, 0.78, 0.21, ...]
```

The actual numbers depend on the embedding model.

## 2. Why Do We Need Embeddings?

Computers cannot directly compare the semantic meaning of two sentences in the way humans do.

Consider:

**Sentence A:** "I love programming in Python."

**Sentence B:** "Python coding is my favorite activity."

**Sentence C:** "The weather is beautiful today."

Sentences A and B have similar meanings, even though their wording is different.

An embedding model converts these sentences into vectors so we can measure how similar their representations are.

**Important:** Embeddings approximate semantic relationships. They do not perfectly understand meaning.

## 3. What Is a Vector?

A vector is an ordered collection of numerical values.

Example:

```text
[0.25, -0.61, 0.43]
```

This example has three dimensions because it contains three values.

Embedding models commonly produce vectors with hundreds or thousands of dimensions.

### What Are Vector Dimensions?

The number of values in a vector is called its dimensionality.

For example:

```text
[0.1, 0.2, 0.3] → 3 dimensions
```

The model `sentence-transformers/all-MiniLM-L6-v2` produces embeddings with **384 dimensions**.

This means each text input is represented by a vector containing 384 numbers.

## 4. Language Models vs Embedding Models

| Language Model               | Embedding Model                     |
| ---------------------------- | ----------------------------------- |
| Generates language           | Generates numerical vectors         |
| Used for answering questions | Used for semantic comparison        |
| Produces text or messages    | Produces lists or arrays of numbers |
| Example: GPT-OSS 120B        | Example: all-MiniLM-L6-v2           |
| Useful for chatbots          | Useful for retrieval and search     |

A RAG application often uses both types of models.

## 5. What Is Semantic Similarity?

Semantic similarity measures how closely related the meanings of two pieces of text are.

For example:

```text
Text A: "How can I learn Python?"
Text B: "What is the best way to study Python programming?"
```

These are semantically similar.

But:

```text
Text C: "How do I cook chicken?"
```

has a different meaning.

An embedding model allows us to compare their vectors mathematically.

## 6. Cosine Similarity

One popular way to compare embedding vectors is **cosine similarity**.

It measures the cosine of the angle between two nonzero vectors.

Formula:

\[
\operatorname{cosine}(A,B)=\frac{A\cdot B}{\|A\|\|B\|}
\]

### Interpretation

- **1:** Vectors point in the same direction.
- **0:** Vectors are perpendicular.
- **-1:** Vectors point in opposite directions.

For text embeddings, higher cosine similarity often suggests stronger semantic similarity.

However, similarity scores are model-dependent and should not be treated as guaranteed probabilities of meaning.

## 7. Types of Embedding Applications

### Semantic Search

Find documents based on their meaning rather than exact keywords.

### Document Retrieval

Retrieve relevant parts of documents to help answer a question.

### Recommendation Systems

Compare descriptions of products, articles, or other items.

### Clustering

Group related texts according to their vector representations.

### RAG

Retrieve relevant information and provide it to a language model before generating an answer.

## 8. Using Hugging Face Embeddings in LangChain

For this learning journey, we use the following model:

`sentence-transformers/all-MiniLM-L6-v2`

Install the required packages:

```powershell
python -m pip install langchain-huggingface sentence-transformers
```

### Example: Generate an Embedding

```python
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = embedding_model.embed_query(
    "LangChain is a framework for building AI applications."
)

print("Vector dimensions:", len(vector))
print("First 10 values:", vector[:10])
```

### Code Explanation

**`HuggingFaceEmbeddings`**

Provides a LangChain integration for supported Hugging Face embedding models.

**`model_name`**

Specifies which embedding model to load.

**`embed_query()`**

Converts one input query into a numerical vector.

**`len(vector)`**

Returns the number of vector dimensions.

**`vector[:10]`**

Displays the first ten numerical values.

Expected vector dimensions:

```text
384
```

## 9. embed_query() vs embed_documents()

LangChain provides two commonly used embedding methods.

### embed_query()

Usually used for a search question or query.

```python
query_vector = embedding_model.embed_query(
    "What is machine learning?"
)
```

Returns one embedding vector.

### embed_documents()

Used to convert multiple documents into embeddings.

```python
documents = [
    "Python is used for data science.",
    "LangChain helps build AI applications.",
    "Machine learning uses data to learn patterns."
]

document_vectors = embedding_model.embed_documents(documents)

print("Documents:", len(document_vectors))
print("Dimensions:", len(document_vectors[0]))
```

For this model, the output contains three vectors, each with 384 dimensions.

Some embedding models treat queries and documents differently, so using the appropriate method matters.

## 10. Practical Semantic Similarity Example

We can compare three sentences.

```python
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

sentences = [
    "I enjoy writing Python code.",
    "Python programming is my favorite activity.",
    "The weather is sunny today."
]

vectors = model.embed_documents(sentences)

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

score_1 = cosine_similarity(vectors[0], vectors[1])
score_2 = cosine_similarity(vectors[0], vectors[2])

print("Python vs Python:", round(float(score_1), 4))
print("Python vs Weather:", round(float(score_2), 4))
```

### Expected Behavior

The two Python-related sentences should generally have a higher similarity score than the Python and weather sentences.

The exact scores depend on the selected embedding model.

## 11. How Embeddings Work in RAG

A simple RAG workflow looks like this:

```text
Documents
    |
    v
Text Splitting
    |
    v
Embedding Model
    |
    v
Vector Store
    |
    v
Relevant Document Retrieval
    |
    v
Question + Retrieved Context
    |
    v
Language Model
    |
    v
Final Answer
```

### Step-by-Step Explanation

1. Load documents.
2. Divide large documents into smaller chunks.
3. Generate embeddings for each chunk.
4. Store the embeddings in a vector store.
5. Convert the user's question into an embedding.
6. Retrieve the most relevant chunks.
7. Provide those chunks to the language model.
8. Generate an answer.

The retrieval step helps the language model use external information instead of relying only on its learned knowledge.

## 12. Common Interview Questions

**Q1. What is an embedding?**

A numerical vector representation of information, such as text.

**Q2. What is an embedding model?**

A model that converts input data into vectors.

**Q3. What is semantic similarity?**

A measurement of how closely related the meanings of two inputs are.

**Q4. What is cosine similarity?**

A mathematical measure of the direction-based similarity of two vectors.

**Q5. What are embedding dimensions?**

The number of numerical values in an embedding vector.

**Q6. What is the difference between `embed_query()` and `embed_documents()`?**

The first embeds a query; the second embeds a collection of documents.

**Q7. Why are embeddings important for RAG?**

They help retrieve relevant information from external knowledge sources.

**Q8. Does an embedding model generate answers like ChatGPT?**

No. Its primary output is a numerical representation rather than a conversational answer.

## 13. Key Takeaways

- Embedding models convert text into numerical vectors.
- Similar texts often have similar vector representations.
- Vector dimensions depend on the selected embedding model.
- Cosine similarity is one way to compare vectors.
- LangChain provides `embed_query()` and `embed_documents()`.
- Hugging Face embedding models can run locally.
- Embeddings are fundamental to semantic search, vector stores, and RAG.

---

## Learning Resources

- [CampusX LangChain Models](https://github.com/campusx-official/langchain-models)
- [Sentence Transformers](https://www.sbert.net/)
- [Hugging Face all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 03 — Topic 04
