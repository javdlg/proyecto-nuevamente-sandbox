import os
import sys

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

# Agregamos la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from state import AgentState
from the_keys import GEMINI_API_KEY
from the_models import GEMINI_GENERACION


def writer_node(state: AgentState) -> dict:
    """Nodo responsable de redactar contenido pedagógico basado en el contexto recuperado."""
    print("✍️  [Agente Redactor] Redactando contenido basado en el perfil y formato...")
    
    # 1. Extraer los datos del estado
    query = state.get("query", "")
    user_profile = state.get("user_profile", "Audiencia General")
    output_format = state.get("output_format", "Resumen")
    retrieved_docs = state.get("retrieved_docs", [])
    review_feedback = state.get("review_feedback", "")
    
    # 2. Combinar los documentos recuperados en un solo bloque de contexto
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Incluir los comentarios del revisor si existen (para el ciclo de corrección)
    feedback_section = (
        f"\n\nCOMENTARIOS CRÍTICOS DEL REVISOR PARA CORREGIR EN ESTE NUEVO BORRADOR:\n{review_feedback}\n"
        if review_feedback
        else ""
    )
    
    # 3. Inicializar el LLM
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_GENERACION,
        api_key=SecretStr(GEMINI_API_KEY) if GEMINI_API_KEY else None,
        temperature=0.4,
    )
    
    # 4. Crear la plantilla del Prompt (Role Prompting en Español)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Eres un redactor pedagógico experto y comunicador técnico. 
Tu tarea es explicar conceptos técnicos complejos de una manera clara, atractiva y altamente precisa.

INSTRUCCIONES:
- Debes adaptar tu tono, vocabulario y profundidad para que coincida con el Perfil del Usuario objetivo: {user_profile}.
- Debes estructurar tu respuesta estrictamente en el Formato Solicitado: {output_format}.
- CRÍTICO: Debes basar tu explicación EXCLUSIVAMENTE en el Contexto Técnico proporcionado. 
  No introduzcas datos externos ni inventes (alucines) características que no se mencionen en el contexto.

CONTEXTO TÉCNICO:
{context}
""",
            ),
            ("human", "Tema a explicar: {query}{feedback_section}"),
        ]
    )
    
    # 5. Construir y ejecutar la cadena
    chain = prompt | llm
    response = chain.invoke(
        {
            "user_profile": user_profile,
            "output_format": output_format,
            "context": context,
            "query": query,
            "feedback_section": feedback_section,
        }
    )
    
    print("✅ [Agente Redactor] Borrador completado.")
    
    # 6. Devolver el estado actualizado
    return {"current_draft": response.content}
