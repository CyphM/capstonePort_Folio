from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.hortifrut_knowledge import HORTIFRUT_KNOWLEDGE
from app.agents.metadata_agent import HortifrutMetadataAgent
from app.models.query_models import QueryRequest, QueryResponse, DataOwnerResponse

app = FastAPI(
    title="Hortifrut Metadata Chatbot API",
    description="API para consultar metadatos de Hortifrut",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar agente
agent = HortifrutMetadataAgent(HORTIFRUT_KNOWLEDGE)

@app.get("/")
async def root():
    return {
        "message": "🤖 Hortifrut Metadata Chatbot API", 
        "version": "1.0.0",
        "endpoints": ["/api/data-owner/{area}", "/api/search/{query}", "/api/owners"]
    }

@app.get("/api/data-owner/{area}", response_model=DataOwnerResponse)
async def get_data_owner(area: str):
    result = agent.find_data_owner(area)
    if result:
        return DataOwnerResponse(
            owner=result["owner"],
            areas=result["areas"],
            systems=result["systems"],
            status="success"
        )
    return DataOwnerResponse(
        owner="",
        areas=[],
        systems=[],
        status="error"
    )

@app.get("/api/search/{query}")
async def search_metadata(query: str):
    results = agent.search_all_areas(query)
    return {
        "query": query, 
        "results": results,
        "count": len(results)
    }

@app.get("/api/owners")
async def get_all_owners():
    owners = agent.get_all_data_owners()
    return {"owners": owners}

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    # Aquí irá la lógica de NLP más avanzada
    simple_response = f"Procesando tu pregunta: '{request.question}'. Esta funcionalidad estará disponible pronto."
    
    return QueryResponse(
        answer=simple_response,
        sources=["knowledge_base"],
        confidence=0.8
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)