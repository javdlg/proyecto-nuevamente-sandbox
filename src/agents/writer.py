import os
import sys

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

# Add src folder to path so it can find the_models and the_keys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from state import AgentState
from the_keys import GEMINI_API_KEY
from the_models import GEMINI_PRO


def writer_node(state: AgentState) -> dict:
    """Node responsible for drafting pedagogical content based on retrieved context."""
    print("✍️  [Writer Agent] Drafting content based on user profile and format...")

    # 1. Extract inputs from the state
    query = state.get("query", "")
    user_profile = state.get("user_profile", "General Audience")
    output_format = state.get("output_format", "Summary")
    retrieved_docs = state.get("retrieved_docs", [])

    # 2. Combine retrieved documents into a single context string
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # 3. Initialize the LLM
    # We use GEMINI_PRO for high-quality pedagogical writing and reasoning.
    # Temperature 0.4 gives a good balance: creative enough for formats like "Flashcards",
    # but strict enough to stick to the facts.
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_PRO,
        api_key=SecretStr(GEMINI_API_KEY) if GEMINI_API_KEY else None,
        temperature=0.4,
    )

    # 4. Create the Prompt Template (Role Prompting)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert pedagogical writer and technical communicator. 
Your task is to explain complex technical concepts in a clear, engaging, and highly accurate manner.

INSTRUCTIONS:
- You must adapt your tone, vocabulary, and depth to match the target User Profile: {user_profile}.
- You must structure your response strictly in the requested Output Format: {output_format}.
- CRITICAL: You must base your explanation EXCLUSIVELY on the provided Technical Context. 
  Do not introduce outside facts or hallucinate features not mentioned in the context.

TECHNICAL CONTEXT:
{context}
""",
            ),
            ("human", "Topic to explain: {query}"),
        ]
    )

    # 5. Build and invoke the chain
    chain = prompt | llm
    response = chain.invoke(
        {
            "user_profile": user_profile,
            "output_format": output_format,
            "context": context,
            "query": query,
        }
    )

    print("✅ [Writer Agent] Draft completed.")

    # 6. Return the updated state
    return {"current_draft": response.content}
