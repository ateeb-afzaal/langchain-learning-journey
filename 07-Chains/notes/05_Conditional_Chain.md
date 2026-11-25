# 05 — Conditional Chains in LangChain

## 1. What Is a Conditional Chain?

A conditional chain is a workflow that selects different processing steps based on a condition.

Instead of always executing the same sequence, the application chooses which branch to run.

LangChain provides `RunnableBranch` for this purpose.

### Example

An educational assistant receives:

- Topic: Python decorators
- Student level: beginner

The application selects a beginner-friendly explanation.

If the student level is advanced, it selects a more technical explanation.

## 2. Why Do We Need Conditional Chains?

Some tasks require different processing logic depending on the input.

Examples include:

- Beginner vs advanced explanations
- Customer support ticket routing
- Different response languages
- Document processing based on file type
- Different workflows based on priority

Conditional chains allow us to organize this logic in reusable LangChain workflows.

## 3. What Is RunnableBranch?

`RunnableBranch` is a LangChain component that selects a runnable based on conditions.

It evaluates conditions in order and executes the first matching branch.

If no condition matches, it executes a default branch.

### Basic Syntax

```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (condition_1, chain_1),
    (condition_2, chain_2),
    default_chain
)
```

### Explanation

- `condition_1` checks the first rule.
- `chain_1` runs if that rule is true.
- `condition_2` checks the next rule if needed.
- `default_chain` runs when no condition matches.

Only one branch is selected for each invocation.

## 4. Creating a Beginner Chain

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

beginner_prompt = PromptTemplate.from_template(
    "Explain {topic} to a complete beginner. "
    "Use simple English and one everyday example."
)

beginner_chain = (
    beginner_prompt
    | model
    | StrOutputParser()
)
```

This branch generates a simple explanation.

## 5. Creating an Advanced Chain

```python
advanced_prompt = PromptTemplate.from_template(
    "Explain {topic} to an advanced computer science student. "
    "Include technical details and one practical example."
)

advanced_chain = (
    advanced_prompt
    | model
    | StrOutputParser()
)
```

This branch generates a more technical explanation.

## 6. Creating a Default Chain

```python
default_prompt = PromptTemplate.from_template(
    "Explain {topic} clearly for a general audience."
)

default_chain = (
    default_prompt
    | model
    | StrOutputParser()
)
```

The default branch handles inputs that do not match the defined conditions.

## 7. Connecting the Branches

```python
from langchain_core.runnables import RunnableBranch

conditional_chain = RunnableBranch(
    (
        lambda x: x["level"].lower() == "beginner",
        beginner_chain
    ),
    (
        lambda x: x["level"].lower() == "advanced",
        advanced_chain
    ),
    default_chain
)
```

### How It Works

1. The application receives an input dictionary.
2. The first condition checks whether the level is `beginner`.
3. If it matches, the beginner chain runs.
4. Otherwise, the next condition checks for `advanced`.
5. If neither condition matches, the default chain runs.

## 8. Executing the Conditional Chain

### Beginner Input

```python
result = conditional_chain.invoke({
    "topic": "Neural Networks",
    "level": "beginner"
})

print(result)
```

### Advanced Input

```python
result = conditional_chain.invoke({
    "topic": "Neural Networks",
    "level": "advanced"
})

print(result)
```

Both inputs use the same `RunnableBranch`, but different prompts are selected.

## 9. Understanding the Execution Flow

```text
                 User Input
                     |
                     v
               RunnableBranch
                     |
              Check "level"
                     |
         +-----------+-----------+
         |           |           |
         v           v           v
      Beginner    Advanced     Default
         |           |           |
         v           v           v
    Simple Prompt  Technical   General
                     Prompt     Prompt
         |           |           |
         +-----------+-----------+
                     |
                     v
                 ChatGroq
                     |
                     v
                Final Answer
```

Only the selected branch is executed.

## 10. What Is the Difference Between Conditional and Parallel Chains?

| Conditional Chain                | Parallel Chain                         |
| -------------------------------- | -------------------------------------- |
| Selects one matching branch      | Executes multiple branches             |
| Uses conditions to route inputs  | Sends input to independent workflows   |
| Useful for different user types  | Useful for generating multiple outputs |
| Common component: RunnableBranch | Common component: RunnableParallel     |

## 11. Conditional Chains vs Agents

A conditional chain follows rules defined by the developer.

For example:

```python
lambda x: x["level"] == "beginner"
```

An AI agent can use a language model to decide which tool or action to select.

The important distinction is that `RunnableBranch` itself does not require AI decision-making.

## 12. Using Python Functions for Conditions

Conditions can be written using ordinary Python functions.

```python
def is_beginner(data):
    return data["level"].lower() == "beginner"
```

Then:

```python
conditional_chain = RunnableBranch(
    (is_beginner, beginner_chain),
    default_chain
)
```

This can improve readability when conditions become complex.

## 13. Common Beginner Mistakes

**Mistake 1 — Forgetting the default branch**

`RunnableBranch` requires a fallback runnable.

**Mistake 2 — Assuming all branches run**

Only the first matching branch executes.

**Mistake 3 — Writing conditions with incompatible input formats**

Conditions must understand the data passed to the branch.

**Mistake 4 — Using fragile dictionary lookups**

For user-provided data, `x.get("level", "")` can be safer than `x["level"]` when the key might be missing.

**Mistake 5 — Confusing branching with AI agents**

Conditional branching follows developer-defined logic unless an AI model is explicitly included in the routing process.

## 14. Interview Questions

**Q1. What is a conditional chain?**

A workflow that selects processing steps based on conditions.

**Q2. What is RunnableBranch?**

A LangChain component that routes input to a matching runnable branch.

**Q3. How are conditions evaluated?**

In order, until a condition returns true.

**Q4. What happens if no condition matches?**

The default branch executes.

**Q5. Does RunnableBranch execute all branches?**

No.

**Q6. Can RunnableBranch use ordinary Python functions?**

Yes.

**Q7. What is the difference between RunnableBranch and RunnableParallel?**

RunnableBranch selects one branch, while RunnableParallel runs multiple branches.

**Q8. Does RunnableBranch require an LLM?**

No. Conditions and branches can use ordinary Python processing.

## 15. Key Takeaways

- Conditional chains route inputs to different workflows.
- `RunnableBranch` executes the first matching branch.
- A default runnable handles unmatched inputs.
- Conditions can be Python functions or lambdas.
- Only the selected branch executes.
- Conditional chains are useful for routing, personalization, and workflow selection.
- They differ from parallel chains and AI agents.

---

## Learning Resources

- [CampusX LangChain Chains Repository](https://github.com/campusx-official/langchain-chains)
- [LangChain Documentation](https://docs.langchain.com/)
- [LangChain RunnableBranch Reference](https://reference.langchain.com/python/langchain-core/runnables/branch/RunnableBranch)

**Learning Journey:** Section 07 — Topic 05
