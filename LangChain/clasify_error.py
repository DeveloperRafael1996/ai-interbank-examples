import time
from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


# ============================================================
# ENUNCIADO : LangChain Ejemplo 4 — Clasificación estructurada de errores
# DESCRIPCIÓN: Usa with_structured_output() con Literal para forzar al LLM
#              a clasificar un error técnico en categorías predefinidas,
#              asignar severidad y recomendar una acción concreta.
#
# CASO DE USO : Procesar automáticamente logs de errores del BFF y clasificarlos
#               para priorizar cuáles requieren intervención inmediata del equipo
#               de guardia vs. cuáles pueden resolverse solos.
#
# CATEGORÍA DE NEGOCIO: Monitoreo y observabilidad / Operaciones de plataforma
#
# OTROS EJEMPLOS:
#   1. Clasificar errores de pagos (timeout, fondos insuficientes, fraude) para enrutar al equipo correcto.
#   2. Categorizar feedback de usuarios en bugs, mejoras o dudas para el equipo de producto.
#   3. Analizar excepciones de microservicios y asignar severidad automática en el sistema de alertas.
# ============================================================
class ErrorClassification(BaseModel):
    category: Literal[
        "CAMERA",
        "CDN",
        "SSE",
        "VALIDATION",
        "UNKNOWN"
    ] = Field(description="Categoría principal del error")
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    recommendation: str


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

classifier = llm.with_structured_output(ErrorClassification)

error_log = """
2026-06-24 WARNING response POST /api/v1/tts/synthesize 400
VALIDATION_ERROR: text should have at least 1 character
"""

start = time.time()
result = classifier.invoke(
    f"Clasifica este error técnico y recomienda una acción:\n\n{error_log}"
)
elapsed = time.time() - start

print(result.category)
print(result.severity)
print(result.recommendation)
print(f"\nTiempo de respuesta: {elapsed:.2f}s")
