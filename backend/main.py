import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.config import settings
from backend.database import db
from backend.rag_service import rag_service

app = FastAPI(
    title="RAG Didático API - Teophilo",
    description="API para demonstração visual e didática de um pipeline RAG completo",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    pergunta: str
    top_k: Optional[int] = 5
    min_threshold: Optional[float] = 0.35

class IngestRequest(BaseModel):
    filename: Optional[str] = None

@app.get("/api/status")
def get_status():
    supabase_ok = db.check_connection()
    openrouter_configured = bool(settings.OPENROUTER_API_KEY)
    
    return {
        "status": "online",
        "services": {
            "supabase": "conectado" if supabase_ok else "falha_conexao",
            "openrouter": "configurado" if openrouter_configured else "nao_configurado",
            "fastembed_model": settings.EMBEDDING_MODEL,
            "embedding_dimension": settings.EMBEDDING_DIMENSION
        }
    }

@app.get("/api/available-files")
def list_available_files():
    if not os.path.exists(settings.DOCS_DIR):
        return {"files": []}
    files = [f for f in os.listdir(settings.DOCS_DIR) if f.lower().endswith(".pdf")]
    return {"files": sorted(files)}

@app.get("/api/documents")
def list_documents():
    docs = db.list_documentos()
    return {"documentos": docs}

@app.post("/api/ingest")
def ingest_documents(req: IngestRequest):
    files_to_process = []
    if req.filename:
        files_to_process = [req.filename]
    else:
        if os.path.exists(settings.DOCS_DIR):
            files_to_process = [f for f in os.listdir(settings.DOCS_DIR) if f.lower().endswith(".pdf")]
    
    if not files_to_process:
        raise HTTPException(status_code=400, detail="Nenhum arquivo PDF encontrado para ingestão.")

    results = []
    for fn in files_to_process:
        try:
            res = rag_service.process_and_ingest_document(fn)
            results.append(res)
        except Exception as e:
            results.append({
                "nome_arquivo": fn,
                "status": "ERRO",
                "erro": str(e)
            })

    return {
        "total_processados": len(results),
        "detalhes": results
    }

@app.post("/api/query")
def execute_query(req: QueryRequest):
    if not req.pergunta.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    try:
        resultado = rag_service.query_rag(
            question=req.pergunta,
            top_k=req.top_k or 5,
            min_threshold=req.min_threshold or 0.35
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar consulta: {str(e)}")

@app.delete("/api/documents")
def clear_documents():
    try:
        db.clear_all()
        return {"mensagem": "Todos os documentos e chunks foram removidos com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar banco: {str(e)}")
