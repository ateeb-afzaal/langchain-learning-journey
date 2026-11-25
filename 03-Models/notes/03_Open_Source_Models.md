# 03 — Open-Source Models and Hugging Face

## 1. What Are Open-Source AI Models?

Open-source AI models are models whose development resources are made available under an open-source license.

However, many models described as _open-source_ are more accurately called **open-weight models**, because their trained weights are available but their training data, code, or processes may not be fully open.

Examples of open-weight model families include:

- Llama
- Gemma
- Qwen
- GPT-OSS
- Mistral

The exact license and usage restrictions depend on the model.

## 2. Open-Weight vs Proprietary Models

| Feature               | Open-Weight Models    | Proprietary Models              |
| --------------------- | --------------------- | ------------------------------- |
| Model weights         | Available to download | Generally not public            |
| Local deployment      | Often possible        | Generally unavailable           |
| Customization         | Often possible        | Depends on provider             |
| Hardware requirements | Depends on model size | Usually managed by provider     |
| Examples              | Llama, Qwen, GPT-OSS  | Closed-weight commercial models |

**Important:** Open-weight does not automatically mean unrestricted use.

Always check the model's license before using it commercially.

## 3. What Is Hugging Face?

Hugging Face is an AI ecosystem that provides tools and services for discovering, downloading, training, sharing, and running machine learning models.

Its main resources include:

**Hugging Face Hub**

A platform for hosting models, datasets, and AI demos.

**Transformers**

A Python library for loading and using many transformer-based models.

**Datasets**

A library for accessing and processing machine learning datasets.

**Sentence Transformers**

A library commonly used to generate text embeddings.

**Hugging Face Spaces**

A platform for publishing interactive machine learning applications.

## 4. Running Models: Hosted vs Local

There are two common ways to use an AI model.

### A. Hosted Inference

A remote service runs the model.

Your application sends a request over the internet and receives a result.

Example:

```text
Python Application
       |
       v
    Groq API
       |
       v
  GPT-OSS 120B
       |
       v
   AI Response
```

**Advantages:**

- No need for a powerful local GPU.
- Faster to set up.
- Infrastructure is managed by the provider.

**Limitations:**

- Requires network access.
- May have API limits or charges.
- Input is processed by the external service.

### B. Local Inference

The model runs on your own computer or server.

Example:

```text
Python Application
       |
       v
 Local Model Runtime
       |
       v
 Downloaded Model
       |
       v
   AI Response
```

**Advantages:**

- Greater control over deployment.
- Can work without an internet connection after setup.
- Data can remain on your own hardware.

**Limitations:**

- Requires suitable RAM, CPU, or GPU resources.
- Large models may run slowly.
- You must manage the model runtime yourself.

## 5. What Does Model Size Mean?

Model sizes are often described using parameter counts.

Examples:

- 0.5B = approximately 500 million parameters.
- 7B = approximately 7 billion parameters.
- 120B = approximately 120 billion parameters.

A larger parameter count does not automatically guarantee better results.

Performance also depends on training quality, architecture, task suitability, inference settings, and hardware.

## 6. What Is Quantization?

Quantization reduces the numerical precision used to store or compute model weights.

For example, a model may use lower-precision representations instead of standard 16-bit floating-point weights.

**Why is it useful?**

- Can reduce memory requirements.
- May improve inference efficiency.
- Makes some models practical on smaller devices.

**Trade-off:** Depending on the technique, quantization can affect model accuracy and output quality.

## 7. Using an Open-Weight Model Through Groq

We already use an open-weight model in this learning journey: GPT-OSS 120B.

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

response = model.invoke(
    "Explain the difference between open-weight and proprietary AI models."
)

print(response.content)
```

Although the model has publicly available weights, **this example runs it through Groq's hosted infrastructure**.

It does not download or run GPT-OSS locally.

## 8. Running a Smaller Model Locally

Hugging Face Transformers can run supported models locally.

For example:

```python
from transformers import pipeline

generator = pipeline(
    task="text-generation",
    model="HuggingFaceTB/SmolLM2-135M-Instruct",
    device=-1
)

messages = [
    {"role": "user", "content": "Explain Python in one sentence."}
]

result = generator(
    messages,
    max_new_tokens=60,
    do_sample=False
)

print(result[0]["generated_text"])
```

### Explanation

- `pipeline()` creates a text-generation pipeline.
- `model` selects a small public model.
- `device=-1` requests CPU inference.
- `max_new_tokens` limits the generated response.
- `do_sample=False` disables sampling.

**Note:** The first run downloads the model files. Local execution can take time and consumes memory. This small model is for demonstration, not for high-quality production answers.

## 9. When Should We Use Hosted or Local Models?

| Situation                            | Suitable Approach                            |
| ------------------------------------ | -------------------------------------------- |
| Learning LangChain quickly           | Hosted API                                   |
| No powerful GPU available            | Hosted API                                   |
| Offline application required         | Local model                                  |
| Sensitive data must remain on device | Local deployment                             |
| Large-scale application              | Depends on cost, latency, and infrastructure |
| Experimenting with small models      | Local or hosted                              |

## 10. Hugging Face and LangChain

LangChain provides integrations for several Hugging Face workflows, including embeddings and supported inference endpoints.

For example, we can use a Hugging Face embedding model to convert text into vectors.

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = embeddings.embed_query(
    "LangChain helps developers build AI applications."
)

print("Vector dimensions:", len(vector))
print("First five values:", vector[:5])
```

The selected embedding model produces vectors with **384 dimensions**.

We'll study this properly in Topic 04.

## 11. Quick Revision Questions

**Q1. What is an open-weight model?**

A model whose trained weights are available for download under its license.

**Q2. What is Hugging Face?**

An ecosystem for sharing, discovering, and working with AI models and datasets.

**Q3. What is hosted inference?**

Running a model on infrastructure managed by an external provider.

**Q4. What is local inference?**

Running a model on your own computer or server.

**Q5. What is quantization?**

Reducing numerical precision to make model storage or inference more efficient.

**Q6. Does using GPT-OSS through Groq mean we're running it locally?**

No. Groq runs the model remotely.

**Q7. Does a larger model always perform better?**

No. Performance depends on more than parameter count.

## 12. Key Takeaways

- Open-weight models provide downloadable trained weights.
- Open-weight and fully open-source are not always the same.
- Hugging Face hosts models, datasets, and related tools.
- Hosted inference runs on external infrastructure.
- Local inference runs on your own hardware.
- Quantization can reduce model memory requirements.
- LangChain works with hosted model providers and supported local model integrations.

---

## Learning Resources

- [CampusX LangChain Models](https://github.com/campusx-official/langchain-models)
- [Hugging Face](https://huggingface.co/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 03 — Topic 03
