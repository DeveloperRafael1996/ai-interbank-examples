from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


# ============================================================
# ENUNCIADO : LangChain Ejemplo 6 — Agente con herramientas de diagnóstico biométrico
# DESCRIPCIÓN: Construye un agente que expone funciones Python como herramientas
#              invocables. El LLM decide qué tool llamar según la pregunta del
#              usuario, combinando el resultado de múltiples herramientas para
#              dar una respuesta coherente en lenguaje natural.
#
# CASO DE USO : Asistente de soporte técnico que consulta el estado de sesiones
#               biométricas y el historial de errores de operaciones, sin que el
#               operador necesite conocer los IDs internos o las APIs del BFF.
#
# CATEGORÍA DE NEGOCIO: Soporte técnico / Diagnóstico operacional
#
# OTROS EJEMPLOS:
#   1. Agente que consulta saldo, movimientos y límites de una cuenta bancaria.
#   2. Bot de onboarding que verifica el estado KYC del cliente y dispara acciones.
#   3. Asistente de fraude que combina herramientas de scoring y bloqueo de tarjeta.
# ============================================================


def get_session_status(session_id: str) -> str:
    """Obtiene el estado de una sesión biométrica."""
    sessions = {
        "session_123": "ACTIVE",
        "session_456": "EXPIRED"
    }
    return sessions.get(session_id, "NOT_FOUND")

def get_operation_error(operation_id: str) -> str:
    """Obtiene el último error de una operación."""
    operations = {
        "op_123": "CameraPermissionDenied",
        "op_456": "CdnLoadingResourcesError"
    }
    return operations.get(operation_id, "NO_ERROR_FOUND")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_agent(
    model=llm,
    tools=[get_session_status, get_operation_error],
    system_prompt="Eres un asistente técnico para soporte de operaciones biométricas."
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Revisa la session session_123 y dime cuál fue el problema."
        }
    ]
})

print(response["messages"][-1].content)