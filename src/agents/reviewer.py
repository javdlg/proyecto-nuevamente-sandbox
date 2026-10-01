import os
import sys
from typing import cast

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field, SecretStr

# Agregamos la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from state import AgentState
from the_keys import GEMINI_API_KEY
from the_models import GEMINI_LIGERO


# Definimos la salida estructurada usando Pydantic (Hito 4)
class ReviewResult(BaseModel):
    score: float = Field(
        description="Puntaje de fidelidad del 0.0 al 1.0. Un 1.0 significa que es perfectamente fiel al contexto. Puntajes bajos indican alucinaciones o errores."
    )
    feedback: str = Field(
        description="Comentarios detallados explicando el puntaje e instruyendo al redactor sobre lo que debe corregir. Si el puntaje es 1.0, escribe 'Aprobado'."
    )


def reviewer_node(state: AgentState) -> dict:
    """Nodo responsable de revisar el borrador contra el contexto original."""
    print(
        "🕵️  [Agente Revisor] Evaluando el borrador en busca de alucinaciones y calidad pedagógica..."
    )

    # 1. Extraer los datos del estado
    query = state.get("query", "")
    current_draft = state.get("current_draft", "")
    retrieved_docs = state.get("retrieved_docs", [])
    revision_attempts = state.get("revision_attempts", 0)

    # 2. Combinar los documentos en un solo bloque de contexto
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # 3. Inicializar el LLM (Usamos temperatura=0.0 para una evaluación estricta y determinista)
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_LIGERO,  # Usamos el modelo ligero para la revisión (originalmente va GEMINI_GENERACION, pero suele estar saturado)
        api_key=SecretStr(GEMINI_API_KEY) if GEMINI_API_KEY else None,
        # temperature=0.0,  # Deshabilitado temporalmente: flash-lite usa defaults fijos
    )

    # Forzar al LLM a devolver nuestro esquema Pydantic
    structured_llm = llm.with_structured_output(ReviewResult)

    # 4. Crear la plantilla del Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Eres un experto Evaluador de Datos (Fact-Checker) y Revisor Técnico.
Tu tarea es evaluar un texto borrador comparándolo con el Contexto Técnico original.

INSTRUCCIONES:
1. Compara el BORRADOR con el CONTEXTO TÉCNICO.
2. Busca Alucinaciones: ¿Menciona el borrador datos, características o números que no están presentes en el contexto?
3. Devuelve una evaluación estructurada con un 'score' (0.0 a 1.0) y un 'feedback'.
4. Si hay alucinaciones u omisiones críticas, el puntaje debe ser inferior a 0.8.
5. Si el borrador es completamente fiel y preciso, otorga un puntaje alto (0.8 - 1.0).

CONTEXTO TÉCNICO:
{context}
""",
            ),
            ("human", "Tema: {query}\n\nBORRADOR A REVISAR:\n{draft}"),
        ]
    )

    # 5. Construir y ejecutar la cadena
    chain = prompt | structured_llm
    result = cast(
        ReviewResult,
        chain.invoke({"context": context, "query": query, "draft": current_draft}),
    )

    print(f"✅ [Agente Revisor] Evaluación completada. Puntaje: {result.score}")

    # 6. Devolver el estado actualizado
    return {
        "source_anchoring_score": result.score,
        "review_feedback": result.feedback,
        "revision_attempts": revision_attempts + 1,
    }
