import os
import sys

# Add src folder to path so it can import the graph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from graph import build_graph
from state import AgentState


def main():
    print("🚀 Inicializando el Sistema Multi-Agente (LangGraph)...\n")

    # Compilar el grafo
    graph = build_graph()

    # Definir los parámetros de prueba iniciales
    inputs: AgentState = {
        "query": "¿Qué es una VCN y cuáles son sus componentes principales?",
        "user_profile": "Estudiante de secundaria sin conocimientos técnicos previos",
        "output_format": "Explicación sencilla con una analogía cotidiana y 3 flashcards finales",
        "retrieved_docs": [],
        "current_draft": "",
        "review_feedback": "",
        "revision_attempts": 0,
        "source_anchoring_score": 0.0,
        "final_content": "",
    }

    print("-" * 50)
    print(f"Pregunta: {inputs['query']}")
    print(f"Perfil: {inputs['user_profile']}")
    print(f"Formato: {inputs['output_format']}")
    print("-" * 50 + "\n")

    # Ejecutar el grafo de principio a fin
    # graph.invoke() maneja automáticamente el paso del estado de nodo a nodo
    final_state = graph.invoke(inputs)

    print("\n" + "=" * 50)
    print("🎉 CONTENIDO FINAL APROBADO")
    print("=" * 50)
    print(final_state["current_draft"])
    print("\n" + "=" * 50)
    print(f"Score de Fidelidad: {final_state['source_anchoring_score']}")
    print(f"Intentos de Revisión: {final_state['revision_attempts']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
