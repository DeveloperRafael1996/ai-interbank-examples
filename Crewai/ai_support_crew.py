from crewai import Agent, Task, Crew, Process

log_analyst = Agent(
    role="Log Analyst",
    goal="Analizar logs técnicos y encontrar la causa raíz",
    backstory="Eres experto revisando logs de APIs, BFF, SSE y servicios internos.",
    verbose=True
)

error_classifier = Agent(
    role="Error Classifier",
    goal="Clasificar errores técnicos según su origen",
    backstory="Conoces errores de cámara, CDN, SSE, validación y permisos.",
    verbose=True
)

support_writer = Agent(
    role="Support Writer",
    goal="Redactar una respuesta clara para el equipo o cliente",
    backstory="Eres experto explicando problemas técnicos de forma simple.",
    verbose=True
)

log_task = Task(
    description="""
    Analiza este log:

    POST /api/v1/tts/synthesize 400
    VALIDATION_ERROR: text should have at least 1 character

    Identifica la causa probable.
    """,
    expected_output="Causa raíz probable del error.",
    agent=log_analyst
)

classification_task = Task(
    description="""
    Clasifica el error según estas categorías:
    VALIDATION, CAMERA, CDN, SSE, ORCHESTRATOR, UNKNOWN.
    """,
    expected_output="Categoría del error y severidad.",
    agent=error_classifier
)

response_task = Task(
    description="""
    Redacta una respuesta profesional para el equipo técnico
    explicando el problema y la acción recomendada.
    """,
    expected_output="Mensaje profesional listo para enviar.",
    agent=support_writer
)

crew = Crew(
    agents=[log_analyst, error_classifier, support_writer],
    tasks=[log_task, classification_task, response_task],
    process=Process.sequential
)

result = crew.kickoff()

print(result)


