# Hito 1: Ingesta y Pipeline ETL

## 🎯 Objetivo
El objetivo de este hito fue establecer la base del sistema RAG (Retrieval-Augmented Generation) mediante la creación de un pipeline capaz de ingerir documentos no estructurados (principalmente PDFs y archivos Markdown), limpiar su contenido y prepararlos para su posterior vectorización.

## ⚙️ Arquitectura y Tecnologías
*   **Lenguaje:** Python
*   **Librerías principales:** `langchain`, `pypdf`, `langchain-text-splitters`
*   **Módulo clave:** `src/ingestion.py`

## 🧠 Decisiones Técnicas
1.  **Carga de Documentos:** Se implementó soporte dual. El sistema detecta la extensión del archivo (`.pdf` o `.md`) y utiliza el cargador correspondiente de LangChain (`PyPDFLoader` o `TextLoader`). Esto permite a los profesores o expertos subir tanto manuales técnicos formales como apuntes rápidos.
2.  **Limpieza y Normalización:** Se diseñó una función para limpiar el texto extraído, eliminando saltos de línea excesivos y caracteres nulos que pudieran ensuciar el contexto que leerán los agentes más adelante.
3.  **Preparación para Chunking:** En este hito se dejó preparada la estructura de documentos (`Document` de LangChain) para que el Hito 2 pudiera aplicar cortes semánticos sin perder la metadata (origen del archivo, página, etc.).

## 🚀 Resultado
Un módulo robusto que escanea automáticamente la carpeta `data/`, procesa cualquier documento soportado y devuelve una lista unificada de documentos limpios, listos para convertirse en *embeddings*.
