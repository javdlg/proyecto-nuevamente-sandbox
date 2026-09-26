# 🧠 Proyecto NuevaMente - Sandbox (Hackathon ONE G10)

Bienvenido al entorno de desarrollo y experimentación para **NuevaMente**. Este repositorio sirve como área de pruebas (*sandbox*) para diseñar, iterar y consolidar la arquitectura de datos y los modelos de inteligencia artificial antes de integrarlos al repositorio oficial del equipo en el Hackathon ONE (Grupo 10).

## 🎯 Objetivo del Proyecto
Construir un sistema inteligente capaz de ingerir documentaciones técnicas complejas (PDF, Markdown, texto) y transformarlas automáticamente en contenidos educativos personalizados. El sistema ajusta el material según el perfil del destinatario (ej. Principiante, Arquitecto) y el formato pedagógico deseado (ej. Flashcards, Quizzes, Resúmenes).

## ⚙️ Enfoque Técnico y Arquitectura
El núcleo de la solución se basa en un flujo de procesamiento de lenguaje natural (NLP) estructurado para garantizar la fidelidad técnica y evitar alucinaciones:

*   **Ingesta y Pipeline ETL:** Extracción y limpieza de texto desde fuentes documentales no estructuradas.
*   **Motor RAG (Retrieval-Augmented Generation):** Segmentación semántica (*chunking*) y generación de embeddings almacenados en un Vector Store (FAISS).
*   **Orquestación Multi-Agente:** Implementación de un grafo de decisión (LangGraph) compuesto por agentes especializados (Investigador, Redactor Pedagógico y Revisor/Crítico).
*   **Capa de Persistencia:** Integración nativa con OCI Object Storage dentro de la capa *Always Free* de Oracle Cloud Infrastructure.
*   **Salida Estructurada:** Generación de payloads en formato JSON estricto para facilitar la integración con la interfaz de usuario.

## 🗺️ Bitácora de Desarrollo (Hitos)
1.  **[x] Hito 1:** Preparación del entorno y script de ingesta de documentos (PDF/Markdown).
2.  **[x] Hito 2:** Implementación del Vector Store local (FAISS) y segmentación semántica de datos.
3.  **[ ] Hito 3:** Desarrollo de nodos LangGraph para el sistema multi-agente.
4.  **[ ] Hito 4:** Configuración de *Structured Outputs* (JSON) y metadatos pedagógicos.
5.  **[ ] Hito 5:** Integración de OCI SDK para la subida de archivos.
6.  **[ ] Hito 6:** Pruebas de integración, validación de fidelidad (*anclaje_fuente_score*) y preparación para la interfaz interactiva.

## 📁 Estructura del Proyecto

```text
.
├── data/                  # Documentos PDF, MD o TXT de prueba
├── src/                   # Código fuente principal
│   ├── ingestion.py       # Script de limpieza y carga de texto
│   ├── chunk_embeddings.py # Generación de chunks y VectorStore (FAISS)
│   ├── the_models.py      # Configuración de modelos (Gemini Pro/Flash)
│   └── the_keys.py        # Carga de variables de entorno
├── tests/                 # Scripts de validación y diagnóstico
│   ├── test_fase2.py      # Test automatizado (Ingesta + VectorStore en lote)
│   └── check_models.py    # Diagnóstico de modelos permitidos por API Key
├── vectorstore/           # [Generado] Índice FAISS local (ignorado en Git)
├── .gitignore             # Reglas para omitir archivos (ej. .venv, .env, vectorstore)
├── requirements.txt       # Dependencias del proyecto (LangChain, PyPDF, FAISS, etc.)
└── README.md              # Documentación del proyecto
```

## 🚀 Instalación y Uso (Entorno Local)

Para replicar este entorno de pruebas y correr la Fase 1 y 2:

**1. Crear y activar el entorno virtual:**
```bash
python -m venv .venv

# En Windows (PowerShell/CMD):
.\.venv\Scripts\activate

# En Mac/Linux:
source .venv/bin/activate
```

**2. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**3. Configurar variables de entorno:**
Crea un archivo llamado `.env` en la raíz del proyecto y agrega tu clave de acceso de Google AI Studio:
```env
GEMINI_API_KEY="TU_API_KEY_AQUI"
```

**4. Ejecutar el pipeline de prueba (Fases 1 y 2 integradas):**
Asegúrate de colocar al menos un archivo `.pdf`, `.md` o `.txt` en la carpeta `data/` y luego ejecuta en tu terminal:
```bash
python tests/test_fase2.py
```
*Este script leerá dinámicamente los archivos, aplicará técnicas de limpieza, generará los embeddings semánticos mediante la API de Gemini y guardará el índice de búsqueda en la carpeta `vectorstore/`.*

---
*Este repositorio es de uso personal y sirve como base técnica para las contribuciones al proyecto oficial del Hackathon ONE G10.*
