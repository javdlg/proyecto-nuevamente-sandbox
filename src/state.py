from typing import TypedDict, List
from langchain_core.documents import Document

class AgentState(TypedDict):
    # --- Input Parameters ---
    query: str               # Topic to query (e.g., "Virtual Cloud Network")
    user_profile: str        # Target audience (e.g., "Beginner", "Architect")
    output_format: str       # Format (e.g., "Flashcards", "Manual", "Summary")
    
    # --- Internal Graph State ---
    retrieved_docs: List[Document] # Context extracted by the Researcher Agent
    current_draft: str             # Text drafted by the Writer Agent
    review_feedback: str           # Comments from the Reviewer Agent if errors are found
    revision_attempts: int         # Counter to avoid infinite loops
    
    # --- Final Output ---
    source_anchoring_score: float  # Fidelity score against the original source
    final_content: str             # The polished and reviewed final text
