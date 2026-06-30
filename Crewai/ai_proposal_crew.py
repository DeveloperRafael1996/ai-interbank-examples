from crewai import Agent, Task, Crew, Process


# ============================================================
# ENUNCIADO : CrewAI Ejemplo 1 — Pipeline multiagente de propuesta comercial IA
# DESCRIPCIÓN: Define un equipo de tres agentes especializados (Researcher,
#              Analyst, Writer) que colaboran en secuencia. Cada agente recibe
#              el output del anterior como contexto y produce un resultado que
#              alimenta al siguiente, hasta generar una propuesta comercial final.
#
# CASO DE USO : Automatización del ciclo completo de preventa: investigar el
#               mercado objetivo (restaurantes, hoteles, inmobiliarias en Perú),
#               identificar oportunidades SaaS viables y redactar una propuesta
#               lista para enviar al cliente, sin intervención manual.
#
# CATEGORÍA DE NEGOCIO: Desarrollo de negocio / Automatización de ventas
#
# OTROS EJEMPLOS:
#   1. Crew de due diligence: investigador + analista financiero + redactor de informe.
#   2. Crew de soporte: agente de diagnóstico + agente de solución + agente de respuesta.
#   3. Crew de contenido: investigador de tendencias + redactor + editor SEO.
# ============================================================


researcher = Agent(
    role="AI Market Researcher",
    goal="Investigar oportunidades de automatización con IA para empresas",
    backstory=(
        "Eres un investigador experto en negocios, IA generativa, "
        "automatización y productos SaaS."
    ),
    verbose=True
)

analyst = Agent(
    role="Business Analyst",
    goal="Convertir la investigación en oportunidades de producto",
    backstory=(
        "Eres un analista de negocio que identifica problemas reales, "
        "clientes objetivo y propuestas de valor."
    ),
    verbose=True
)

writer = Agent(
    role="Proposal Writer",
    goal="Redactar una propuesta comercial clara y persuasiva",
    backstory=(
        "Eres experto escribiendo propuestas para clientes empresariales."
    ),
    verbose=True
)

research_task = Task(
    description=(
        "Investiga oportunidades para implementar un asistente de voz con IA "
        "para restaurantes, hoteles e inmobiliarias en Perú."
    ),
    expected_output="Lista de oportunidades, dolores del cliente y posibles soluciones.",
    agent=researcher
)

analysis_task = Task(
    description=(
        "Analiza la investigación y define 3 productos SaaS viables "
        "que se puedan implementar con IA."
    ),
    expected_output="3 ideas de producto con cliente objetivo, problema y solución.",
    agent=analyst
)

proposal_task = Task(
    description=(
        "Redacta una propuesta comercial corta para presentar el producto "
        "a una empresa interesada."
    ),
    expected_output="Propuesta comercial lista para enviar.",
    agent=writer
)

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, proposal_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
print(result)