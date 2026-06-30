from crewai import Agent, Task, Crew, Process


# ============================================================
# ENUNCIADO : CrewAI Ejemplo 2 — Pipeline multiagente para generación de posts LinkedIn
# DESCRIPCIÓN: Define un equipo de tres agentes (Researcher, Writer, Reviewer)
#              que colaboran en secuencia para producir contenido técnico
#              optimizado. El researcher propone temas, el writer redacta el
#              post y el reviewer lo refina para maximizar su impacto.
#
# CASO DE USO : Automatización de la creación de contenido técnico para
#               LinkedIn sobre AI Engineering, LangGraph, CrewAI y RAG,
#               reduciendo el tiempo de producción de posts sin sacrificar
#               calidad ni tono profesional.
#
# CATEGORÍA DE NEGOCIO: Marketing de contenido / Automatización editorial
#
# OTROS EJEMPLOS:
#   1. Crew para generar newsletters técnicas semanales de forma automática.
#   2. Pipeline de contenido para Twitter/X con investigador + redactor + editor de hilos.
#   3. Generación automatizada de artículos de blog con SEO integrado.
# ============================================================


trend_researcher = Agent(
    role="AI Trend Researcher",
    goal="Identificar temas interesantes sobre AI Engineering",
    backstory="Eres experto en tendencias de IA, agentes, RAG y automatización.",
    verbose=True
)

technical_writer = Agent(
    role="Technical Content Writer",
    goal="Crear posts técnicos cortos para LinkedIn",
    backstory="Escribes contenido técnico claro, directo y con impacto.",
    verbose=True
)

reviewer = Agent(
    role="LinkedIn Copy Reviewer",
    goal="Mejorar el post para hacerlo más claro y atractivo",
    backstory="Eres experto en copywriting para LinkedIn técnico.",
    verbose=True
)

research_task = Task(
    description=(
        "Propón 5 temas de LinkedIn sobre AI Engineering, LangGraph, "
        "CrewAI, RAG y agentes."
    ),
    expected_output="Lista de 5 temas con enfoque técnico.",
    agent=trend_researcher
)

write_task = Task(
    description=(
        "Elige el mejor tema y redacta un post corto para LinkedIn "
        "con tono profesional y cercano."
    ),
    expected_output="Post de LinkedIn listo para publicar.",
    agent=technical_writer
)

review_task = Task(
    description=(
        "Mejora el post para que tenga más impacto, claridad y gancho inicial."
    ),
    expected_output="Versión final del post optimizada.",
    agent=reviewer
)

crew = Crew(
    agents=[trend_researcher, technical_writer, reviewer],
    tasks=[research_task, write_task, review_task],
    process=Process.sequential
)

result = crew.kickoff()

print(result)