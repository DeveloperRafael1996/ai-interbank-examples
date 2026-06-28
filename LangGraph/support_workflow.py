from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ============================================================
# ENUNCIADO : LangGraph Ejemplo 5 — Pipeline de diagnóstico de operaciones
# DESCRIPCIÓN: Implementa un grafo lineal de tres nodos que recupera el error
#              asociado a una operación, evalúa su severidad (HIGH/MEDIUM) y
#              construye un mensaje final de diagnóstico con toda la información
#              consolidada en el estado compartido.
#
# CASO DE USO : Soporte técnico del BFF que, dado un operation_id, determina
#               automáticamente qué falló y qué tan crítico es, para priorizar
#               la atención de incidentes biométricos en producción.
#
# CATEGORÍA DE NEGOCIO: Gestión de incidentes / Soporte operacional
#
# OTROS EJEMPLOS:
#   1. Pipeline que recupera una transacción, evalúa riesgo de fraude y genera alerta.
#   2. Flujo que obtiene el estado de un cliente, calcula su scoring y arma un reporte.
#   3. Diagnóstico automático de fallos en pasarelas de pago con nivel de urgencia.
# ============================================================


class SupportState(TypedDict):
    operation_id: str
    error_code: str
    severity: str
    final_message: str

def get_operation_error(state: SupportState) -> SupportState:
    fake_operations = {
        "op_123": "CameraPermissionDenied",
        "op_456": "CdnLoadingResourcesError",
        "op_789": "SseConnectionError"
    }

    return {
        **state,
        "error_code": fake_operations.get(state["operation_id"], "UNKNOWN")
    }

def evaluate_severity(state: SupportState) -> SupportState:
    high_severity_errors = [
        "SseConnectionError",
        "CdnLoadingResourcesError"
    ]

    severity = "HIGH" if state["error_code"] in high_severity_errors else "MEDIUM"

    return {
        **state,
        "severity": severity
    }

def build_final_message(state: SupportState) -> SupportState:
    return {
        **state,
        "final_message": (
            f"La operación {state['operation_id']} falló con "
            f"{state['error_code']}. Severidad: {state['severity']}."
        )
    }

graph = StateGraph(SupportState)

graph.add_node("get_operation_error", get_operation_error)
graph.add_node("evaluate_severity", evaluate_severity)
graph.add_node("build_final_message", build_final_message)

graph.add_edge(START, "get_operation_error")
graph.add_edge("get_operation_error", "evaluate_severity")
graph.add_edge("evaluate_severity", "build_final_message")
graph.add_edge("build_final_message", END)

app = graph.compile()

result = app.invoke({
    "operation_id": "op_123",
    "error_code": "",
    "severity": "",
    "final_message": ""
})

print(result["final_message"])