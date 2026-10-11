from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from backend.config import settings

class SupabaseManager:
    def __init__(self):
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY são obrigatórios.")
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    def check_connection(self) -> bool:
        try:
            # Query mínima
            res = self.client.table("documentos").select("id").limit(1).execute()
            return True
        except Exception:
            return False

    def insert_documento(self, doc_data: Dict[str, Any]) -> Dict[str, Any]:
        res = self.client.table("documentos").insert(doc_data).execute()
        if res.data and len(res.data) > 0:
            return res.data[0]
        return {}

    def insert_chunks(self, chunks_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not chunks_data:
            return []
        res = self.client.table("documento_chunks").insert(chunks_data).execute()
        return res.data or []

    def list_documentos(self) -> List[Dict[str, Any]]:
        res = self.client.table("documentos").select("*").order("criado_em", desc=True).execute()
        return res.data or []

    def get_ingestion_summary(self) -> Dict[str, Any]:
        """Conta documentos com chunks gravados e o total de vetores no índice."""
        documents = self.client.table("documentos").select("id,nome_arquivo").execute().data or []
        indexed_names = set()
        total_chunks = 0

        # Fazemos contagens pequenas, sem baixar os vetores do Supabase.
        for document in documents:
            result = (
                self.client.table("documento_chunks")
                .select("id", count="exact", head=True)
                .eq("documento_id", document["id"])
                .execute()
            )
            chunk_count = result.count or 0
            if chunk_count:
                indexed_names.add(document["nome_arquivo"])
                total_chunks += chunk_count

        return {
            "arquivos_indexados": sorted(indexed_names),
            "total_documentos_vetorizados": len(indexed_names),
            "total_chunks_vetorizados": total_chunks,
        }

    def delete_documento(self, doc_id: str):
        # Chunks são apagados ou referenciados
        self.client.table("documento_chunks").delete().eq("documento_id", doc_id).execute()
        self.client.table("documentos").delete().eq("id", doc_id).execute()

    def clear_all(self):
        self.client.table("documento_chunks").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        self.client.table("documentos").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()

    def match_chunks(self, query_embedding: List[float], match_count: int = 5, match_threshold: float = 0.0) -> List[Dict[str, Any]]:
        payload = {
            "query_embedding": query_embedding,
            "match_threshold": match_threshold,
            "match_count": match_count
        }
        res = self.client.rpc("match_documento_chunks", payload).execute()
        return res.data or []

db = SupabaseManager()
