import os
import re
from typing import Dict, Any, List
import pdfplumber
from pypdf import PdfReader

class InvoiceExtractor:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extrai texto integral do PDF usando pdfplumber com fallback para pypdf"""
        full_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
        except Exception:
            pass

        if not full_text.strip():
            # Fallback pypdf
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        full_text += t + "\n"
            except Exception:
                pass

        return full_text.strip()

    @staticmethod
    def parse_invoice_fields(text: str, filename: str) -> Dict[str, Any]:
        """Identifica campos estruturados na nota fiscal a partir do texto extraído"""
        data: Dict[str, Any] = {
            "nome_arquivo": filename,
            "categoria": "Notas Fiscais",
            "numero_nota": None,
            "serie": None,
            "data_emissao": None,
            "fornecedor": None,
            "cnpj_fornecedor": None,
            "endereco_fornecedor": None,
            "cliente": None,
            "cnpj_cliente": None,
            "endereco_cliente": None,
            "natureza_operacao": None,
            "itens": [],
            "valor_total": None,
            "observacoes": None,
            "texto_extraido": text
        }

        # Número da Nota
        num_match = re.search(r"N[ºo°]\s*(\d+)", text, re.IGNORECASE)
        if num_match:
            data["numero_nota"] = num_match.group(1)

        # Série
        serie_match = re.search(r"SÉRIE\s*(\d+)", text, re.IGNORECASE)
        if serie_match:
            data["serie"] = serie_match.group(1)

        # Data de emissão
        data_match = re.search(r"DATA DE EMISS[ÃA]O:\s*([\d/]+)", text, re.IGNORECASE)
        if data_match:
            data["data_emissao"] = data_match.group(1)

        # Fornecedor / Emitente
        forn_match = re.search(r"EMITENTE\s*/\s*FORNECEDOR:\s*([^\n]+)", text, re.IGNORECASE)
        if forn_match:
            data["fornecedor"] = forn_match.group(1).strip()

        # CNPJs
        cnpjs = re.findall(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", text)
        if len(cnpjs) >= 1:
            data["cnpj_fornecedor"] = cnpjs[0]
        if len(cnpjs) >= 2:
            data["cnpj_cliente"] = cnpjs[1]

        # Cliente / Destinatário
        cli_match = re.search(r"DESTINAT[ÁA]RIO\s*/\s*CLIENTE:\s*([^\n]+)", text, re.IGNORECASE)
        if cli_match:
            data["cliente"] = cli_match.group(1).strip()

        # Natureza da operação
        nat_match = re.search(r"NATUREZA DA OPERA[ÇC][ÃA]O:\s*([^\n]+)", text, re.IGNORECASE)
        if nat_match:
            data["natureza_operacao"] = nat_match.group(1).strip()

        # Valor Total
        val_match = re.search(r"VALOR TOTAL DA NOTA:\s*R\$\s*([\d\.,]+)", text, re.IGNORECASE)
        if val_match:
            val_str = val_match.group(1).replace(".", "").replace(",", ".")
            try:
                data["valor_total"] = float(val_str)
            except ValueError:
                pass

        # Observações / Informações complementares
        obs_match = re.search(r"INFORMA[ÇC][ÕO]ES COMPLEMENTARES:\s*([^\n]+(?:\n[^\n]+)*?)(?=VALOR TOTAL|$)", text, re.IGNORECASE)
        if obs_match:
            data["observacoes"] = obs_match.group(1).strip()

        # Itens / Produtos (busca por linhas de itens)
        lines = text.split("\n")
        capturing_items = False
        for line in lines:
            line_str = line.strip()
            if "Descrição do Produto" in line_str:
                capturing_items = True
                continue
            if capturing_items and ("INFORMAÇÕES COMPLEMENTARES" in line_str or "VALOR TOTAL" in line_str):
                capturing_items = False
                break
            if capturing_items and line_str:
                # Exemplo: Notebook Dell Latitude 5440 UN 5 R$ 4.500,00 R$ 22.500,00
                price_matches = re.findall(r"R\$\s*([\d\.,]+)", line_str)
                if price_matches:
                    data["itens"].append(line_str)

        # Cálculo de campos preenchidos e nulos para observabilidade estruturada
        core_fields = [
            "numero_nota", "data_emissao", "fornecedor", "cnpj_fornecedor",
            "cliente", "cnpj_cliente", "natureza_operacao", "valor_total", "observacoes"
        ]
        total_campos = len(core_fields)
        preenchidos = sum(1 for f in core_fields if data.get(f) is not None)
        nulos = total_campos - preenchidos
        percentual = round((preenchidos / total_campos) * 100, 2)

        data["total_campos"] = total_campos
        data["campos_preenchidos"] = preenchidos
        data["campos_nulos"] = nulos
        data["percentual_sucesso"] = percentual
        data["status"] = "PROCESSADO" if percentual >= 70 else "PARCIAL"

        return data

extractor = InvoiceExtractor()
