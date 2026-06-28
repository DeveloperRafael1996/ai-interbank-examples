import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()

# ============================================================
# ENUNCIADO : LangChain Ejemplo 2 — Agente con herramientas (Tools)
# DESCRIPCIÓN: Crea un agente LLM que puede llamar funciones Python como
#              herramientas. El LLM decide cuándo y cómo invocar cada tool
#              según la pregunta del usuario.
#
# CASO DE USO : Asistente interno que recibe una pregunta en lenguaje natural
#               ("¿qué pasó con la operación op_123?") y consulta automáticamente
#               la API de operaciones para devolver el estado real.
#
# CATEGORÍA DE NEGOCIO: Operaciones biométricas / Soporte técnico interno
#
# OTROS EJEMPLOS:
#   1. Agente que consulta métricas de Datadog y explica anomalías en lenguaje natural.
#   2. Asistente de soporte que busca el historial de sesiones de un usuario por ID.
#   3. Bot que recibe una alerta de monitoreo y crea automáticamente un ticket en Jira.
# ============================================================

def get_operation_status(operation_id: str) -> str:
    """Obtiene el estado de una operación biométrica."""
    fake_db = {
        "op_123": "FAILED: CameraPermissionDenied",
        "op_456": "SUCCESS",
    }
    return fake_db.get(operation_id, "NOT_FOUND")

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[get_operation_status],
    system_prompt="Eres un asistente que ayuda a revisar operaciones biométricas."
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Consulta la operación op_123 y dime qué ocurrió."
        }
    ]
})

print(response["messages"][-1].content)