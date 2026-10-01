# Hito 2: Implementación del Vector Store (FAISS)

## 🎯 Objetivo
Transformar el texto limpio proveniente de la ingesta (Hito 1) en representaciones matemáticas (Embeddings) y almacenarlas en una base de datos vectorial local y ultrarrápida. Esto permite realizar búsquedas semánticas (por significado y no solo por coincidencia de palabras) cuando el usuario hace una consulta.

## ⚙️ Arquitectura y Tecnologías
*   **Librerías principales:** `langchain-community`, `langchain-google-genai`, `faiss-cpu`
*   **Módulo clave:** `src/chunk_embeddings.py`
*   **Modelo de Embeddings:** `models/gemini-embedding-001` (A través de Google AI Studio)
*   **Base de Datos Vectorial:** FAISS (Facebook AI Similarity Search)

## 🧠 Decisiones Técnicas
1.  **Estrategia de Chunking:** Se utilizó `RecursiveCharacterTextSplitter` con un `chunk_size` de 1000 caracteres y un `chunk_overlap` de 100.
    *   *Justificación:* Documentos técnicos complejos (como Arquitecturas Cloud) pierden contexto si se cortan en pedazos muy pequeños (ej. 300). Un tamaño de 1000 asegura que las ideas completas se mantengan juntas, y el solapamiento de 100 evita que conceptos se corten por la mitad entre dos fragmentos.
2.  **Persistencia Local (FAISS):** Para mantener el entorno *sandbox* ágil y gratuito, se optó por guardar el índice de FAISS en disco local (carpeta `vectorstore/`).
3.  **Centralización de la Carga:** Se refactorizó el código para incluir una función única `cargar_vectorstore()` que se encarga de instanciar el modelo de embeddings e hidratar el índice FAISS, evitando código duplicado en los agentes del Hito 3.

## 🚀 Resultado
Un índice vectorial pre-calculado que responde a búsquedas de similitud en milisegundos, devolviendo los 4 fragmentos (`k=4`) más relevantes del texto original que coinciden con la intención de búsqueda del usuario.
