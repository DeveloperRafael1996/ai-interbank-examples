# AI Interbank — LangChain, LangGraph & CrewAI Examples

Colección de ejemplos prácticos de LangChain, LangGraph y CrewAI aplicados a casos de uso del contexto bancario/biométrico.

---

## Estructura del proyecto

```
AI_Interbank/
├── LangChain/
│   ├── resume.py            # Ejemplo 1: Cadena de resumen simple (LCEL)
│   ├── tools.py             # Ejemplo 2: Agente con herramientas (Tools)
│   ├── cv.py                # Ejemplo 3: Extracción estructurada con Pydantic
│   ├── clasify_error.py     # Ejemplo 4: Clasificación estructurada de errores
│   ├── rag_simple.py        # Ejemplo 5: RAG simple (búsqueda semántica)
│   ├── agent_tools.py       # Ejemplo 6: Agente con herramientas de diagnóstico biométrico
│   ├── tts_alert.py         # Ejemplo 7: Redacción de mensajes técnicos con LCEL
│   └── bff_docs_agent.py    # Ejemplo 8: Agente de investigación y resumen de documentación
├── LangGraph/
│   ├── workflow.py          # Ejemplo 1: Workflow simple con estado compartido
│   ├── routing.py           # Ejemplo 2: Routing condicional
│   ├── human.py             # Ejemplo 3: Human-in-the-loop (revisión humana)
│   ├── rag_simple.py        # Ejemplo 4: RAG simple con recuperación semántica
│   ├── support_workflow.py  # Ejemplo 5: Pipeline de diagnóstico de operaciones
│   ├── tts_alert.py         # Ejemplo 6: Redacción y aprobación humana de alertas TTS
│   └── bff_docs_agent.py    # Ejemplo 7: Agente de documentación con revisión humana
├── Crewai/
│   └── ai_proposal_crew.py  # Ejemplo 1: Pipeline multiagente de propuesta comercial IA
├── .env                     # Variables de entorno (no commitear)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz:

```env
OPENAI_API_KEY=sk-...
```

---

## LangChain

| Archivo | Técnica | Categoría de negocio |
|---|---|---|
| `resume.py` | LCEL `prompt \| llm` | Productividad técnica |
| `tools.py` | Agente con tools | Operaciones biométricas |
| `cv.py` | `with_structured_output` + Pydantic | Recursos Humanos |
| `clasify_error.py` | Clasificación estructurada con `Literal` | Monitoreo y observabilidad |
| `rag_simple.py` | RAG con `InMemoryVectorStore` | Gestión del conocimiento |
| `agent_tools.py` | Agente con tools de sesión y operaciones | Soporte técnico / Diagnóstico |
| `tts_alert.py` | LCEL para redacción de alertas técnicas | Comunicación de incidentes |
| `bff_docs_agent.py` | Agente de búsqueda y resumen de docs | Soporte técnico / Conocimiento |

### Ejecutar

```bash
cd LangChain
python resume.py
python cv.py
python clasify_error.py
python rag_simple.py
python agent_tools.py
python tts_alert.py
python bff_docs_agent.py
```

---

## LangGraph

| Archivo | Técnica | Categoría de negocio |
|---|---|---|
| `workflow.py` | Grafo lineal con estado `TypedDict` | Procesamiento de eventos |
| `routing.py` | `add_conditional_edges` + router | Resiliencia de plataforma |
| `human.py` | Human-in-the-loop con `input()` | Gobernanza de IA |
| `rag_simple.py` | RAG con routing por contexto | Soporte técnico / Conocimiento |
| `support_workflow.py` | Pipeline lineal de diagnóstico y severidad | Gestión de incidentes |
| `tts_alert.py` | Redacción de borrador + aprobación humana | Comunicación de incidentes |
| `bff_docs_agent.py` | Agente con revisión humana de respuestas | Soporte técnico / Gobernanza |

### Ejecutar

```bash
cd LangGraph
python workflow.py
python routing.py
python human.py
python rag_simple.py
python support_workflow.py
python tts_alert.py
python bff_docs_agent.py
```

---

## CrewAI

| Archivo | Técnica | Categoría de negocio |
|---|---|---|
| `ai_proposal_crew.py` | Pipeline multiagente secuencial (Researcher → Analyst → Writer) | Desarrollo de negocio / Ventas |

### Ejecutar

```bash
cd Crewai
python ai_proposal_crew.py
```

---

## Conceptos clave

**Estado compartido (LangGraph):** Diccionario `TypedDict` que viaja por todos los nodos del grafo. Cada nodo lo lee y enriquece sin destruir la información previa.

**LCEL (LangChain):** Operador `|` que conecta componentes en secuencia — `prompt | llm | parser`.

**RAG:** Patrón donde el LLM responde basándose en documentos recuperados por búsqueda semántica, no en su conocimiento interno.

**`with_structured_output`:** Fuerza al LLM a devolver datos tipados y validados por Pydantic en lugar de texto libre.

**CrewAI:** Framework multiagente donde cada `Agent` tiene un rol, objetivo y contexto. Los agentes colaboran ejecutando `Task`s en secuencia o en paralelo para producir un resultado compuesto.
