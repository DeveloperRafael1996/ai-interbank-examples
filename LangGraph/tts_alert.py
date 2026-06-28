from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class ApprovalState(TypedDict):
    context: str
    draft: str
    approved: bool
    final_status: str

def generate_draft(state: ApprovalState) -> ApprovalState:
    draft = (
        "Hola equipo, se identificó un error en la generación de audio dinámico. "
        "El problema parece estar relacionado con un texto vacío enviado al endpoint TTS. "
        "Vamos a validar el origen y aplicar la corrección correspondiente."
    )

    return {
        **state,
        "draft": draft
    }

def human_review(state: ApprovalState) -> ApprovalState:
    print("\n--- REVISIÓN HUMANA ---")
    print(f"Borrador del mensaje:\n{state['draft']}\n")
    respuesta = input("¿Aprobar mensaje? (s/n): ").strip().lower()
    return {
        **state,
        "approved": respuesta == "s"
    }

def send_or_stop(state: ApprovalState) -> ApprovalState:
    if state["approved"]:
        status = "Mensaje aprobado y listo para enviar."
    else:
        status = "Mensaje rechazado. Requiere ajustes."

    return {
        **state,
        "final_status": status
    }

graph = StateGraph(ApprovalState)

graph.add_node("generate_draft", generate_draft)
graph.add_node("human_review", human_review)
graph.add_node("send_or_stop", send_or_stop)

graph.add_edge(START, "generate_draft")
graph.add_edge("generate_draft", "human_review")
graph.add_edge("human_review", "send_or_stop")
graph.add_edge("send_or_stop", END)

app = graph.compile()

result = app.invoke({
    "context": "Error TTS por texto vacío",
    "draft": "",
    "approved": False,
    "final_status": ""
})

print(result["draft"])
print(result["final_status"])

