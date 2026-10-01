import os
import sys

# Add src folder to path so it can find the_models and the_keys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from state import AgentState


def get_retriever():
    """Initializes and returns the retriever pointing to our local vector base."""
    from chunk_embeddings import cargar_vectorstore
    
    # Load the vector database generated in Phase 2 using the unified function
    vectorstore = cargar_vectorstore()

    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.3, "k": 4},
    )


def researcher_node(state: AgentState) -> dict:
    """Node responsible for retrieving context from the Vector Store based on the query."""
    print("🔍 [Researcher Agent] Searching for context in the knowledge base...")

    query = state["query"]
    retriever = get_retriever()
    documents = retriever.invoke(query)

    print(
        f"📚 [Researcher Agent] Found {len(documents)} relevant chunks for '{query}'."
    )

    # Return state update using English keys
    return {
        "retrieved_docs": documents,
        "revision_attempts": 0,  # Initialize the counter for the revision loop
    }
