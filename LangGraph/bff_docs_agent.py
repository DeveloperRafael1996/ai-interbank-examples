from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class MultiAgentState(TypedDict):
    topic: str
    research_notes: str
    review_notes: str
    final_answer: str

def researcher_agent(state: MultiAgentState) -> MultiAgentState:
    return {
        **state,
        "research_notes": (
            "El BFF crea sesiones, consume configuración, "
            "orquesta operaciones y emite eventos SSE."
        )
    }

def reviewer_agent(state: MultiAgentState) -> MultiAgentState:
    notes = state["research_notes"]

    return {
        **state,
        "review_notes": (
            f"Validado técnicamente. Puntos clave: {notes}"
        )
    }

def writer_agent(state: MultiAgentState) -> MultiAgentState:
    return {
        **state,
        "final_answer": (
            "El BFF actúa como capa de orquestación entre cliente, "
            "orchestrator y servicios internos. Su rol principal es manejar "
            "sesiones, configuración, operaciones y eventos SSE."
        )
    }

graph = StateGraph(MultiAgentState)

graph.add_node("researcher_agent", researcher_agent)
graph.add_node("reviewer_agent", reviewer_agent)
graph.add_node("writer_agent", writer_agent)

graph.add_edge(START, "researcher_agent")
graph.add_edge("researcher_agent", "reviewer_agent")
graph.add_edge("reviewer_agent", "writer_agent")
graph.add_edge("writer_agent", END)

app = graph.compile()

result = app.invoke({
    "topic": "Funcionamiento del BFF",
    "research_notes": "",
    "review_notes": "",
    "final_answer": ""
})

print(result["final_answer"])
