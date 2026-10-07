import sys
from backend.rag_service import rag_service
from backend.database import db

print("=== 1. Limpando base anterior para teste limpo ===")
try:
    db.clear_all()
    print("Base limpa.")
except Exception as e:
    print(f"Erro ao limpar: {e}")

print("\n=== 2. Testando Ingestão de NF_1042_TechByte.pdf ===")
res1 = rag_service.process_and_ingest_document("NF_1042_TechByte.pdf")
print(f"Status: {res1['status']}, Chunks gerados: {res1['total_chunks']}")
print(f"Campos estruturados extraídos: {res1['dados_estruturados']['campos_preenchidos']}/{res1['dados_estruturados']['total_campos']}")

print("\n=== 3. Ingerindo as outras 3 notas fiscais ===")
for fn in ["NF_2085_EscritorioReal.pdf", "NF_3150_ConstrutoraHorizonte.pdf", "NF_4899_AutoPecasCentral.pdf"]:
    r = rag_service.process_and_ingest_document(fn)
    print(f"Ingerido {fn}: {r['total_chunks']} chunks")

print("\n=== 4. Testando Consulta RAG COM dados existentes ===")
q1 = "Quais modelos de notebook foram comprados e qual o valor total da nota?"
res_q1 = rag_service.query_rag(q1, top_k=5)
print(f"Pergunta: {q1}")
print(f"Status: {res_q1['status']}")
print(f"Total candidatos recuperados: {len(res_q1['candidatos'])}")
for c in res_q1['candidatos'][:3]:
    print(f"  #{c['ranking']} - NF {c['numero_nota']} - Score {c['score_similaridade']} - Seção: {c['tipo_secao']}")
print(f"Resposta LLM:\n{res_q1['resposta']}")

print("\n=== 5. Testando Consulta RAG SEM dados (Regra de Ausência de Dados) ===")
q2 = "Qual a receita de bolo de chocolate e tempo de assar no forno?"
res_q2 = rag_service.query_rag(q2, top_k=5, min_threshold=0.55)
print(f"Pergunta: {q2}")
print(f"Status: {res_q2['status']}")
print(f"LLM Executado: {res_q2['llm_executado']}")
print(f"Resposta exata: '{res_q2['resposta']}'")
assert res_q2['resposta'] == "Sem dados disponiveis na base", "Falha na regra de ausência de dados!"

print("\n=== TODOS OS TESTES DO BACKEND PASSARAM COM SUCESSO! ===")
