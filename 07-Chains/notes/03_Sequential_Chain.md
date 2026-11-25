# 03 — Sequential Chains in LangChain

## 1. What Is a Sequential Chain?

A sequential chain is a workflow where processing steps run in a specific order.

Each step receives the output of the previous step.

For example:

1. Generate an English explanation of a topic.
2. Translate that explanation into Urdu.
3. Return the translated explanation.

The second operation depends on the first, so they must execute sequentially.

## 2. Why Do We Need Sequential Chains?

Some AI applications require multiple dependent tasks.

Examples include:

- Summarizing a document and translating the summary.
- Generating an article and creating a title.
- Extracting information and generating a report.
- Analyzing code and suggesting improvements.

Instead of manually managing every model call, LangChain allows us to compose these steps into one workflow.

## 3. Simple Chain vs Sequential Chain

| Simple Chain                      | Multi-step Sequential Chain       |
| --------------------------------- | --------------------------------- |
| Usually performs one logical task | Performs multiple dependent tasks |
| Prompt → Model → Parser           | Chain 1 → Chain 2                 |
| One LLM request is common         | Multiple LLM requests are common  |
| Example: Explain Python           | Explain Python, then translate it |

Technically, both can use `RunnableSequence`. The difference here is the complexity of the logical workflow.

## 4. Creating the First Chain

We want to generate an English explanation.

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

explanation_prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in 3 simple sentences."
)

explanation_chain = (
    explanation_prompt
    | model
    | StrOutputParser()
)
```

This chain receives a topic and returns an explanation.

## 5. Creating the Second Chain

The next task translates the explanation into Urdu.

```python
translation_prompt = PromptTemplate.from_template(
    "Translate the following text into natural Urdu. "
    "Preserve its technical meaning:\n\n{text}"
)

translation_chain = (
    translation_prompt
    | model
    | StrOutputParser()
)
```

This chain expects a dictionary containing a `text` field.

## 6. Connecting the Two Chains

We can use `RunnableLambda` to transform the first chain's string output into the dictionary expected by the second chain.

```python
from langchain_core.runnables import RunnableLambda

sequential_chain = (
    explanation_chain
    | RunnableLambda(lambda text: {"text": str(text)})
    | translation_chain
)
```

### Explanation

- `explanation_chain` generates an English explanation.
- `RunnableLambda` converts the output into `{"text": ...}`.
- `translation_chain` translates the explanation.
- `sequential_chain.invoke()` executes both tasks.

## 7. Executing the Sequential Chain

```python
result = sequential_chain.invoke({
    "topic": "Machine Learning"
})

print(result)
```

The final result is the translated explanation.

## 8. Understanding Data Flow

```text
{"topic": "Machine Learning"}
             |
             v
      Explanation Prompt
             |
             v
           ChatGroq
             |
             v
       StrOutputParser
             |
             v
     English Explanation
             |
             v
        RunnableLambda
             |
             v
   {"text": "English text"}
             |
             v
       Translation Prompt
             |
             v
           ChatGroq
             |
             v
       StrOutputParser
             |
             v
       Urdu Explanation
```

## 9. What Is RunnableSequence?

`RunnableSequence` is a LangChain component that executes connected runnables in order.

The pipe operator creates a runnable sequence automatically:

```python
chain = prompt | model | parser
```

It is also possible to construct a sequence explicitly.

```python
from langchain_core.runnables import RunnableSequence

chain = RunnableSequence(
    prompt,
    model,
    parser
)
```

The pipe syntax is generally easier to read.

## 10. What Is RunnableLambda?

`RunnableLambda` wraps a Python function so it can participate in LangChain runnable workflows.

Example:

```python
from langchain_core.runnables import RunnableLambda

double = RunnableLambda(lambda number: number * 2)

print(double.invoke(5))
```

Output:

```text
10
```

In our translation workflow, we use `RunnableLambda` to adapt the data passed between two chains.

## 11. Why Does the Input Format Matter?

Our second prompt expects:

```python
{"text": "An English explanation"}
```

But the first chain returns a string.

Therefore, we need an adapter to convert:

```text
"An English explanation"
```

into:

```python
{"text": "An English explanation"}
```

This is why understanding input and output types is important when building chains.

## 12. Alternative: Direct String Input

In many LangChain versions, a prompt template containing only one required variable can accept a direct string input.

Therefore, the following may also work:

```python
sequential_chain = explanation_chain | translation_chain
```

However, the explicit dictionary adapter makes the data flow easier to understand and works well when additional fields are introduced.

## 13. Common Beginner Mistakes

**Mistake 1 — Passing incompatible outputs between chains**

Each runnable must receive an input format it supports.

**Mistake 2 — Assuming two LLM calls happen in parallel**

Sequential chains execute dependent steps in order.

**Mistake 3 — Forgetting that both tasks use the API**

Our example makes two Groq model requests for one user input.

**Mistake 4 — Losing intermediate results**

A basic sequential chain returns the final result. If an application also needs the English explanation, it must preserve that intermediate result.

**Mistake 5 — Assuming sequential chains are agents**

A sequential chain follows predefined steps rather than dynamically deciding which tools to use.

## 14. Interview Questions

**Q1. What is a sequential chain?**

A workflow in which the output of one step becomes the input of another.

**Q2. Why use sequential chains?**

To perform multiple dependent tasks in a predefined order.

**Q3. What is RunnableSequence?**

A LangChain runnable that executes connected components sequentially.

**Q4. What is RunnableLambda?**

A wrapper that allows Python functions to participate in runnable workflows.

**Q5. Does a sequential chain require multiple LLM calls?**

No. It can also combine ordinary Python processing steps, although our example uses two model calls.

**Q6. What happens if the first step fails?**

The workflow normally stops and propagates the error unless error handling or fallback logic is configured.

**Q7. What is the difference between sequential and parallel chains?**

Sequential steps depend on one another; parallel branches can run independently.

## 15. Key Takeaways

- Sequential chains execute connected tasks in order.
- The output of one step feeds the next.
- `RunnableSequence` implements sequential composition.
- The `|` operator connects compatible runnables.
- `RunnableLambda` can adapt data between steps.
- Each step must receive the correct input format.
- Sequential chains are useful for summarization, translation, reporting, and multi-stage processing.
- Multiple model steps may increase API usage and latency.

---

## Learning Resources

- [CampusX LangChain Chains Repository](https://github.com/campusx-official/langchain-chains)
- [LangChain RunnableSequence Reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSequence)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 07 — Topic 03
