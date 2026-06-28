from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ============================================================
# ENUNCIADO : LangGraph Ejemplo 2 — Routing condicional
# DESCRIPCIÓN: Usa add_conditional_edges() para bifurcar el flujo según el
#              valor del estado. Una función router decide a qué nodo ir,
#              permitiendo ejecutar lógica distinta para cada caso.
#
# CASO DE USO : Sistema de manejo de errores del BFF que detecta el tipo de
#               falla (cámara, CDN, desconocido) y ejecuta la acción correcta
#               para cada uno sin mezclar la lógica en un solo bloque if/else.
#
# CATEGORÍA DE NEGOCIO: Resiliencia de plataforma / Manejo de errores
#
# OTROS EJEMPLOS:
#   1. Enrutar transacciones bancarias según el tipo (transferencia, pago, recarga) a flujos distintos.
#   2. Clasificar solicitudes de soporte y asignarlas al equipo correcto (L1, L2, L3).
#   3. Dirigir resultados de un análisis de fraude a revisión manual o aprobación automática.
# ============================================================

class State(TypedDict):
    error_code: str
    action: str
    message: str


def analyze_error(state: State) -> State:
    error_code = state["error_code"]

    if error_code == "CameraPermissionDenied":
        action = "ASK_CAMERA_PERMISSION"
    elif error_code == "CdnLoadingResourcesError":
        action = "RETRY_CDN"
    else:
        action = "ESCALATE"

    return {
        **state,
        "action": action
    }

def ask_camera_permission(state: State) -> State:
    return {
        **state,
        "message": "Solicita al usuario habilitar permisos de cámara."
    }

def retry_cdn(state: State) -> State:
    return {
        **state,
        "message": "Reintenta la carga de recursos desde el CDN."
    }

def escalate(state: State) -> State:
    return {
        **state,
        "message": "Escalar el caso al equipo técnico."
    }

def router(state: State) -> str:
    if state["action"] == "ASK_CAMERA_PERMISSION":
        return "ask_camera_permission"

    if state["action"] == "RETRY_CDN":
        return "retry_cdn"

    return "escalate"

graph = StateGraph(State)

graph.add_node("analyze_error", analyze_error)
graph.add_node("ask_camera_permission", ask_camera_permission)
graph.add_node("retry_cdn", retry_cdn)
graph.add_node("escalate", escalate)

graph.add_edge(START, "analyze_error")

graph.add_conditional_edges(
    "analyze_error",
    router,
    {
        "ask_camera_permission": "ask_camera_permission",
        "retry_cdn": "retry_cdn",
        "escalate": "escalate"
    }
)

graph.add_edge("ask_camera_permission", END)
graph.add_edge("retry_cdn", END)
graph.add_edge("escalate", END)

app = graph.compile()

response = app.invoke({
    "error_code": "CameraPermissionDenied",
    "action": "",
    "message": ""
})

print(response["message"])