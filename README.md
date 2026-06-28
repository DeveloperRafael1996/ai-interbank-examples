# AI Interbank — LangChain & LangGraph Examples

Colección de ejemplos prácticos de LangChain y LangGraph aplicados a casos de uso del contexto bancario/biométrico.

---

## Estructura del proyecto

```
AI_Interbank/
├── LangChain/
│   ├── resume.py          # Ejemplo 1: Cadena de resumen simple (LCEL)
│   ├── tools.py           # Ejemplo 2: Agente con herramientas (Tools)
│   ├── cv.py              # Ejemplo 3: Extracción estructurada con Pydantic
│   ├── clasify_error.py   # Ejemplo 4: Clasificación estructurada de errores
│   └── rag_simple.py      # Ejemplo 5: RAG simple (búsqueda semántica)
├── LangGraph/
│   ├── workflow.py        # Ejemplo 1: Workflow simple con estado compartido
│   ├── routing.py         # Ejemplo 2: Routing condicional
│   └── human.py           # Ejemplo 3: Human-in-the-loop (revisión humana)
├── .env                   # Variables de entorno (no commitear)
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

### Ejecutar

```bash
cd LangChain
python resume.py
python cv.py
python clasify_error.py
python rag_simple.py
```

---

## LangGraph

| Archivo | Técnica | Categoría de negocio |
|---|---|---|
| `workflow.py` | Grafo lineal con estado `TypedDict` | Procesamiento de eventos |
| `routing.py` | `add_conditional_edges` + router | Resiliencia de plataforma |
| `human.py` | Human-in-the-loop con `input()` | Gobernanza de IA |

### Ejecutar

```bash
cd LangGraph
python workflow.py
python routing.py
python human.py
```

---

## Conceptos clave

**Estado compartido (LangGraph):** Diccionario `TypedDict` que viaja por todos los nodos del grafo. Cada nodo lo lee y enriquece sin destruir la información previa.

**LCEL (LangChain):** Operador `|` que conecta componentes en secuencia — `prompt | llm | parser`.

**RAG:** Patrón donde el LLM responde basándose en documentos recuperados por búsqueda semántica, no en su conocimiento interno.

**`with_structured_output`:** Fuerza al LLM a devolver datos tipados y validados por Pydantic en lugar de texto libre.
