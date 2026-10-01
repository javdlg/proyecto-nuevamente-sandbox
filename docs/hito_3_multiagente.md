# Hito 3: Orquestación Multi-Agente (LangGraph) - "El Diferenciador"

## 🎯 Objetivo
Reemplazar un flujo tradicional y plano de RAG por un sistema cognitivo multi-agente. Este sistema es capaz de investigar, redactar contenido pedagógico adaptado a un perfil específico y, críticamente, **autoevaluarse** para detectar y corregir alucinaciones antes de entregar el resultado al usuario final.

## ⚙️ Arquitectura y Tecnologías
*   **Librerías principales:** `langgraph`, `pydantic`, `langchain-google-genai`
*   **Módulos clave:** `src/graph.py`, `src/state.py` y la carpeta `src/agents/`
*   **Modelos LLM (Gemini):** 
    *   *Redactor y Revisor:* `gemini-3.5-flash-lite` (Configurado para pivotar fácilmente a `gemini-3.8-flash` según la demanda de la API).

## 🧠 Decisiones Técnicas y Flujo del Grafo
El corazón del sistema es un `StateGraph` que hace circular un objeto de estado (`AgentState`) a través de tres nodos (agentes) principales:

1.  **Investigador (`researcher.py`):**
    *   Toma la `query` del usuario.
    *   Se conecta a FAISS (`cargar_vectorstore()`).
    *   Retorna los fragmentos de contexto exactos.

2.  **Redactor Pedagógico (`writer.py`):**
    *   Toma el contexto, el perfil del usuario, el formato de salida y cualquier *feedback* previo.
    *   Usa **Role Prompting** estricto para transformar el texto árido en material educativo (ej. analogías, flashcards).
    *   *Regla de Oro:* Tiene prohibido usar conocimiento externo.

3.  **Revisor / Fact-Checker (`reviewer.py`):**
    *   Toma el borrador del Redactor y lo compara contra el contexto original extraído por el Investigador.
    *   Usa **Structured Outputs (Pydantic)** para devolver un objeto JSON determinista con un `score` (0.0 a 1.0) y un `feedback` textual.
    *   Opera con `temperature=0.0` para garantizar un juicio frío, lógico y libre de alucinaciones propias.

4.  **Bucle de Corrección (Conditional Edge):**
    *   El orquestador (`graph.py`) lee el puntaje del Revisor.
    *   Si el puntaje es `< 0.8`, el borrador es rechazado y devuelto al Redactor junto con las críticas.
    *   Si el puntaje es `>= 0.8` (o se superan los 3 intentos máximos), el contenido se aprueba.

## 🚀 Resultado y Pruebas de Estrés
Durante las pruebas de validación, se realizó una "prueba de estrés por alucinación inducida" (preguntando por la conexión entre Oracle VCN y satélites Starlink, algo ausente en los documentos). 

**El sistema demostró su valor:**
*   El Redactor intentó alucinar la respuesta.
*   El Revisor detectó la anomalía dos veces, asignando puntajes de `0.2` y `0.0`.
*   En la tercera iteración, el Redactor corrigió su comportamiento, aclaró explícitamente que dicha tecnología no formaba parte del manual técnico y explicó el concepto real de VCN obteniendo un `1.0` final.
