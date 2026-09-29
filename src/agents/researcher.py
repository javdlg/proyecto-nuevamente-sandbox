import os
import sys
from pydantic import SecretStr
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Add src folder to path so it can find the_models and the_keys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from the_keys import GEMINI_API_KEY
from the_models import GEMINI_EMBEDDINGS
from state import AgentState

def get_retriever():
    """Initializes and returns the retriever pointing to our local vector base."""
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model=GEMINI_EMBEDDINGS,
        api_key=SecretStr(GEMINI_API_KEY) if GEMINI_API_KEY else None,
    )
    
    # Load the vector database generated in Phase 2
    # We use allow_dangerous_deserialization=True because it's a trusted local file
    vectorstore = FAISS.load_local(
        folder_path="vectorstore", 
        embeddings=embeddings_model, 
        allow_dangerous_deserialization=True
    )
    
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
    
    print(f"📚 [Researcher Agent] Found {len(documents)} relevant chunks for '{query}'.")
    
    # Return state update using English keys
    return {
        "retrieved_docs": documents,
        "revision_attempts": 0  # Initialize the counter for the revision loop
    }
