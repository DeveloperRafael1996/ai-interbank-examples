import os
from dotenv import load_dotenv

from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

load_dotenv()

# ============================================================
# ENUNCIADO : LangChain Ejemplo 3 — Extracción estructurada con Pydantic
# DESCRIPCIÓN: Usa with_structured_output() para instruir al LLM a devolver
#              datos tipados y validados. El modelo Pydantic define el contrato
#              exacto que debe cumplir la respuesta.
#
# CASO DE USO : Procesar CVs recibidos en texto libre y extraer automáticamente
#               nombre, seniority, skills y años de experiencia para poblar
#               una base de datos de candidatos sin intervención manual.
#
# CATEGORÍA DE NEGOCIO: Recursos Humanos / Automatización de procesos
#
# OTROS EJEMPLOS:
#   1. Extraer campos clave (monto, fecha, partes) de contratos legales en PDF.
#   2. Parsear mensajes de error de logs y convertirlos en tickets estructurados.
#   3. Leer respuestas de formularios de clientes y mapearlos a un payload JSON de CRM.
# ============================================================

class CandidateProfile(BaseModel):
    name: str = Field(description="Nombre del candidato")
    seniority: str = Field(description="Nivel: junior, semi senior, senior o lead")
    skills: List[str] = Field(description="Lista de habilidades técnicas")
    years_experience: int = Field(description="Años de experiencia aproximados")


llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0
)

structured_llm = llm.with_structured_output(CandidateProfile)

cv_text = """
Rafael Guevara es backend engineer con experiencia en Python, FastAPI,
AWS, Kubernetes, LangChain, RAG y arquitectura de microservicios.
Tiene más de 8 años de experiencia construyendo soluciones productivas.
"""

profile = structured_llm.invoke(cv_text)

print(profile)
print(profile.skills)


