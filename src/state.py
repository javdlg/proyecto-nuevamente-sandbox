from typing import TypedDict, List
from langchain_core.documents import Document

class AgentState(TypedDict):
    # --- Parámetros de Entrada ---
    query: str               # Tema a consultar (ej: "Virtual Cloud Network")
    perfil_usuario: str      # Público objetivo (ej: "Principiante", "Arquitecto")
    formato_salida: str      # Formato (ej: "Flashcards", "Manual", "Resumen")
    
    # --- Estado Interno del Grafo ---
    documentos_recuperados: List[Document] # Contexto extraído por el Agente Investigador
    borrador_actual: str                   # Texto redactado por el Agente Pedagógico
    feedback_revision: str                 # Comentarios del Agente Revisor si encuentra errores
    intentos_revision: int                 # Contador para evitar bucles infinitos
    
    # --- Salida Final ---
    anclaje_fuente_score: float            # Puntuación de fidelidad a la fuente original
    contenido_aprobado: str                # El texto final pulido y revisado
