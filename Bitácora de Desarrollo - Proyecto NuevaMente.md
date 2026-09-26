### **Bitácora de Desarrollo: Proyecto NuevaMente**

A tener en cuenta:

- Project management (GitHub Project): Cristian Basto  
- Documentos base (técnicos y no técnicos): Linamaría   
- Documentación general y específicas (RAG, OCI, etc.)  
- Canal \#project-manager: Dailys \- saber en qué va cada uno diariamente.  
- Weeklys: Martes 1:30 pm (MEX) \- 2:30 pm (COL) \- 5:30 pm (CHL-ARG)

**Fechas:**

* **Semana 1:** 21-25 SEP  
* **Semana 2:** 28 SEP \- 2 OCT  
* **Semana 3:** 5-9 OCT  
* **Semana 4:** 12-16 OCT  
* **Semana 5:** 19-23 OCT  
* **Demo Day: 27 OCT**

**Hito 1: Preparación del Entorno y Pipeline de Ingesta**

* **Objetivo:** Construir la base de datos y la extracción de texto.  
* **Tareas:**  
  * Inicializar el repositorio local y configurar el entorno virtual (dependencias: LangChain, PyPDF, OCI SDK, etc.).  
  * Desarrollar el script de ingesta para procesar documentos en formatos PDF, Markdown y texto sin formato.  
  * Implementar técnicas de limpieza y normalización del texto extraído para preparar los datos para la vectorización.  
- **Asignación:** Javi   
- **Tiempos**: Semana 1

**Hito 2: Núcleo del RAG y Vector Store**

**Canal:** \#data-scientist

* **Objetivo:** Lograr que la inteligencia artificial pueda "leer" y recuperar la documentación con precisión técnica.  
* **Tareas:**  
  * Implementar la segmentación semántica (*chunking*) del texto extraído, asegurando no cortar conceptos a la mitad.  
  * Generar los *embeddings* vectoriales del contenido.  
  * Configurar y poblar el Vector Store (ChromaDB o FAISS) para permitir la búsqueda de similitud.  
  * Crear una función de recuperación (*retriever*) que busque los fragmentos más relevantes dada una consulta.  
- **Asignación:** Javi, Linamaría, Álvaro.   
- **Tiempos**: Semana 2-3 

**Hito 3: Orquestación del Sistema Multi-Agente (El Diferenciador)**

**Canal:** \#ai-engineer

* **Objetivo:** Reemplazar un prompt simple por un flujo inteligente de agentes usando LangGraph para planificar, redactar y revisar el contenido.  
* **Tareas:**  
  * **Agente Investigador RAG:** Construir el nodo encargado de extraer la información del Vector Store basándose en los parámetros de entrada (perfil, formato, nicho).  
  * **Agente Redactor Pedagógico:** Diseñar el nodo con *role prompting* que tome el contexto técnico y lo transforme al tono y formato adecuado (ej. de manual técnico a Flashcards para principiantes).  
  * **Agente Revisor:** Crear el nodo que evalúe la claridad pedagógica, detecte alucinaciones comparando con las fuentes originales y asigne el *anclaje\_fuente\_score*.  
* **Asignación**: Yerry, Nicolás, Ivonne, Daniel  
* **Tiempos**: Semana 2-3

**Hito 4: Estructuración de Salida y Metadatos**

**Canal:** \#backend-developer

* **Objetivo:** Garantizar que el sistema se comunique correctamente con cualquier *frontend* o aplicación externa.  
* **Tareas:**  
  * Utilizar *Structured Outputs* (ej. Pydantic) para forzar al LLM a devolver la información estrictamente en el formato JSON requerido.  
  * Asegurar que el JSON incluye metadatos, perfil aplicado, tiempo estimado, conceptos clave, contenido adaptado y la evaluación de calidad.  
- **Asignación**: Ivonne,  Cristian, Daniel  
- **Tiempos**: Semana 4

**Hito 5: Pruebas e Interfaz**

**Canal:** \#machine-learning

* **Objetivo:** Validar el MVP y prepararlo para la demostración.  
* **Tareas:**  
  * Conectar el backend con una interfaz interactiva en Streamlit o Gradio.  
  * Ejecutar pruebas con al menos 3 escenarios distintos (diferentes perfiles y formatos) para asegurar la adaptabilidad.  
  * Construcción interfaz   
  * Probar directamente en OCI para ver si soporta todo el proyecto.  
- **Asignación**: Linamaría, Nicolás \- Frontend  
  - Cristian \- Pruebas  
- **Tiempos**: Semana 1-2

**Hito 6: Integración con OCI (Oracle Cloud Infrastructure)**

**Canal:** \#llm-engineer

* **Objetivo:** Cumplir con el requisito obligatorio de la capa Always Free.  
* **Tareas:**  
  * Configurar credenciales y autenticación para OCI mediante el SDK de Python.  
  * Crear las funciones para subir automáticamente los documentos originales y los JSON generados al *Bucket* de OCI Object Storage.  
  * Capturar el ID del objeto y el estado de la subida para incluirlo en la respuesta final JSON.  
  * Tener en cuenta que la capa Always Free soporte lo que estamos construyendo   
- **Asignación**: Linamaría, Javi, Yerry  
- **Tiempos:** Semana 4

**Hito 7: Documentación (Fase Final)**

- **Tareas:**   
  * Redactar el README.md detallando la arquitectura y las instrucciones de uso para el resto del equipo.  
  * Presentación final  
- **Tiempos:** Semana 5

