from langgraph.graph import END, StateGraph

from agents.researcher import researcher_node
from agents.reviewer import reviewer_node
from agents.writer import writer_node
from state import AgentState


def check_score(state: AgentState) -> str:
    """
    Conditional edge function.
    Decides whether the draft passes the review or needs to go back to the writer.
    """
    score = state.get("source_anchoring_score", 0.0)
    attempts = state.get("revision_attempts", 0)

    if score >= 0.8:
        print(f"🏁 [Graph Orchestrator] Draft Approved! Score: {score}")
        return "approved"
    elif attempts >= 3:
        print(
            f"⚠️ [Graph Orchestrator] Max attempts reached (3). Forcing approval. Score: {score}"
        )
        return "approved"
    else:
        print(
            f"🔄 [Graph Orchestrator] Draft Rejected (Score: {score}). Sending back to Writer..."
        )
        return "needs_revision"


def build_graph():
    """Builds and compiles the multi-agent LangGraph."""
    # 1. Initialize Graph with our TypedDict State
    builder = StateGraph(AgentState)

    # 2. Add all agent nodes
    builder.add_node("researcher", researcher_node)
    builder.add_node("writer", writer_node)
    builder.add_node("reviewer", reviewer_node)

    # 3. Define the main workflow (edges)
    builder.set_entry_point("researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "reviewer")

    # 4. Define the Conditional Edge (The Loop)
    # The output of 'check_score' determines the next step.
    builder.add_conditional_edges(
        "reviewer",
        check_score,
        {
            "approved": END,  # If approved, finish the graph
            "needs_revision": "writer",  # If rejected, loop back to the writer
        },
    )

    # 5. Compile and return
    return builder.compile()
