# 04 — Parallel Chains in LangChain

## 1. What Is a Parallel Chain?

A parallel chain is a LangChain workflow that processes the same input through multiple independent branches.

Each branch performs a different task, and the results are combined into one structured output.

For example:

- Branch 1 generates a summary.
- Branch 2 generates interview questions.
- Both receive the same programming topic.

LangChain provides `RunnableParallel` for this purpose.

## 2. Why Do We Need Parallel Chains?

Imagine an educational assistant that must generate:

1. A topic summary.
2. Interview questions.
3. Important keywords.

These tasks do not depend on one another.

Running independent tasks concurrently can be more efficient than executing them one after another.

### Common Applications

- Generate summaries and quizzes.
- Analyze sentiment and classify text.
- Extract multiple types of information.
- Produce alternative explanations.
- Run independent document-processing operations.

## 3. Sequential vs Parallel Chains

| Sequential Chain                         | Parallel Chain                            |
| ---------------------------------------- | ----------------------------------------- |
| Steps depend on earlier outputs          | Branches are independent                  |
| Executes dependent stages in order       | Can execute branches concurrently         |
| Output of step A becomes input to step B | Multiple branches receive shared input    |
| Example: Summarize then translate        | Example: Summarize and generate questions |

## 4. What Is RunnableParallel?

`RunnableParallel` is a LangChain component that accepts multiple runnable branches.

It passes the same input to each branch and returns their outputs in a dictionary.

### Basic Syntax

```python
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    summary=summary_chain,
    questions=questions_chain
)
```

Here:

- `summary` is the name of the first output.
- `questions` is the name of the second output.
- Each branch receives the same input.
- The final result contains both outputs.

## 5. Creating the Summary Chain

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

summary_prompt = PromptTemplate.from_template(
    "Explain {topic} in three simple sentences."
)

summary_chain = (
    summary_prompt
    | model
    | StrOutputParser()
)
```

This branch generates a beginner-friendly explanation.

## 6. Creating the Questions Chain

```python
questions_prompt = PromptTemplate.from_template(
    "Generate three interview questions about {topic}. "
    "Return a numbered list."
)

questions_chain = (
    questions_prompt
    | model
    | StrOutputParser()
)
```

This branch generates interview questions.

## 7. Combining Both Branches

```python
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    summary=summary_chain,
    questions=questions_chain
)

result = parallel_chain.invoke({
    "topic": "Python decorators"
})
```

The final result is a dictionary containing two values.

```python
print(result["summary"])
print(result["questions"])
```

## 8. Understanding the Execution Flow

```text
                 Topic
                   |
                   v
            RunnableParallel
                   |
          +--------+--------+
          |                 |
          v                 v
     Summary Chain     Questions Chain
          |                 |
          v                 v
      Summary Text     Questions Text
          |                 |
          +--------+--------+
                   |
                   v
            Result Dictionary
```

## 9. What Does RunnableParallel Return?

`RunnableParallel` returns a mapping of branch names to results.

Example:

```python
{
    "summary": "Decorators allow functions to be wrapped...",
    "questions": "1. What is a decorator?\n2. ..."
}
```

Each branch can return a different type of value, depending on its processing components.

## 10. Using a Dictionary Instead of RunnableParallel

LangChain can also interpret a dictionary of runnable components as a parallel workflow when used in LCEL composition.

Example:

```python
parallel_chain = {
    "summary": summary_chain,
    "questions": questions_chain
}
```

To execute this directly using the Runnable interface, we should explicitly wrap it:

```python
parallel_chain = RunnableParallel({
    "summary": summary_chain,
    "questions": questions_chain
})
```

Using `RunnableParallel` makes the intention clear.

## 11. Concurrency and API Rate Limits

Parallel chains may send multiple model requests at approximately the same time.

This can improve latency, but it may also:

- Increase concurrent API usage.
- Trigger provider rate limits.
- Increase resource consumption.
- Cause the overall workflow to fail if one branch raises an exception.

For Groq experiments, keep the number of simultaneous branches small.

Parallel processing does not reduce the total number of model calls.

## 12. Handling Errors

If a branch fails, the overall parallel chain normally raises an exception unless the workflow has explicit error handling.

Example:

```python
try:
    result = parallel_chain.invoke({
        "topic": "Python decorators"
    })
    print(result)
except Exception as error:
    print("Parallel chain failed:", error)
```

For production systems, retry policies, fallbacks, and rate-limit management may be necessary.

## 13. Sequential vs Parallel: Which Should We Use?

Use a **sequential chain** when one task depends on another.

Example:

Generate English text → Translate generated text.

Use a **parallel chain** when tasks can run independently.

Example:

Generate a summary and generate interview questions from the same topic.

## 14. Common Beginner Mistakes

**Mistake 1 — Assuming parallel means one API call**

Two model branches normally make two separate model requests.

**Mistake 2 — Assuming parallel always means faster**

Latency depends on provider limits, resource availability, and component behavior.

**Mistake 3 — Passing incompatible input variables**

Each branch must accept the input provided to it.

**Mistake 4 — Confusing branch names with prompt variables**

Names such as `summary` and `questions` identify output fields. The prompt variable `{topic}` represents input data.

**Mistake 5 — Ignoring failures**

One branch failing can prevent the combined result from being returned.

## 15. Interview Questions

**Q1. What is a parallel chain?**

A workflow that runs multiple independent processing branches using shared input.

**Q2. What is RunnableParallel?**

A LangChain runnable that runs branches concurrently where possible and combines their outputs.

**Q3. What does RunnableParallel return?**

A dictionary mapping branch names to their outputs.

**Q4. What is the difference between sequential and parallel chains?**

Sequential chains connect dependent operations, while parallel chains execute independent branches.

**Q5. Does RunnableParallel reduce API usage?**

No. Each branch may still make its own model request.

**Q6. Can parallel chains have different prompts?**

Yes.

**Q7. Can parallel chains contain non-LLM components?**

Yes. Branches can include other runnable components and Python functions.

**Q8. What happens when a branch fails?**

The overall workflow normally raises an exception unless error handling is configured.

## 16. Key Takeaways

- Parallel chains process shared input through independent branches.
- `RunnableParallel` combines these branches.
- Each branch can have its own prompt, model, and parser.
- The final result is a dictionary.
- Parallel execution can reduce latency for independent tasks.
- Multiple branches can increase concurrent API usage.
- Parallel chains are useful for generating multiple outputs from the same input.

---

## Learning Resources

- [CampusX LangChain Chains Repository](https://github.com/campusx-official/langchain-chains)
- [LangChain RunnableParallel Reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableParallel)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 07 — Topic 04
