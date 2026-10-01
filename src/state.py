from typing import TypedDict, List
from langchain_core.documents import Document

class AgentState(TypedDict):
    # --- Parámetros de Entrada ---
    query: str               # Tema a consultar (ej: "Virtual Cloud Network")
    user_profile: str        # Público objetivo (ej: "Principiante", "Arquitecto")
    output_format: str       # Formato deseado (ej: "Flashcards", "Resumen")
    
    # --- Estado Interno del Grafo ---
    retrieved_docs: List[Document] # Contexto extraído por el Agente Investigador
    current_draft: str             # Texto redactado por el Agente Redactor
    review_feedback: str           # Comentarios del Agente Revisor si hay errores
    revision_attempts: int         # Contador para evitar bucles infinitos
    
    # --- Salida Final ---
    source_anchoring_score: float  # Puntaje de fidelidad respecto a la fuente original
    final_content: str             # El texto final pulido y aprobado
