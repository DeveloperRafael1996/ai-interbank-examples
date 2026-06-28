from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

def search_docs(query: str) -> str:
    """Busca información en documentación técnica."""
    return "El BFF maneja eventos SSE y diagnósticos de operaciones."

def create_summary(text: str) -> str:
    """Crea un resumen breve."""
    return f"Resumen técnico: {text}"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


agent = create_agent(
    model=llm,
    tools=[search_docs, create_summary],
    system_prompt="Eres un agente técnico que investiga y resume documentación."
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Investiga cómo funciona el BFF y dame un resumen."
        }
    ]
})

print(response["messages"][-1].content)