# 05 — Advanced LCEL in LangChain

## 1. What Is Advanced LCEL?

Advanced LangChain Expression Language (LCEL) means combining different Runnable components into larger, reusable workflows.

So far, we have learned how to:

- Connect components using `|`.
- Run independent operations using dictionaries.
- Clean and validate inputs.
- Preserve information using `RunnablePassthrough`.
- Transform values using `RunnableLambda`.

Now we will combine these concepts into a complete workflow.

## 2. Our Example Application

We will build an AI Programming Tutor.

The application will:

1. Receive a programming topic and learning level.
2. Clean and validate the input.
3. Select an explanation based on the learning level.
4. Generate three interview questions independently.
5. Preserve the topic and level.
6. Add a display label and explanation length.
7. Return a dictionary.

### Execution Flow

```text
                  User Input
                      |
                      v
               Normalize Input
                      |
                      v
               Validate Input
                      |
                      v
          RunnablePassthrough.assign()
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
     RunnableBranch  Questions   Display Label
          |           Chain       Function
     +----+----+       |
     |         |       |
  Beginner  Advanced   |
   Prompt    Prompt    |
     |         |       |
     +----+----+       |
          |            |
        Groq          Groq
          |            |
        Parser       Parser
          |            |
          +------+-----+
                 |
                 v
          Combined Dictionary
                 |
                 v
          Add Explanation Length
                 |
                 v
             Final Result
```

## 3. Important Components

| Component                      | Responsibility                             |
| ------------------------------ | ------------------------------------------ |
| `RunnableLambda`               | Clean, validate, and transform data        |
| `RunnableSequence`             | Execute connected stages                   |
| `RunnableParallel`             | Run independent processing branches        |
| `RunnableBranch`               | Select a workflow using conditions         |
| `RunnablePassthrough.assign()` | Preserve dictionary fields and add results |
| `PromptTemplate`               | Generate reusable model instructions       |
| `ChatGroq`                     | Generate AI responses                      |
| `StrOutputParser`              | Extract generated text                     |

## 4. Combining Sequential Operations

We can connect several dependent Runnables using the pipe operator.

```python
from langchain_core.runnables import RunnableLambda

clean = RunnableLambda(lambda text: text.strip())
uppercase = RunnableLambda(lambda text: text.upper())

chain = clean | uppercase

print(chain.invoke("  hello  "))
```

Output:

```text
HELLO
```

This creates a `RunnableSequence`.

Each step receives the output of the previous step.

## 5. Combining Parallel Operations

We can use `RunnableParallel` to execute independent operations.

```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    uppercase=RunnableLambda(lambda x: x.upper()),
    lowercase=RunnableLambda(lambda x: x.lower()),
    length=RunnableLambda(lambda x: len(x))
)

print(parallel.invoke("Python"))
```

Output:

```python
{
    "uppercase": "PYTHON",
    "lowercase": "python",
    "length": 6
}
```

All branches receive the same input.

## 6. Understanding RunnableBranch

`RunnableBranch` routes input to different processing workflows.

It checks conditions in order and executes the first matching branch.

Example:

```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (
        lambda data: data["level"] == "beginner",
        RunnableLambda(lambda data: "Simple explanation")
    ),
    (
        lambda data: data["level"] == "advanced",
        RunnableLambda(lambda data: "Technical explanation")
    ),
    RunnableLambda(lambda data: "General explanation")
)
```

Test:

```python
print(branch.invoke({"level": "beginner"}))
```

Output:

```text
Simple explanation
```

Only one selected branch executes.

## 7. Combining RunnableBranch with Groq

We can select different prompts based on a student's level.

### Beginner Prompt

```python
beginner_prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in three simple sentences."
)
```

### Advanced Prompt

```python
advanced_prompt = PromptTemplate.from_template(
    "Explain {topic} to an advanced CS student. "
    "Include technical terminology and one example."
)
```

### Create the Chains

```python
beginner_chain = beginner_prompt | model | StrOutputParser()
advanced_chain = advanced_prompt | model | StrOutputParser()
```

### Create the Branch

```python
explanation_branch = RunnableBranch(
    (
        lambda data: data["level"] == "beginner",
        beginner_chain
    ),
    advanced_chain
)
```

For this example, the advanced chain is the default.

The branch receives the input dictionary and selects the appropriate model prompt.

## 8. Combining Conditional and Parallel Processing

Now suppose we want two independent outputs:

- A level-appropriate explanation.
- Three interview questions.

We can write:

```python
questions_prompt = PromptTemplate.from_template(
    "Generate exactly three interview questions about {topic}."
)

questions_chain = (
    questions_prompt
    | model
    | StrOutputParser()
)
```

Then:

```python
parallel_chain = RunnableParallel(
    explanation=explanation_branch,
    questions=questions_chain
)
```

Here, the explanation branch selects a prompt, while the questions branch independently generates questions.

The parallel stage returns a dictionary.

## 9. Preserving Original Input with assign()

`RunnableParallel` returns the outputs defined by its branches.

If we also want to keep the original topic and level, use `RunnablePassthrough.assign()`.

```python
combined_chain = RunnablePassthrough.assign(
    explanation=explanation_branch,
    questions=questions_chain
)
```

Input:

```python
{
    "topic": "Machine Learning",
    "level": "beginner"
}
```

Output structure:

```python
{
    "topic": "Machine Learning",
    "level": "beginner",
    "explanation": "...",
    "questions": "..."
}
```

This is a common pattern in larger LangChain workflows.

## 10. Adding a Postprocessing Stage

After generating the explanation, we may want to calculate its length.

```python
add_length = RunnablePassthrough.assign(
    explanation_length=lambda data: len(
        str(data["explanation"])
    )
)
```

We connect it to the preceding stage:

```python
chain = combined_chain | add_length
```

The second stage receives the complete dictionary produced by the first stage.

**Important:** Fields computed in the same `assign()` operation are calculated from the input to that stage. Use another `assign()` stage when one new field depends on another newly generated field.

## 11. Input Validation

Before making model requests, validate input.

```python
def normalize_input(data):
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary")

    topic = data.get("topic")
    level = data.get("level", "beginner")

    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("Topic cannot be empty")

    if not isinstance(level, str):
        raise TypeError("Level must be a string")

    level = level.strip().lower()

    if level not in {"beginner", "advanced"}:
        raise ValueError("Level must be beginner or advanced")

    return {
        "topic": topic.strip(),
        "level": level
    }
```

Wrap the function:

```python
normalize = RunnableLambda(normalize_input)
```

Validation can prevent invalid inputs from reaching the LLM.

## 12. Building the Complete LCEL Workflow

Now we can combine everything:

```python
study_chain = (
    normalize
    | RunnablePassthrough.assign(
        display_label=lambda data: (
            f"{data['topic']} ({data['level']})"
        ),
        explanation=explanation_branch,
        questions=questions_chain
    )
    | RunnablePassthrough.assign(
        explanation_length=lambda data: len(
            str(data["explanation"])
        )
    )
)
```

This workflow includes:

- Sequential composition
- Input validation
- Conditional routing
- Parallel generation
- Dictionary enrichment
- Postprocessing

### Invoke the Workflow

```python
result = study_chain.invoke({
    "topic": "Python decorators",
    "level": "beginner"
})
```

The final result is a dictionary containing the normalized input and generated outputs.

## 13. Understanding Fallbacks

LangChain Runnables support fallback behavior through `with_fallbacks()`.

A fallback is an alternative Runnable that is attempted when the primary Runnable raises an exception.

Example:

```python
def primary_function(number):
    raise ValueError("Primary operation failed")

primary = RunnableLambda(primary_function)

fallback = RunnableLambda(
    lambda number: number * 2
)

safe_chain = primary.with_fallbacks([fallback])

print(safe_chain.invoke(5))
```

Output:

```text
10
```

The first operation raises an error, so LangChain attempts the fallback.

### Important

Fallbacks do not automatically guarantee correctness or successful execution.

The fallback must accept a compatible input and produce an appropriate output.

## 14. Understanding Retries

Some Runnable components support retry policies.

Example:

```python
reliable_chain = chain.with_retry(
    stop_after_attempt=3
)
```

This allows the operation to be retried after certain exceptions.

Retries can be useful for temporary network failures.

However, they should be used carefully:

- Additional attempts may increase API usage.
- Invalid input usually should not be retried.
- Provider rate limits must be respected.
- Retries cannot guarantee success.

For learning purposes, we will demonstrate a deterministic local fallback instead of intentionally triggering Groq failures.

## 15. Inspecting Advanced LCEL Chains

For debugging, we can inspect the workflow.

```python
print(type(study_chain))
```

We can also inspect its graph:

```python
graph = study_chain.get_graph()

print(graph.draw_ascii())
```

ASCII rendering may require the optional `grandalf` dependency.

```powershell
python -m pip install grandalf
```

Graph inspection is particularly useful when the workflow contains nested branches and transformations.

## 16. Error Handling

A production application should handle errors appropriately.

Example:

```python
try:
    result = study_chain.invoke({
        "topic": "Python",
        "level": "beginner"
    })

    print(result)

except ValueError as error:
    print("Validation error:", error)

except Exception as error:
    print("Workflow failed:", error)
```

This separates expected validation failures from unexpected processing failures.

## 17. Advanced LCEL vs AI Agents

An advanced LCEL workflow can contain many processing stages.

However, it still generally follows developer-defined execution logic.

| Advanced LCEL                         | AI Agent                            |
| ------------------------------------- | ----------------------------------- |
| Uses predefined composition           | Can select actions dynamically      |
| Often follows known workflow paths    | May decide which tools to use       |
| Uses conditions defined by developers | Can use model-driven tool selection |
| Good for predictable applications     | Good for adaptive, tool-using tasks |

A conditional LCEL chain is not automatically an AI agent.

## 18. Real-World Applications

### AI Learning Assistant

Generate explanations and interview questions according to student level.

### Customer Support Automation

Classify customer input and route it to different response workflows.

### Document Processing

Generate summaries, extract keywords, and prepare structured results.

### RAG Applications

Combine retrieved context with questions and generate grounded answers.

### Software Development Tools

Process code, generate explanations, and format review results.

## 19. Common Beginner Mistakes

**Mistake 1 — Confusing sequence and parallel processing**

Sequential steps depend on earlier outputs, while parallel branches operate independently.

**Mistake 2 — Assuming RunnableBranch executes every branch**

Only the first matching branch executes.

**Mistake 3 — Forgetting validation**

Invalid data can cause errors during prompt formatting or model execution.

**Mistake 4 — Losing original dictionary fields**

Use `RunnablePassthrough.assign()` when existing fields must be preserved.

**Mistake 5 — Assuming fallback means automatic success**

A fallback can fail too.

**Mistake 6 — Assuming retries do not consume resources**

Retries can cause additional model calls.

**Mistake 7 — Building overly complex workflows without testing components**

Test individual stages before composing them into larger pipelines.

## 20. Interview Questions

**Q1. What is advanced LCEL composition?**

Combining different Runnable components into larger workflows.

**Q2. What does RunnableBranch do?**

Selects the first branch whose condition matches, otherwise running a default.

**Q3. How do we combine conditional and parallel processing?**

Place a RunnableBranch inside a RunnableParallel or an `assign()` stage alongside other independent branches.

**Q4. What does RunnablePassthrough.assign() do?**

Preserves existing dictionary fields and adds calculated values.

**Q5. What is the purpose of with_fallbacks()?**

To attempt alternative Runnables after an exception.

**Q6. What is the purpose of with_retry()?**

To retry a Runnable according to a configured policy.

**Q7. Why should we validate inputs before LLM requests?**

To reject invalid data and avoid unnecessary processing.

**Q8. Can advanced LCEL workflows use ordinary Python functions?**

Yes, using RunnableLambda.

**Q9. Can an LCEL workflow return a dictionary?**

Yes.

**Q10. Is an advanced LCEL workflow automatically an agent?**

No.

## 21. Key Takeaways

- Advanced LCEL combines different Runnable types.
- RunnableSequence connects dependent processing stages.
- RunnableParallel runs independent operations.
- RunnableBranch selects a workflow conditionally.
- RunnablePassthrough.assign() preserves and enriches dictionaries.
- RunnableLambda adds custom Python processing.
- Validation should happen before expensive LLM operations.
- with_fallbacks() provides alternative execution paths after failures.
- with_retry() can help handle certain temporary failures.
- Complex LCEL workflows should be tested incrementally.

---

## Learning Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [LangChain Runnable Reference](https://reference.langchain.com/python/langchain-core/runnables/)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 09 — Topic 05
