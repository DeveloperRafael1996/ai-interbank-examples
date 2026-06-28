from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# ENUNCIADO : LangChain Ejemplo 7 — Redacción de mensajes técnicos con LCEL
# DESCRIPCIÓN: Usa una cadena LCEL (prompt | llm) para generar mensajes
#              profesionales en lenguaje natural a partir de un contexto
#              estructurado. El LLM redacta el mensaje adaptado al tono
#              técnico requerido por el equipo de soporte.
#
# CASO DE USO : Generación automática de alertas técnicas cuando el endpoint
#               TTS recibe un texto vacío, evitando redacción manual y
#               estandarizando la comunicación de incidentes en el BFF.
#
# CATEGORÍA DE NEGOCIO: Comunicación de incidentes / Automatización de soporte
#
# OTROS EJEMPLOS:
#   1. Generar notificaciones automáticas ante fallos de autenticación biométrica.
#   2. Redactar resúmenes de incidentes para el equipo de guardia a partir de logs.
#   3. Producir mensajes de escalamiento para el equipo L2 con contexto del error.
# ============================================================


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


prompt = ChatPromptTemplate.from_template("""
    Redacta un mensaje profesional para el equipo técnico.

    Contexto:
    {context}
""")

chain = prompt | llm

response = chain.invoke({
    "context": """
    Se detectó un error en la generación de audio dinámico.
    El problema está relacionado con un texto vacío enviado al endpoint TTS.
    """
})

print(response.content)