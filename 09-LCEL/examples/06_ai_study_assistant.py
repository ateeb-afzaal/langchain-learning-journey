
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableBranch,
    RunnablePassthrough,
)


# ==========================================
# STEP 1: LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# STEP 2: INPUT VALIDATION
# ==========================================

VALID_LEVELS = {"beginner", "intermediate", "advanced"}


def normalize_input(data):
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary.")

    topic = data.get("topic")
    level = data.get("level", "beginner")

    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    if not isinstance(level, str):
        raise TypeError("Level must be a string.")

    topic = " ".join(topic.strip().split())
    level = level.strip().lower()

    if level not in VALID_LEVELS:
        raise ValueError(
            "Level must be beginner, intermediate, or advanced."
        )

    return {
        "topic": topic,
        "level": level,
    }


normalize = RunnableLambda(normalize_input)


# ==========================================
# STEP 3: INITIALIZE GROQ
# ==========================================

def create_model():
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is missing from your environment."
        )

    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )


# ==========================================
# STEP 4: CREATE PROMPTS
# ==========================================

beginner_prompt = PromptTemplate.from_template(
    """
    You are a friendly Python and AI programming tutor.

    Topic: {topic}

    Explain this topic to a beginner.

    Requirements:
    - Use simple English.
    - Explain the main concept.
    - Include one easy example.
    - Avoid unnecessary technical jargon.
    - Keep the answer concise.
    """
)

intermediate_prompt = PromptTemplate.from_template(
    """
    You are an experienced software development tutor.

    Topic: {topic}

    Explain this topic to an intermediate student.

    Requirements:
    - Explain the concept clearly.
    - Include technical terminology where appropriate.
    - Show one practical application.
    - Keep the answer concise.
    """
)

advanced_prompt = PromptTemplate.from_template(
    """
    You are a senior Python and AI software engineer.

    Topic: {topic}

    Explain this topic to an advanced CS student.

    Requirements:
    - Include important technical details.
    - Explain the underlying mechanism.
    - Mention practical software engineering use cases.
    - Include one advanced example.
    - Keep the answer concise.
    """
)

questions_prompt = PromptTemplate.from_template(
    """
    You are a software engineering interviewer.

    Topic: {topic}
    Student level: {level}

    Generate exactly 3 interview questions suitable
    for this learning level.

    Return a numbered list.
    Do not provide answers.
    """
)


# ==========================================
# STEP 5: BUILD THE LCEL WORKFLOW
# ==========================================

def build_study_chain(model):

    parser = StrOutputParser()

    beginner_chain = beginner_prompt | model | parser
    intermediate_chain = intermediate_prompt | model | parser
    advanced_chain = advanced_prompt | model | parser

    # Select one explanation branch
    explanation_branch = RunnableBranch(
        (
            lambda data: data["level"] == "beginner",
            beginner_chain,
        ),
        (
            lambda data: data["level"] == "intermediate",
            intermediate_chain,
        ),
        advanced_chain,
    )

    # Independent interview questions branch
    questions_chain = questions_prompt | model | parser

    # Validation → Parallel generation → Enrichment
    study_chain = (
        normalize
        | RunnablePassthrough.assign(
            display_label=lambda data: (
                f"{data['topic']} ({data['level']})"
            ),
            explanation=explanation_branch,
            questions=questions_chain,
        )
        | RunnablePassthrough.assign(
            explanation_length=lambda data: len(
                str(data["explanation"])
            )
        )
    )

    return study_chain


# ==========================================
# STEP 6: DISPLAY RESULTS
# ==========================================

def display_results(result):

    print("\n" + "=" * 60)
    print("AI PROGRAMMING STUDY ASSISTANT")
    print("=" * 60)

    print("\nTOPIC:")
    print(result["topic"])

    print("\nLEARNING LEVEL:")
    print(result["level"].title())

    print("\nDISPLAY LABEL:")
    print(result["display_label"])

    print("\nEXPLANATION:")
    print(str(result["explanation"]))

    print("\nINTERVIEW QUESTIONS:")
    print(str(result["questions"]))

    print("\nEXPLANATION LENGTH:")
    print(result["explanation_length"])

    print("\n" + "=" * 60)


# ==========================================
# STEP 7: INTERACTIVE APPLICATION
# ==========================================

def main():

    print("=" * 60)
    print("WELCOME TO AI PROGRAMMING STUDY ASSISTANT")
    print("=" * 60)

    print("\nSupported levels:")
    print("beginner | intermediate | advanced")
    print("\nType 'exit' as the topic to quit.")

    # Validate the API configuration once at startup
    try:
        model = create_model()
        study_chain = build_study_chain(model)

    except Exception as error:
        print("\nStartup failed:", error)
        return

    while True:

        try:
            print("\n" + "-" * 60)

            topic = input("Enter a programming topic: ").strip()

            if topic.lower() in {"exit", "quit"}:
                print("\nGoodbye! Keep learning.")
                break

            level = input(
                "Enter level (beginner/intermediate/advanced): "
            ).strip()

            user_input = {
                "topic": topic,
                "level": level or "beginner",
            }

            # Validate before making any model calls
            normalized = normalize.invoke(user_input)

            print("\nGenerating study material...\n")

            result = study_chain.invoke(normalized)

            display_results(result)

        except (KeyboardInterrupt, EOFError):
            print("\n\nApplication closed.")
            break

        except (ValueError, TypeError) as error:
            print("\nInput error:", error)

        except Exception as error:
            print("\nModel or workflow error:", error)


# ==========================================
# STEP 8: APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
