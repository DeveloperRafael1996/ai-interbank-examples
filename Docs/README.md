# Tipos de Agentes de IA

Este documento resume los tipos de agentes más usados en frameworks como LlamaIndex, LangChain, LangGraph y CrewAI, con ejemplos aplicados al dominio bancario de este repositorio.

## 1. Function-Calling / Tool-Calling Agent (el más usado hoy)

El LLM decide qué función/tool llamar usando la API nativa de function calling (OpenAI, Anthropic, etc.). Es el patrón usado en [LlamaIndex/agente_orquestador_banco.py](../LlamaIndex/agente_orquestador_banco.py).

- ✅ Rápido, confiable, bajo costo en tokens.
- ❌ Poco transparente (no se ve el razonamiento intermedio).

## 2. ReAct Agent (Reasoning + Acting)

Razonamiento explícito en texto (`Thought → Action → Observation`) antes de responder.

- ✅ Auditable, bueno para debugging y tareas complejas multi-paso.
- ❌ Más lento y consume más tokens.

## 3. RAG Agent (Retrieval-Augmented Generation)

No es un "agente" puro sino un patrón de recuperación + generación. Se combina frecuentemente con los anteriores como una tool más.

## 4. Router Agent

Un LLM (o clasificador) decide a qué sub-agente o cadena enviar la consulta (ej. "productos" vs "riesgo" vs "soporte"). Muy usado como capa de entrada en sistemas con múltiples dominios.

## 5. Multi-Agent / Supervisor Pattern

Varios agentes especializados (cada uno con su rol y tools) coordinados por un agente supervisor/orquestador. Ideal para flujos bancarios con un agente de productos, otro de riesgo, otro de compliance, coordinados por un supervisor.

## 6. Plan-and-Execute Agent

El LLM primero genera un plan completo de pasos, luego los ejecuta uno a uno (a diferencia de ReAct que decide paso a paso). Útil para tareas largas y complejas donde replanificar es costoso.

---

## Ejemplos

### Ejemplo 1 — Function-Calling Agent (razonamiento implícito)

```python
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.openai import OpenAI

def consultar_productos_banco(question: str) -> str:
    return "El préstamo personal requiere DNI, ingresos demostrables y evaluación crediticia."

def evaluar_riesgo_cliente(question: str) -> str:
    return "Riesgo medio. Se recomienda validación adicional de ingresos."

workflow = AgentWorkflow.from_tools_or_functions(
    tools_or_functions=[consultar_productos_banco, evaluar_riesgo_cliente],
    llm=OpenAI(model="gpt-4o-mini"),
    system_prompt="""
        Eres un orquestador bancario.
        Usa las herramientas disponibles para responder con criterio.
    """
)

response = workflow.run(
    user_msg="¿Este cliente puede acceder a un préstamo personal?"
)
print(response)
```

El modelo elige la tool internamente (vía function calling) sin mostrar el razonamiento como texto.

### Ejemplo 2 — ReAct Agent (razonamiento explícito)

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

def consultar_productos_banco(question: str) -> str:
    return "El préstamo personal requiere DNI, ingresos demostrables y evaluación crediticia."

def evaluar_riesgo_cliente(question: str) -> str:
    return "Riesgo medio. Se recomienda validación adicional de ingresos."

tools = [
    FunctionTool.from_defaults(fn=consultar_productos_banco),
    FunctionTool.from_defaults(fn=evaluar_riesgo_cliente),
]

agent = ReActAgent.from_tools(tools, llm=OpenAI(model="gpt-4o-mini"), verbose=True)

response = agent.chat("¿Este cliente puede acceder a un préstamo personal?")
print(response)
```

Con `verbose=True`, el agente imprime su razonamiento paso a paso:

```
Thought: Necesito saber los requisitos del préstamo personal.
Action: consultar_productos_banco
Action Input: {"question": "requisitos préstamo personal"}
Observation: El préstamo personal requiere DNI, ingresos demostrables...
Thought: Ahora necesito evaluar el riesgo del cliente.
Action: evaluar_riesgo_cliente
Action Input: {"question": "riesgo cliente"}
Observation: Riesgo medio. Se recomienda validación adicional...
Thought: Ya tengo suficiente información para responder.
Answer: Sí, puede acceder, pero se recomienda validar ingresos por riesgo medio.
```

---

## Resumen comparativo

| Tipo de agente | Razonamiento visible | Velocidad | Uso típico |
|---|---|---|---|
| Function-Calling | No | Rápido | Producción |
| ReAct | Sí | Lento | Debug / prototipo |
| RAG | N/A | Media | Consulta de documentos |
| Router | No | Rápido | Clasificación de intención |
| Multi-Agent / Supervisor | Depende | Media | Flujos complejos multi-dominio |
| Plan-and-Execute | Sí (plan inicial) | Media | Tareas largas multi-paso |
