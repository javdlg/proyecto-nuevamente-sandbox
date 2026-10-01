from langgraph.graph import StateGraph, END
from state import AgentState

# Importamos los nodos (agentes)
from agents.researcher import researcher_node
from agents.writer import writer_node
from agents.reviewer import reviewer_node

def check_score(state: AgentState) -> str:
    """
    Función de borde condicional.
    Decide si el borrador pasa la revisión o si necesita volver al redactor.
    """
    score = state.get("source_anchoring_score", 0.0)
    attempts = state.get("revision_attempts", 0)
    
    if score >= 0.8:
        print(f"🏁 [Orquestador] ¡Borrador Aprobado! Puntaje: {score}")
        return "approved"
    elif attempts >= 3:
        print(f"⚠️ [Orquestador] Límite de intentos alcanzado (3). Aprobación forzada. Puntaje: {score}")
        return "approved"
    else:
        print(f"🔄 [Orquestador] Borrador Rechazado (Puntaje: {score}). Devolviendo al Redactor...")
        return "needs_revision"

def build_graph():
    """Construye y compila el LangGraph multi-agente."""
    # 1. Inicializamos el Grafo con nuestro TypedDict State
    builder = StateGraph(AgentState)
    
    # 2. Agregamos todos los nodos (agentes)
    builder.add_node("researcher", researcher_node)
    builder.add_node("writer", writer_node)
    builder.add_node("reviewer", reviewer_node)
    
    # 3. Definimos el flujo principal (conexiones)
    builder.set_entry_point("researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "reviewer")
    
    # 4. Definimos el Borde Condicional (El Ciclo)
    # La salida de 'check_score' determina el siguiente paso.
    builder.add_conditional_edges(
        "reviewer",
        check_score,
        {
            "approved": END,               # Si es aprobado, termina el grafo
            "needs_revision": "writer"     # Si es rechazado, vuelve al redactor
        }
    )
    
    # 5. Compilamos y devolvemos
    return builder.compile()
