from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore

# ============================================================
# ENUNCIADO : LangChain Ejemplo 5 — RAG simple (Retrieval-Augmented Generation)
# DESCRIPCIÓN: Convierte documentos en vectores semánticos, los almacena en
#              memoria, recupera los más relevantes ante una pregunta y los
#              inyecta como contexto al LLM para generar una respuesta precisa.
#
# CASO DE USO : Asistente de documentación interna que responde preguntas sobre
#               el BFF (endpoints, eventos SSE, pipelines) sin necesidad de
#               buscar manualmente en Confluence o el README.
#
# CATEGORÍA DE NEGOCIO: Gestión del conocimiento / Developer Experience
#
# OTROS EJEMPLOS:
#   1. Chatbot que responde preguntas de onboarding usando el handbook interno de la empresa.
#   2. Asistente legal que busca cláusulas específicas dentro de un contrato de 100 páginas.
#   3. Soporte técnico que responde preguntas de clientes usando la base de conocimiento del producto.
# ============================================================

documents = [
    Document(
        page_content="Para realizar deploy del BFF se debe ejecutar el pipeline de GitHub Actions."
    ),
    Document(
        page_content="El servicio expone el endpoint /api/v1/sessions para crear sesiones."
    ),
    Document(
        page_content="Los eventos SSE soportados son act, action, diagnostic, heartbeat y sse_error."
    )
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = InMemoryVectorStore.from_documents(
    documents=documents,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template("""
    Responde usando solo el siguiente contexto.

    Contexto:
    {context}

    Pregunta:
    {question}
""")

question = "¿Qué eventos SSE soporta el BFF?"

docs = retriever.invoke(question)
context = "\n".join(doc.page_content for doc in docs)

chain = prompt | llm

response = chain.invoke({
    "context": context,
    "question": question
})

print(response.content)

