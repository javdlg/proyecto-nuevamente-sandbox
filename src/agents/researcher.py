import os
import sys
from pydantic import SecretStr
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Añadimos la ruta de la carpeta src para que encuentre the_models y the_keys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from the_keys import GEMINI_API_KEY
from the_models import GEMINI_EMBEDDINGS
from state import AgentState

def get_retriever():
    """Inicializa y devuelve el retriever apuntando a nuestra base vectorial local."""
    modelo_embeddings = GoogleGenerativeAIEmbeddings(
        model=GEMINI_EMBEDDINGS,
        api_key=SecretStr(GEMINI_API_KEY) if GEMINI_API_KEY else None,
    )
    
    # Cargar la base de datos vectorial generada en el Hito 2
    # Usamos allow_dangerous_deserialization=True porque es un archivo local de confianza
    vectorstore = FAISS.load_local(
        folder_path="vectorstore", 
        embeddings=modelo_embeddings, 
        allow_dangerous_deserialization=True
    )
    
    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.3, "k": 4},
    )

def nodo_investigador(state: AgentState) -> dict:
    """Nodo responsable de recuperar contexto del Vector Store según la query."""
    print("🔍 [Agente Investigador] Buscando contexto en la base de conocimientos...")
    
    query = state["query"]
    retriever = get_retriever()
    documentos = retriever.invoke(query)
    
    print(f"📚 [Agente Investigador] Se encontraron {len(documentos)} fragmentos relevantes para '{query}'.")
    
    # Devolvemos la actualización del estado
    return {
        "documentos_recuperados": documentos,
        "intentos_revision": 0  # Inicializamos el contador para el ciclo de revisión posterior
    }
