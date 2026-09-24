# 🧠 Proyecto NuevaMente - Sandbox (Hackathon ONE G10)

Bienvenido al entorno de desarrollo y experimentación privado para **NuevaMente**. Este repositorio sirve como área de pruebas (*sandbox*) para diseñar, iterar y consolidar la arquitectura de datos y los modelos de inteligencia artificial antes de integrarlos al repositorio oficial del equipo en el Hackathon ONE (Grupo 10).

## 🎯 Objetivo del Proyecto
Construir un sistema inteligente capaz de ingerir documentaciones técnicas complejas (PDF, Markdown, texto) y transformarlas automáticamente en contenidos educativos personalizados. El sistema ajusta el material según el perfil del destinatario (ej. Principiante, Arquitecto) y el formato pedagógico deseado (ej. Flashcards, Quizzes, Resúmenes).

## ⚙️ Enfoque Técnico y Arquitectura
El núcleo de la solución se basa en un flujo de procesamiento de lenguaje natural (NLP) estructurado para garantizar la fidelidad técnica y evitar alucinaciones:

*   **Ingesta y Pipeline ETL:** Extracción y limpieza de texto desde fuentes documentales no estructuradas.
*   **Motor RAG (Retrieval-Augmented Generation):** Segmentación semántica (*chunking*) y generación de embeddings almacenados en un Vector Store (ChromaDB / FAISS).
*   **Orquestación Multi-Agente:** Implementación de un grafo de decisión (LangGraph) compuesto por agentes especializados (Investigador, Redactor Pedagógico y Revisor/Crítico).
*   **Capa de Persistencia:** Integración nativa con OCI Object Storage dentro de la capa *Always Free* de Oracle Cloud Infrastructure.
*   **Salida Estructurada:** Generación de payloads en formato JSON estricto para facilitar la integración con la interfaz de usuario.

## 🗺️ Bitácora de Desarrollo (Hitos)
1.  **[ ] Hito 1:** Preparación del entorno y script de ingesta de documentos (PDF/Markdown).
2.  **[ ] Hito 2:** Implementación del Vector Store local y segmentación de datos.
3.  **[ ] Hito 3:** Desarrollo de nodos LangGraph para el sistema multi-agente.
4.  **[ ] Hito 4:** Configuración de *Structured Outputs* (JSON) y metadatos pedagógicos.
5.  **[ ] Hito 5:** Integración de OCI SDK para la subida de archivos.
6.  **[ ] Hito 6:** Pruebas de integración, validación de fidelidad (*anclaje_fuente_score*) y preparación para la interfaz interactiva.

## 📁 Estructura del Proyecto

```text
.
├── data/               # Documentos PDF, MD o TXT de prueba
├── src/                # Carpeta para el código fuente principal
│   └── ingestion.py    # Script de ingesta y procesamiento
├── notebooks/          # Experimentos interactivos o pruebas de embeddings
├── .gitignore          # Reglas para omitir archivos y credenciales
├── requirements.txt    # Dependencias del proyecto (LangChain, PyPDF, etc.)
└── README.md           # Documentación del proyecto
```

## 🚀 Instalación y Uso (Entorno Local)

Para replicar este entorno de pruebas:

1. Clonar este repositorio:
    ```bash
    git clone https://github.com/tu-usuario/proyecto-nuevamente-sandbox.git
    cd proyecto-nuevamente-sandbox
    ```

2. Crear y activar un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instalar las dependencias (por definir en requirements.txt):
    ```bash
    pip install -r requirements.txt
    ```

4. Configurar variables de entorno (API Keys de LLMs, Credenciales de OCI) en un archivo .env.


Este repositorio es de uso personal y sirve como base técnica para las contribuciones al proyecto oficial del Hackathon ONE.
