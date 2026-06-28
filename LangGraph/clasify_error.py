from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class ErrorState(TypedDict):
    error_code: str
    category: str
    action: str
    response: str

def classify_error(state: ErrorState) -> ErrorState:
    error_code = state["error_code"]

    if error_code == "CameraPermissionDenied":
        category = "CAMERA"
    elif error_code == "CdnLoadingResourcesError":
        category = "CDN"
    elif error_code == "SseConnectionError":
        category = "SSE"
    else:
        category = "UNKNOWN"

    return {
        **state,
        "category": category
    }

def decide_action(state: ErrorState) -> ErrorState:
    category = state["category"]

    actions = {
        "CAMERA": "ASK_PERMISSION",
        "CDN": "RETRY_RESOURCE_LOADING",
        "SSE": "RECONNECT_STREAM",
        "UNKNOWN": "ESCALATE"
    }

    return {
        **state,
        "action": actions.get(category, "ESCALATE")
    }

def build_response(state: ErrorState) -> ErrorState:
    action = state["action"]

    messages = {
        "ASK_PERMISSION": "Solicita al usuario habilitar la cámara.",
        "RETRY_RESOURCE_LOADING": "Reintenta la carga de recursos desde el CDN.",
        "RECONNECT_STREAM": "Reconecta el canal SSE.",
        "ESCALATE": "Escala el caso al equipo técnico."
    }

    return {
        **state,
        "response": messages[action]
    }

graph = StateGraph(ErrorState)

graph.add_node("classify_error", classify_error)
graph.add_node("decide_action", decide_action)
graph.add_node("build_response", build_response)

graph.add_edge(START, "classify_error")
graph.add_edge("classify_error", "decide_action")
graph.add_edge("decide_action", "build_response")
graph.add_edge("build_response", END)

app = graph.compile()

result = app.invoke({
    "error_code": "CameraPermissionDenied",
    "category": "",
    "action": "",
    "response": ""
})

print(result["category"])  # Output: CAMERA
print(result["action"])    # Output: ASK_PERMISSION
print(result["response"])  # Output: Solicita al usuario habilitar la cámara.

# Error → clasificar → decidir acción → construir respuesta
# LangChain = clasificación inteligente
# LangGraph = flujo completo de decisión