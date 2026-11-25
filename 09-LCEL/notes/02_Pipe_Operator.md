# 02 — Pipe Operator in LangChain LCEL

## 1. What Is the Pipe Operator?

The **pipe operator (`|`)** is used in LangChain Expression Language (LCEL) to connect compatible Runnable components.

It creates a workflow in which the output of one component becomes the input of the next.

### Basic Syntax

```python
chain = runnable_1 | runnable_2 | runnable_3
```

### Execution Flow

```text
Input
  |
  v
Runnable 1
  |
  v
Runnable 2
  |
  v
Runnable 3
  |
  v
Final Output
```

**Important:** In ordinary Python, `|` also has other meanings, such as bitwise OR and dictionary union. LangChain's Runnable classes implement operator behavior that allows `|` to compose compatible processing components.

---

## 2. Why Do We Use the Pipe Operator?

Imagine creating an AI application that:

1. Cleans user input.
2. Prepares a prompt.
3. Sends the prompt to an LLM.
4. Extracts the generated text.
5. Formats the final result.

Without LCEL, we could manually execute each operation.

```python
cleaned_input = prepare_input.invoke(user_input)
formatted_prompt = prompt.invoke(cleaned_input)
response = model.invoke(formatted_prompt)
answer = parser.invoke(response)
final_result = format_output.invoke(answer)
```

With LCEL:

```python
chain = (
    prepare_input
    | prompt
    | model
    | parser
    | format_output
)

final_result = chain.invoke(user_input)
```

### Benefits

- Cleaner and more readable code
- Reusable workflows
- Less manual data passing
- Easier integration with LangChain components
- Support for batching and asynchronous execution
- Support for streaming when components allow it

---

## 3. Basic Pipe Operator Example Without an LLM

We'll start with ordinary Python functions.

```python
from langchain_core.runnables import RunnableLambda

double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)

chain = double | add_five

result = chain.invoke(10)

print(result)
```

### Output

```text
25
```

### Explanation

Input: `10`

First operation:

```text
10 × 2 = 20
```

Second operation:

```text
20 + 5 = 25
```

Final result: `25`

---

## 4. The Order of Operations Matters

Consider these two chains.

### Chain A

```python
chain_a = double | add_five

print(chain_a.invoke(10))
```

Output:

```text
25
```

### Chain B

```python
chain_b = add_five | double

print(chain_b.invoke(10))
```

Output:

```text
30
```

### Why Are They Different?

Chain A:

```text
10 → Double → 20 → Add 5 → 25
```

Chain B:

```text
10 → Add 5 → 15 → Double → 30
```

**Key Point:** Changing the order of the Runnables can change the result.

---

## 5. How the Pipe Operator Creates RunnableSequence

When we write:

```python
chain = double | add_five
```

LangChain creates a `RunnableSequence` object.

We can verify this:

```python
print(type(chain))
```

The resulting type is `RunnableSequence`.

### Explicit Alternative

```python
from langchain_core.runnables import RunnableSequence

chain = RunnableSequence(
    double,
    add_five
)
```

Both approaches create sequential workflows.

### Comparison

| Pipe Operator                | RunnableSequence                                  |
| ---------------------------- | ------------------------------------------------- |
| `double \| add_five`         | `RunnableSequence(double, add_five)`              |
| Concise syntax               | Explicit constructor                              |
| Easy to extend               | Useful for understanding the underlying component |
| Executes components in order | Executes components in order                      |

---

## 6. Connecting Three or More Runnables

The pipe operator isn't limited to two components.

Example:

```python
double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)
square = RunnableLambda(lambda x: x ** 2)

chain = double | add_five | square

print(chain.invoke(3))
```

### Output

```text
121
```

### Explanation

```text
Input: 3
   |
   v
Double: 6
   |
   v
Add Five: 11
   |
   v
Square: 121
```

The final result is `121`.

---

## 7. Using the Pipe Operator for Text Processing

LCEL also works with text.

Example:

```python
clean = RunnableLambda(lambda text: text.strip())

uppercase = RunnableLambda(lambda text: text.upper())

add_prefix = RunnableLambda(
    lambda text: "Processed: " + text
)

chain = clean | uppercase | add_prefix

result = chain.invoke("  hello langchain  ")

print(result)
```

### Output

```text
Processed: HELLO LANGCHAIN
```

### Processing Flow

```text
"  hello langchain  "
          |
          v
       strip()
          |
          v
"hello langchain"
          |
          v
       upper()
          |
          v
"HELLO LANGCHAIN"
          |
          v
     Add Prefix
          |
          v
"Processed: HELLO LANGCHAIN"
```

This example requires no LLM or external API.

---

## 8. Understanding Input and Output Compatibility

Every Runnable must receive a compatible input.

For example:

```python
double = RunnableLambda(lambda x: x * 2)

uppercase = RunnableLambda(lambda text: text.upper())
```

Now consider:

```python
chain = double | uppercase

chain.invoke(5)
```

This will fail.

### Why?

The first step returns an integer:

```python
10
```

The second step attempts:

```python
10.upper()
```

But integers do not have an `upper()` method.

### Correct Approach

Convert the integer into a string.

```python
convert_to_string = RunnableLambda(
    lambda x: str(x)
)

chain = double | convert_to_string | uppercase

result = chain.invoke(5)

print(result)
```

### Output

```text
10
```

The displayed output is `10`, but its Python type is `str`.

```python
print(type(result))
```

Output:

```text
<class 'str'>
```

### Important Lesson

**Each processing step must accept the data type produced by the previous step.**

This is one of the most important concepts in LCEL.

---

## 9. Using the Pipe Operator with Groq

Now we'll connect an actual language model.

### Step 1 — Import Libraries

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
```

### Step 2 — Initialize Groq

```python
load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
```

### Step 3 — Create a Prompt

```python
prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in three simple sentences."
)
```

### Step 4 — Create the Chain

```python
chain = prompt | model | StrOutputParser()
```

### Step 5 — Execute

```python
result = chain.invoke({
    "topic": "Machine Learning"
})

print(str(result))
```

The final result contains an explanation of machine learning.

Its wording depends on the model response.

---

## 10. Adding RunnableLambda Before the LLM

We can clean the user's input before generating a response.

### Python Function

```python
def prepare_topic(topic):
    cleaned_topic = topic.strip().title()

    return {
        "topic": cleaned_topic
    }
```

### Convert to Runnable

```python
from langchain_core.runnables import RunnableLambda

prepare_input = RunnableLambda(prepare_topic)
```

### Create the Chain

```python
chain = (
    prepare_input
    | prompt
    | model
    | StrOutputParser()
)
```

### Execute

```python
result = chain.invoke("  machine learning  ")

print(str(result))
```

### Explanation

The user provides a string.

The first Runnable converts it into:

```python
{"topic": "Machine Learning"}
```

That dictionary is compatible with the prompt's `{topic}` variable.

The prompt then sends the formatted instructions to the model.

---

## 11. Adding RunnableLambda After the LLM

We can also transform model output.

Example:

```python
def format_answer(text):
    return "AI EXPLANATION:\n\n" + str(text).strip()
```

Convert it into a Runnable:

```python
formatter = RunnableLambda(format_answer)
```

Connect:

```python
chain = (
    prepare_input
    | prompt
    | model
    | StrOutputParser()
    | formatter
)
```

### Execution Flow

```text
Raw Topic
   |
   v
Prepare Input
   |
   v
PromptTemplate
   |
   v
ChatGroq
   |
   v
StrOutputParser
   |
   v
Output Formatter
   |
   v
Final Explanation
```

This workflow combines ordinary Python processing with an AI model.

---

## 12. Passing Multiple Prompt Variables

A prompt can contain multiple variables.

Example:

```python
prompt = PromptTemplate.from_template(
    """
    Explain {topic} to a {level} student.
    Include one practical example.
    """
)
```

We must provide both variables:

```python
chain = prompt | model | StrOutputParser()

result = chain.invoke({
    "topic": "Python decorators",
    "level": "beginner"
})
```

### Important

If the prompt expects `{topic}` and `{level}`, the input must provide both values.

Otherwise, the prompt formatting step can raise an error.

---

## 13. Using batch() with a Pipe-Based Chain

LCEL workflows support common Runnable execution methods.

Example:

```python
topics = [
    {"topic": "Python"},
    {"topic": "SQL"},
    {"topic": "FastAPI"}
]

results = chain.batch(
    topics,
    config={"max_concurrency": 2}
)
```

Each input passes through the same workflow.

The result is a list containing the generated explanations.

**Important:** Multiple inputs may result in multiple Groq API requests.

---

## 14. Using stream() with the Pipe Operator

Streaming allows supported components to produce output incrementally.

Example:

```python
for chunk in chain.stream({
    "topic": "Artificial Intelligence"
}):
    print(str(chunk), end="", flush=True)
```

The output may appear progressively.

However, the streaming behavior depends on the model and the connected Runnables.

A regular `RunnableLambda` placed after the model may buffer the complete response before producing its own output.

---

## 15. Inspecting a Pipe-Based Chain

LCEL workflows can be inspected programmatically.

### Check the Type

```python
print(type(chain))
```

### Inspect the Steps

```python
print(chain.steps)
```

### Count the Steps

```python
print(len(chain.steps))
```

### Inspect the Graph

```python
graph = chain.get_graph()

print(graph.draw_ascii())
```

ASCII graph rendering may require the optional `grandalf` package.

```powershell
python -m pip install grandalf
```

### Why Is This Useful?

Graph inspection helps developers:

- Understand workflow structure.
- Debug processing pipelines.
- See connected components.
- Document complex applications.

---

## 16. Pipe Operator vs Ordinary Python Functions

A normal Python function can be called directly.

```python
def double_number(number):
    return number * 2

result = double_number(5)
```

But we cannot assume that ordinary function objects support LangChain's pipe operator directly.

For a standalone function-first composition, wrap the function:

```python
double_runnable = RunnableLambda(double_number)
```

Now:

```python
chain = double_runnable | RunnableLambda(lambda x: x + 5)
```

LangChain can also automatically coerce compatible functions when they're used in supported Runnable composition positions.

---

## 17. Pipe Operator vs RunnableParallel

The pipe operator normally connects steps sequentially.

Example:

```python
chain = runnable_1 | runnable_2
```

But LCEL also supports parallel processing using dictionaries.

Example:

```python
chain = RunnableLambda(lambda x: x + 1) | {
    "double": RunnableLambda(lambda x: x * 2),
    "square": RunnableLambda(lambda x: x ** 2)
}
```

The dictionary becomes a `RunnableParallel` stage.

For input `5`, the first step produces `6`, and both branches then receive `6`.

The result is:

```python
{
    "double": 12,
    "square": 36
}
```

We will study dictionary composition in Topic 03.

---

## 18. Common Beginner Mistakes

**Mistake 1 — Assuming the pipe operator works with every Python object**

It depends on supported operator implementations and Runnable coercion.

**Mistake 2 — Connecting incompatible data types**

The next Runnable must accept the previous output.

**Mistake 3 — Forgetting required prompt variables**

Provide every required variable when invoking a PromptTemplate chain.

**Mistake 4 — Assuming the order of operations doesn't matter**

Different orders can produce different results.

**Mistake 5 — Thinking pipe composition requires an LLM**

It can also connect ordinary Python functions.

**Mistake 6 — Assuming batch() makes one API request**

Batching may execute multiple requests.

**Mistake 7 — Assuming all components stream incrementally**

Some components process complete inputs before returning output.

---

## 19. Interview Questions

**Q1. What is the pipe operator in LangChain?**

It connects compatible Runnable components into a workflow.

**Q2. What does `prompt | model | parser` mean?**

It prepares a prompt, generates a model response, and parses the result.

**Q3. What is created when two Runnables are connected with `|`?**

Typically a RunnableSequence.

**Q4. Does the execution order matter?**

Yes.

**Q5. Can we connect more than two Runnables?**

Yes.

**Q6. Does LCEL require an LLM?**

No.

**Q7. Why is input/output compatibility important?**

Each step must be able to process the preceding step's output.

**Q8. Can RunnableLambda be placed before a model?**

Yes, to prepare or transform the input.

**Q9. Can RunnableLambda be placed after a model?**

Yes, to process the model output.

**Q10. What is the difference between RunnableSequence and RunnableParallel?**

RunnableSequence executes connected steps sequentially. RunnableParallel processes independent branches.

**Q11. Does a pipe-based chain support batch()?**

Yes.

**Q12. How can we inspect an LCEL workflow?**

Using properties and methods such as `steps` and `get_graph()`.

---

## 20. Key Takeaways

- The pipe operator (`|`) is the main LCEL composition syntax.
- It connects compatible Runnable components.
- Pipe-based sequential composition creates RunnableSequence.
- Execution order matters.
- Each step receives the preceding step's output.
- Input and output types must be compatible.
- RunnableLambda can transform data before and after model execution.
- LCEL supports prompts, models, parsers, and Python functions.
- Composed workflows support common Runnable execution methods.
- More advanced LCEL workflows can combine sequential and parallel processing.

---

## Learning Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [RunnableSequence Reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSequence)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 09 — Topic 02
