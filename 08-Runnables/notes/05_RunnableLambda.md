# 05 — RunnableLambda in LangChain

## 1. What Is RunnableLambda?

`RunnableLambda` is a LangChain component that wraps an ordinary Python function and makes it compatible with the Runnable interface.

In simple words:

**Python Function → RunnableLambda → LangChain Runnable**

A normal Python function can be called directly, but wrapping it in `RunnableLambda` lets us use LangChain's execution methods and combine the function with other Runnables.

### Basic Example

```python
from langchain_core.runnables import RunnableLambda

double = RunnableLambda(lambda x: x * 2)

result = double.invoke(5)

print(result)
```

Expected output:

```text
10
```

## 2. Why Do We Need RunnableLambda?

Real-world AI applications often need additional Python processing before or after a language model.

For example, an application may need to:

- Remove extra spaces from user input.
- Convert text to lowercase or uppercase.
- Extract specific values from a dictionary.
- Validate user input.
- Format data for a prompt.
- Clean a model-generated response.
- Combine or transform retrieved information.

`RunnableLambda` allows us to add these operations to LangChain workflows.

## 3. Importing RunnableLambda

```python
from langchain_core.runnables import RunnableLambda
```

It is available through `langchain-core`.

## 4. Normal Python Function vs RunnableLambda

Consider a normal Python function:

```python
def square(number):
    return number ** 2

print(square(5))
```

Output:

```text
25
```

Now wrap it:

```python
square_runnable = RunnableLambda(square)

print(square_runnable.invoke(5))
```

Output:

```text
25
```

### Comparison

| Normal Python Function             | RunnableLambda                       |
| ---------------------------------- | ------------------------------------ |
| Called with `function(input)`      | Called with `runnable.invoke(input)` |
| Can use Python directly            | Supports LangChain Runnable methods  |
| Can be composed manually           | Supports LCEL composition            |
| No built-in Runnable interface     | Provides Runnable interface          |
| Useful in ordinary Python programs | Useful within LangChain workflows    |

Both are valid approaches. Use RunnableLambda when integrating functions into Runnable-based workflows.

## 5. Using Lambda Functions

A lambda is a short anonymous Python function.

Example:

```python
multiply = lambda x: x * 3

print(multiply(4))
```

Output:

```text
12
```

We can wrap it directly:

```python
multiply_runnable = RunnableLambda(
    lambda x: x * 3
)

print(multiply_runnable.invoke(4))
```

Output:

```text
12
```

## 6. Using Regular Functions

We are not limited to anonymous functions.

```python
def clean_text(text):
    return text.strip().lower()

clean_runnable = RunnableLambda(clean_text)

result = clean_runnable.invoke(
    "  HELLO LANGCHAIN  "
)

print(result)
```

Output:

```text
hello langchain
```

Regular functions are preferable when the logic is complex or needs to be reused.

## 7. Connecting Multiple RunnableLambda Components

Suppose we want to perform two tasks:

1. Remove unnecessary spaces.
2. Convert the text to uppercase.

```python
clean = RunnableLambda(
    lambda text: text.strip()
)

uppercase = RunnableLambda(
    lambda text: text.upper()
)

chain = clean | uppercase

print(chain.invoke("  hello langchain  "))
```

Output:

```text
HELLO LANGCHAIN
```

### Execution Flow

```text
Input: "  hello langchain  "
             |
             v
       Remove Spaces
             |
             v
      "hello langchain"
             |
             v
       Convert Uppercase
             |
             v
      "HELLO LANGCHAIN"
```

The pipe operator creates a sequential workflow.

## 8. Transforming Dictionaries

RunnableLambda can process dictionaries.

Example:

```python
def format_user(data):
    return {
        "full_name": data["first_name"] + " " + data["last_name"],
        "age": data["age"]
    }

formatter = RunnableLambda(format_user)

result = formatter.invoke({
    "first_name": "Ali",
    "last_name": "Khan",
    "age": 22
})

print(result)
```

Expected output:

```python
{
    "full_name": "Ali Khan",
    "age": 22
}
```

This is useful for preparing structured application data.

## 9. RunnableLambda with RunnableSequence

We can create a sequence of mathematical operations.

```python
from langchain_core.runnables import RunnableSequence

double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)

sequence = RunnableSequence(
    double,
    add_five
)

print(sequence.invoke(10))
```

Output:

```text
25
```

The same workflow can be written as:

```python
sequence = double | add_five
```

## 10. RunnableLambda with RunnableParallel

RunnableLambda can also be used inside independent parallel branches.

```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2),
    cube=RunnableLambda(lambda x: x ** 3)
)

print(parallel.invoke(3))
```

Expected output:

```python
{
    "double": 6,
    "square": 9,
    "cube": 27
}
```

Each branch receives the same input.

## 11. RunnableLambda with batch()

The `batch()` method processes multiple inputs.

```python
square = RunnableLambda(lambda x: x ** 2)

results = square.batch([2, 3, 4, 5])

print(results)
```

Expected output:

```text
[4, 9, 16, 25]
```

The default batch implementation may use concurrent execution, depending on the Runnable and execution configuration.

## 12. RunnableLambda with ainvoke()

We can execute a Runnable asynchronously.

```python
import asyncio

double = RunnableLambda(lambda x: x * 2)

async def main():
    result = await double.ainvoke(10)
    print(result)

asyncio.run(main())
```

Output:

```text
20
```

RunnableLambda can also wrap supported asynchronous functions.

However, asynchronous execution does not automatically make CPU-intensive operations faster.

## 13. RunnableLambda with Groq

Now we'll use a Python function to clean user input before sending it to Groq.

### Initialize the Model

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
```

### Create a Cleaning Function

```python
def clean_topic(topic):
    return {
        "topic": topic.strip().title()
    }

clean_runnable = RunnableLambda(clean_topic)
```

This converts a string such as:

```text
"  machine learning  "
```

into:

```python
{"topic": "Machine Learning"}
```

### Create the Prompt

```python
prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in three simple sentences."
)
```

### Connect Everything

```python
chain = (
    clean_runnable
    | prompt
    | model
    | StrOutputParser()
)

result = chain.invoke("  machine learning  ")

print(str(result))
```

### Execution Flow

```text
Raw Input
    |
    v
RunnableLambda
    |
    v
Cleaned Topic Dictionary
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
Final Explanation
```

The Python function prepares the input before the LLM receives it.

## 14. Postprocessing Model Output

We can also place RunnableLambda after an output parser.

Example:

```python
def add_heading(text):
    return "AI Explanation:\n\n" + str(text).strip()

format_output = RunnableLambda(add_heading)

chain = (
    prompt
    | model
    | StrOutputParser()
    | format_output
)
```

Here, the model generates a response, and a Python function adds a heading.

The final text comes from both the LLM and ordinary Python processing.

## 15. RunnableLambda vs RunnablePassthrough

| Feature              | RunnableLambda            | RunnablePassthrough        |
| -------------------- | ------------------------- | -------------------------- |
| Main purpose         | Execute a Python function | Preserve input             |
| Changes input        | Depending on function     | Not by default             |
| Supports invoke()    | Yes                       | Yes                        |
| Supports batch()     | Yes                       | Yes                        |
| Typical use          | Text cleaning, formatting | Preserve original question |
| Can work without LLM | Yes                       | Yes                        |

### Example

RunnableLambda:

```python
RunnableLambda(lambda x: x * 2).invoke(5)
```

Output: `10`

RunnablePassthrough:

```python
RunnablePassthrough().invoke(5)
```

Output: `5`

## 16. RunnableLambda and Streaming

`RunnableLambda` supports the Runnable interface, including `stream()`.

However, this does not mean a normal Python function generates multiple incremental chunks.

For example:

```python
double = RunnableLambda(lambda x: x * 2)

for chunk in double.stream(5):
    print(chunk)
```

This typically produces a single output:

```text
10
```

When a Python function must transform each incoming streaming chunk incrementally, `RunnableGenerator` is often more appropriate.

This distinction becomes important when building streaming chat applications.

## 17. Error Handling

RunnableLambda executes ordinary Python functions, so those functions may raise exceptions.

Example:

```python
def divide_by_two(number):
    if not isinstance(number, (int, float)):
        raise TypeError("Input must be a number")

    return number / 2

runnable = RunnableLambda(divide_by_two)

try:
    print(runnable.invoke("hello"))
except TypeError as error:
    print("Error:", error)
```

Expected output:

```text
Error: Input must be a number
```

Good validation and error handling help make workflows reliable.

## 18. Common Beginner Mistakes

**Mistake 1 — Thinking RunnableLambda requires an LLM**

It can run ordinary Python functions without any AI model.

**Mistake 2 — Assuming all functions work with every input**

Functions must receive compatible data types.

**Mistake 3 — Forgetting dictionary formatting**

If the next prompt expects `{topic}`, a function may need to return a dictionary containing `topic`.

**Mistake 4 — Assuming a normal Python function streams tokens**

Most ordinary functions return one complete result.

**Mistake 5 — Using complicated lambda expressions**

Use named Python functions when the logic becomes difficult to read.

**Mistake 6 — Ignoring errors**

Exceptions raised inside a function can cause the overall chain to fail.

## 19. Interview Questions

**Q1. What is RunnableLambda?**

A LangChain component that wraps a Python function as a Runnable.

**Q2. Why use RunnableLambda?**

To integrate custom Python processing into LangChain workflows.

**Q3. Can RunnableLambda use regular Python functions?**

Yes.

**Q4. Can it use lambda expressions?**

Yes.

**Q5. Does RunnableLambda require an LLM?**

No.

**Q6. Can RunnableLambda connect to other Runnables?**

Yes, using LCEL or Runnable composition.

**Q7. Does RunnableLambda support invoke()?**

Yes.

**Q8. Does it support batch()?**

Yes.

**Q9. Can it transform dictionaries?**

Yes.

**Q10. What is the difference between RunnableLambda and RunnablePassthrough?**

RunnableLambda executes custom logic, whereas RunnablePassthrough forwards input unchanged by default.

**Q11. Can RunnableLambda clean user input before an LLM call?**

Yes.

**Q12. Does RunnableLambda automatically support token-by-token streaming?**

No. Ordinary functions generally process their inputs as complete values.

## 20. Key Takeaways

- `RunnableLambda` converts Python functions into Runnables.
- It supports regular and lambda functions.
- It can clean, format, validate, and transform data.
- It integrates with RunnableSequence and RunnableParallel.
- It can process dictionaries.
- It can be used before or after an LLM.
- It supports synchronous and asynchronous execution methods.
- Normal functions do not automatically provide incremental streaming.
- It is useful for creating custom LangChain workflows.

---

## Learning Resources

- [LangChain RunnableLambda Reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableLambda)
- [LangChain Documentation](https://docs.langchain.com/)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 08 — Topic 05
