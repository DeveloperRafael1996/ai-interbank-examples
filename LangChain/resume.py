import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ============================================================
# ENUNCIADO : LangChain Ejemplo 1 — Cadena de resumen simple (LCEL)
# DESCRIPCIÓN: Construye una cadena prompt | llm usando LangChain Expression
#              Language (LCEL). Recibe un texto libre y devuelve un resumen
#              estructurado en 3 puntos usando un LLM.
#
# CASO DE USO : Resumir automáticamente las notas de un post-mortem técnico
#               para incluirlas en un reporte ejecutivo sin perder los puntos clave.
#
# CATEGORÍA DE NEGOCIO: Productividad técnica / Comunicación interna
#
# OTROS EJEMPLOS:
#   1. Resumir un PR largo de GitHub para enviarlo al equipo por Slack.
#   2. Condensar un log de errores de producción en un párrafo para el ticket de soporte.
#   3. Generar un resumen ejecutivo de la documentación de una nueva API para onboarding.
# ============================================================

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente técnico experto en backend."),
    ("user", "Resume este texto en 3 puntos:\n\n{texto}")
])

# Conecta los dos componentes en secuencia:
chain = prompt | llm 

response = chain.invoke({
    "texto": """
    Se implementó un nuevo flujo de generación de audio dinámico.
    Ahora se usa el archivo es.json del CDN y se evita una inferencia adicional
    para traducción, reduciendo el tiempo de respuesta de 5 segundos a 2 segundos.
    """
})

print(response)