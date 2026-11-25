# 05 — LangChain Prompts: Quick Revision

## 1. Core Concepts

| Concept             | Explanation                                             |
| ------------------- | ------------------------------------------------------- |
| Prompt              | Instructions or input sent to a language model          |
| Static Prompt       | A prompt with fixed text                                |
| Dynamic Prompt      | A prompt containing variables                           |
| Prompt Engineering  | Designing and improving prompts                         |
| PromptTemplate      | Creates reusable text-based prompts                     |
| ChatPromptTemplate  | Creates reusable role-based chat prompts                |
| MessagesPlaceholder | Inserts previous messages into a chat prompt            |
| Prompt Variable     | A placeholder such as `{topic}`                         |
| Partial Variables   | Variables filled in before final formatting             |
| LCEL                | LangChain Expression Language for connecting components |

## 2. Important Comparisons

### PromptTemplate vs ChatPromptTemplate

| PromptTemplate                                 | ChatPromptTemplate                           |
| ---------------------------------------------- | -------------------------------------------- |
| Formats text prompts                           | Formats structured chat messages             |
| Returns a StringPromptValue through `invoke()` | Returns a ChatPromptValue through `invoke()` |
| Suitable for reusable text instructions        | Suitable for role-based conversations        |

### PromptTemplate vs MessagesPlaceholder

| PromptTemplate                    | MessagesPlaceholder             |
| --------------------------------- | ------------------------------- |
| Inserts variable values into text | Inserts a list of chat messages |
| Useful for dynamic instructions   | Useful for conversation history |
| Does not store messages           | Does not store messages         |

## 3. Important Methods

| Method                               | Purpose                                    |
| ------------------------------------ | ------------------------------------------ |
| `PromptTemplate.from_template()`     | Creates a text prompt template             |
| `ChatPromptTemplate.from_messages()` | Creates a chat prompt template             |
| `prompt.invoke()`                    | Formats a prompt using inputs              |
| `prompt.format()`                    | Returns a formatted string                 |
| `prompt.partial()`                   | Pre-fills prompt variables                 |
| `to_messages()`                      | Converts a chat prompt value into messages |
| `model.invoke()`                     | Calls the language model                   |
| `chain.invoke()`                     | Runs a connected workflow                  |

## 4. Code Examples

### Dynamic Prompt

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} to a {level} student."
)

result = prompt.format(
    topic="Python",
    level="beginner"
)

print(result)
```

### ChatPromptTemplate

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Python teacher."),
    ("human", "Explain {topic}.")
])

formatted = prompt.invoke({"topic": "Decorators"})

print(formatted.to_messages())
```

### MessagesPlaceholder

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])
```

The final example defines a prompt; the application must still supply the conversation history and call a model.

## 5. Interview Questions

**Q1. What is prompt engineering?**

Designing and improving prompts to guide language model responses.

**Q2. What is the difference between static and dynamic prompts?**

Static prompts contain fixed instructions, while dynamic prompts use replaceable variables.

**Q3. What does PromptTemplate do?**

It creates reusable text-based prompts.

**Q4. What does ChatPromptTemplate do?**

It creates structured chat prompts containing different message roles.

**Q5. Does prompt.invoke() call the LLM?**

No. It formats the prompt.

**Q6. What is MessagesPlaceholder?**

A LangChain component that inserts previous chat messages into a prompt.

**Q7. Does MessagesPlaceholder store memory automatically?**

No. The application must maintain the conversation history.

**Q8. What is partial()?**

A method used to pre-fill some prompt variables.

**Q9. What does the pipe operator (`|`) do?**

Connects compatible LangChain components into a workflow.

**Q10. Why is conversation history useful?**

It allows the model to use information from earlier interactions.

## 6. Practical Test Results

### PromptTemplate

Successfully generated a beginner-friendly explanation of Python decorators using:

```python
chain = prompt | model | StrOutputParser()
```

### ChatPromptTemplate

Successfully used structured system and human messages to generate an explanation of Python decorators.

### MessagesPlaceholder

Test conversation:

```text
You: My name is Ateeb.
You: I am learning LangChain.
You: What is my name and what am I learning?

AI: Your name is Ateeb, and you're currently learning LangChain.
```

**Result:** The chatbot successfully used previous conversation history.

## 7. Key Takeaways

- Prompts provide instructions to language models.
- Prompt templates make instructions reusable.
- `PromptTemplate` works with text-based prompts.
- `ChatPromptTemplate` supports structured message roles.
- `MessagesPlaceholder` inserts existing conversation history.
- Prompt templates do not automatically remember conversations.
- LCEL allows prompts, models, and output parsers to work together.

---

## Learning Resources

- [CampusX LangChain Prompts](https://github.com/campusx-official/langchain-prompts)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 04 of 18
