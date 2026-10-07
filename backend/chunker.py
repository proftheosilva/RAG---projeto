from typing import List, Dict, Any

class ChunkManager:
    @staticmethod
    def chunk_invoice(doc_id: str, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        chunks = []
        pos = 1

        numero_nota = parsed_data.get("numero_nota") or "S/N"
        fornecedor = parsed_data.get("fornecedor") or "Não identificado"
        cnpj_fornecedor = parsed_data.get("cnpj_fornecedor") or "N/A"
        cliente = parsed_data.get("cliente") or "Não identificado"
        cnpj_cliente = parsed_data.get("cnpj_cliente") or "N/A"
        data_emissao = parsed_data.get("data_emissao") or "N/A"
        natureza = parsed_data.get("natureza_operacao") or "N/A"
        valor_total = parsed_data.get("valor_total")
        valor_total_str = f"R$ {valor_total:,.2f}" if valor_total is not None else "N/A"
        observacoes = parsed_data.get("observacoes") or "Sem observações"
        itens = parsed_data.get("itens") or []
        itens_text = "\n".join(itens) if itens else "Itens detalhados no corpo da nota fiscal"

        # Chunk 1: Cabeçalho e Fornecedor (Emitente)
        c1_text = (
            f"NOTA FISCAL Nº {numero_nota} | SÉRIE {parsed_data.get('serie', '1')} | DATA DE EMISSÃO: {data_emissao}\n"
            f"EMITENTE / FORNECEDOR: {fornecedor}\n"
            f"CNPJ DO FORNECEDOR: {cnpj_fornecedor}"
        )
        chunks.append({
            "documento_id": doc_id,
            "posicao_chunk": pos,
            "tipo_secao": "cabecalho_fornecedor",
            "texto": c1_text,
            "metadados": {
                "numero_nota": numero_nota,
                "fornecedor": fornecedor,
                "cnpj_fornecedor": cnpj_fornecedor,
                "posicao": pos,
                "tipo": "cabecalho_fornecedor"
            }
        })
        pos += 1

        # Chunk 2: Destinatário e Natureza da Operação
        c2_text = (
            f"NOTA FISCAL Nº {numero_nota} | DESTINATÁRIO / CLIENTE: {cliente}\n"
            f"CNPJ DO CLIENTE: {cnpj_cliente}\n"
            f"NATUREZA DA OPERAÇÃO: {natureza}"
        )
        chunks.append({
            "documento_id": doc_id,
            "posicao_chunk": pos,
            "tipo_secao": "cliente_destinatario",
            "texto": c2_text,
            "metadados": {
                "numero_nota": numero_nota,
                "cliente": cliente,
                "cnpj_cliente": cnpj_cliente,
                "posicao": pos,
                "tipo": "cliente_destinatario"
            }
        })
        pos += 1

        # Chunk 3: Produtos / Itens da Nota
        c3_text = (
            f"NOTA FISCAL Nº {numero_nota} ({fornecedor}) - PRODUTOS E SERVIÇOS:\n"
            f"{itens_text}"
        )
        chunks.append({
            "documento_id": doc_id,
            "posicao_chunk": pos,
            "tipo_secao": "itens_produtos",
            "texto": c3_text,
            "metadados": {
                "numero_nota": numero_nota,
                "fornecedor": fornecedor,
                "qtd_itens": len(itens),
                "posicao": pos,
                "tipo": "itens_produtos"
            }
        })
        pos += 1

        # Chunk 4: Totais e Observações
        c4_text = (
            f"NOTA FISCAL Nº {numero_nota} - TOTAL E INFORMAÇÕES COMPLEMENTARES:\n"
            f"VALOR TOTAL DA NOTA: {valor_total_str}\n"
            f"OBSERVAÇÕES: {observacoes}"
        )
        chunks.append({
            "documento_id": doc_id,
            "posicao_chunk": pos,
            "tipo_secao": "totais_observacoes",
            "texto": c4_text,
            "metadados": {
                "numero_nota": numero_nota,
                "valor_total": valor_total,
                "posicao": pos,
                "tipo": "totais_observacoes"
            }
        })
        pos += 1

        # Chunk 5: Síntese Completa da Nota Fiscal (Visão Consolidada)
        c5_text = (
            f"RESUMO COMPLETO DA NOTA FISCAL Nº {numero_nota}:\n"
            f"Emissão: {data_emissao} | Fornecedor: {fornecedor} (CNPJ: {cnpj_fornecedor}) | "
            f"Cliente: {cliente} (CNPJ: {cnpj_cliente}) | Natureza: {natureza} | "
            f"Itens: {itens_text} | "
            f"Valor Total: {valor_total_str} | Finalidade: {observacoes}"
        )
        chunks.append({
            "documento_id": doc_id,
            "posicao_chunk": pos,
            "tipo_secao": "resumo_consolidado",
            "texto": c5_text,
            "metadados": {
                "numero_nota": numero_nota,
                "fornecedor": fornecedor,
                "cliente": cliente,
                "valor_total": valor_total,
                "posicao": pos,
                "tipo": "resumo_consolidado"
            }
        })

        return chunks

chunker = ChunkManager()
