# 06 — LangChain Chains: Quick Revision

## 1. What Is a Chain?

A chain is a reusable workflow that connects multiple processing components in LangChain.

These components can include prompts, language models, output parsers, Python functions, and other runnables.

Example:

```python
chain = prompt | model | parser
```

The pipe operator (`|`) connects compatible runnable components.

## 2. Main Types of Chains

| Chain Type        | Purpose                               | Example                 |
| ----------------- | ------------------------------------- | ----------------------- |
| Simple Chain      | Connect basic processing steps        | Prompt → Model → Parser |
| Sequential Chain  | Execute dependent tasks in order      | Explain → Translate     |
| Parallel Chain    | Run independent tasks concurrently    | Summary + Questions     |
| Conditional Chain | Select a workflow based on conditions | Beginner vs Advanced    |

## 3. Important LangChain Components

| Component          | Purpose                                                |
| ------------------ | ------------------------------------------------------ |
| `RunnableSequence` | Execute connected processing steps sequentially        |
| `RunnableParallel` | Execute independent branches and combine their outputs |
| `RunnableBranch`   | Select a branch based on predefined conditions         |
| `RunnableLambda`   | Wrap a Python function as a runnable                   |
| `PromptTemplate`   | Create reusable text prompts                           |
| `ChatGroq`         | Connect to a Groq-hosted chat model                    |
| `StrOutputParser`  | Extract generated response text                        |

## 4. Simple Chain

A simple chain connects a prompt, model, and parser.

```python
chain = prompt | model | StrOutputParser()

result = chain.invoke({
    "topic": "Machine Learning"
})
```

### Important Methods

- `invoke()` — Process one input.
- `batch()` — Process multiple inputs.
- `stream()` — Produce incremental output when supported.

## 5. Sequential Chain

A sequential chain connects dependent tasks.

Example:

1. Generate an English explanation.
2. Translate it into Urdu.

```python
from langchain_core.runnables import RunnableLambda

sequential_chain = (
    explanation_chain
    | RunnableLambda(lambda text: {"text": str(text)})
    | translation_chain
)
```

**Key point:** The second task depends on the result of the first task.

## 6. Parallel Chain

A parallel chain executes independent branches.

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

The result contains both outputs:

```python
{
    "summary": "...",
    "questions": "..."
}
```

**Key point:** Both branches receive the same input.

Parallel execution may improve latency, but it doesn't necessarily reduce API requests.

## 7. Conditional Chain

A conditional chain executes a selected branch based on a condition.

```python
from langchain_core.runnables import RunnableBranch

conditional_chain = RunnableBranch(
    (
        lambda x: x.get("level") == "beginner",
        beginner_chain
    ),
    (
        lambda x: x.get("level") == "advanced",
        advanced_chain
    ),
    default_chain
)
```

### How It Works

1. Check the first condition.
2. Execute its chain if the condition is true.
3. Otherwise, check the next condition.
4. If no condition matches, execute the default chain.

**Key point:** Only the first matching branch executes.

## 8. Sequential vs Parallel vs Conditional

| Feature             | Sequential                       | Parallel                             | Conditional            |
| ------------------- | -------------------------------- | ------------------------------------ | ---------------------- |
| Execution           | In order                         | Independent branches                 | Selected branch        |
| Dependency          | Steps depend on previous outputs | Branches don't depend on one another | Depends on conditions  |
| Typical output      | Final result of last step        | Dictionary of results                | Selected branch result |
| LangChain component | `RunnableSequence`               | `RunnableParallel`                   | `RunnableBranch`       |

## 9. Practical Exercises

### Exercise 1 — Simple Chain

Create a chain that explains a Python concept using a beginner-friendly prompt.

### Exercise 2 — Sequential Chain

Generate an English summary and then translate it into Urdu.

### Exercise 3 — Parallel Chain

Generate a topic summary and three interview questions from the same input.

### Exercise 4 — Conditional Chain

Return a simple explanation for beginners and a technical explanation for advanced learners.

## 10. Important Interview Questions

**Q1. What is a chain in LangChain?**

A workflow that connects multiple processing components.

**Q2. What is LCEL?**

LangChain Expression Language, a way of composing runnable components.

**Q3. What does the pipe operator do?**

Connects compatible runnables into a workflow.

**Q4. What is RunnableSequence?**

A runnable that executes components in sequence.

**Q5. What is RunnableParallel?**

A runnable that executes independent branches concurrently where possible and combines their results.

**Q6. What is RunnableBranch?**

A runnable that executes the first branch whose condition matches, or a default branch.

**Q7. What is RunnableLambda?**

A wrapper that allows an ordinary Python function to be used in a runnable workflow.

**Q8. What is the difference between sequential and parallel chains?**

Sequential chains connect dependent tasks; parallel chains execute independent tasks.

**Q9. What is the difference between conditional chains and agents?**

Conditional chains follow predefined routing logic, whereas agents can dynamically select tools or actions using a language model.

**Q10. Does every chain require an LLM?**

No. Chains can also contain ordinary Python operations.

**Q11. What does batch() do?**

Processes multiple inputs, potentially using concurrent requests.

**Q12. What happens if a chain step fails?**

The error usually propagates unless error handling or fallback logic has been configured.

## 11. Common Beginner Mistakes

- Assuming `batch()` always means one API request.
- Assuming parallel chains use only one model request.
- Passing incompatible data types between sequential steps.
- Forgetting the default branch in `RunnableBranch`.
- Assuming all conditional branches run.
- Confusing a chain with an AI agent.
- Forgetting to handle API failures and rate limits.

## 12. Key Takeaways

- Chains are reusable processing workflows.
- LCEL connects components using the pipe operator.
- Simple chains connect basic processing steps.
- Sequential chains connect dependent tasks.
- Parallel chains run independent tasks.
- Conditional chains select workflows using conditions.
- `RunnableLambda` helps adapt Python functions for runnable composition.
- Chains are useful for predictable AI application workflows.

---

## Learning Resources

- [CampusX LangChain Chains Repository](https://github.com/campusx-official/langchain-chains)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 07 of 18
