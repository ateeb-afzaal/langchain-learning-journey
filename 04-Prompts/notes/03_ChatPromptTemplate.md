# 03 — ChatPromptTemplate in LangChain

## 1. What Is ChatPromptTemplate?

`ChatPromptTemplate` is a LangChain class used to create reusable prompts containing structured chat messages.

Unlike `PromptTemplate`, which primarily formats a text prompt, `ChatPromptTemplate` can organize messages into different roles.

The most common roles are:

- **System:** Instructions for the assistant.
- **Human:** The user's question or request.
- **AI:** Previous responses from the assistant.

## 2. PromptTemplate vs ChatPromptTemplate

| PromptTemplate                                 | ChatPromptTemplate                           |
| ---------------------------------------------- | -------------------------------------------- |
| Creates text-based prompts                     | Creates structured chat prompts              |
| Uses text placeholders                         | Supports messages with roles                 |
| Useful for general text generation             | Useful for conversational applications       |
| Returns a StringPromptValue through `invoke()` | Returns a ChatPromptValue through `invoke()` |

## 3. Creating a ChatPromptTemplate

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Python teacher."),
    ("human", "Explain {topic} in simple words.")
])

result = prompt.invoke({
    "topic": "Python decorators"
})

print(result.to_messages())
```

### Explanation

- `from_messages()` creates the chat prompt template.
- `("system", "...")` defines system instructions.
- `("human", "...")` defines a user message.
- `{topic}` is a dynamic variable.
- `invoke()` formats the chat prompt.
- `to_messages()` returns the formatted messages.

**Important:** Formatting a chat prompt does not call the AI model.

## 4. Using Multiple Variables

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {subject} teacher."),
    ("human", "Explain {topic} to a {level} student.")
])

result = prompt.invoke({
    "subject": "Python",
    "topic": "Decorators",
    "level": "beginner"
})

print(result.to_messages())
```

This allows the same template to work with different subjects, topics, and student levels.

## 5. Using SystemMessage and HumanMessage

We can also create a template using LangChain message objects.

```python
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful Python tutor."),
    ("human", "Explain {topic}.")
])
```

Here, `SystemMessage` contains fixed instructions, while the human message remains dynamic.

For dynamic system instructions, use a `("system", "...")` tuple or `SystemMessagePromptTemplate`.

## 6. Adding AI Messages to a Chat Prompt

Chat prompts can also contain example assistant responses.

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer briefly."),
    ("human", "What is 2 + 2?"),
    ("ai", "4"),
    ("human", "What is {number} + 5?")
])

result = prompt.invoke({
    "number": 10
})

print(result.to_messages())
```

The earlier human and AI messages provide an example of the expected response style.

This is a basic form of few-shot prompting.

## 7. Connecting ChatPromptTemplate to Groq

```python
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert {subject} teacher. Use simple English."),
    ("human", "Explain {topic} with one example.")
])

formatted_prompt = prompt.invoke({
    "subject": "Python",
    "topic": "Decorators"
})

response = model.invoke(formatted_prompt)

print(response.content)
```

### Execution Flow

```text
Input Dictionary
       |
       v
ChatPromptTemplate
       |
       v
System + Human Messages
       |
       v
     ChatGroq
       |
       v
   AI Response
```

## 8. Creating a Chain Using LCEL

Instead of manually formatting and sending the prompt, we can connect the components.

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()

response = chain.invoke({
    "subject": "Python",
    "topic": "Decorators"
})

print(response)
```

This approach is useful for creating reusable workflows.

## 9. Real-World Applications

**Educational Assistant**

System: You are a programming teacher.

Human: Explain `{topic}` to a `{level}` student.

**Customer Support**

System: You are a professional customer support assistant.

Human: Respond to `{customer_message}`.

**Translation Assistant**

System: Translate text into `{language}`.

Human: `{text}`.

**Technical Interview Assistant**

System: You are a software engineering interviewer.

Human: Ask me questions about `{technology}`.

## 10. Common Mistakes

**Mistake 1 — Confusing text and chat templates**

`PromptTemplate` produces a text-based prompt value, while `ChatPromptTemplate` produces a structured chat prompt value.

**Mistake 2 — Forgetting input variables**

Every required placeholder must receive a value.

**Mistake 3 — Assuming the prompt remembers conversations**

A `ChatPromptTemplate` does not automatically store previous interactions.

**Mistake 4 — Using fixed messages when dynamic ones are needed**

A concrete `SystemMessage` is fixed. Use a role-based message template for variable substitution.

## 11. Quick Revision Questions

**Q1. What is ChatPromptTemplate?**

A reusable LangChain prompt template containing structured chat messages.

**Q2. What does from_messages() do?**

Creates a chat prompt template from a sequence of message definitions.

**Q3. What is the purpose of a system message?**

To provide instructions about the assistant's role and behavior.

**Q4. What is a human message?**

A message representing user input.

**Q5. What does to_messages() return?**

A list of formatted LangChain message objects.

**Q6. Does ChatPromptTemplate automatically remember conversations?**

No. Conversation history must be supplied separately.

**Q7. Can ChatPromptTemplate be used in an LCEL chain?**

Yes, using the pipe operator (`|`).

## 12. Key Takeaways

- `ChatPromptTemplate` creates reusable, role-based prompts.
- It supports system, human, and AI message templates.
- `from_messages()` defines the message structure.
- `invoke()` inserts input values into the template.
- `to_messages()` produces the formatted message list.
- Chat prompts can be passed to Groq models.
- LCEL connects prompts, models, and output parsers.

---

## Learning Resources

- [CampusX LangChain Prompts](https://github.com/campusx-official/langchain-prompts)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 04 — Topic 03
