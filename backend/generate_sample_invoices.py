import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "documentos")
os.makedirs(DOCS_DIR, exist_ok=True)

invoices = [
    {
        "filename": "NF_1042_TechByte.pdf",
        "numero": "1042",
        "serie": "1",
        "data_emissao": "15/01/2026",
        "fornecedor": "TechByte Distribuidora de Eletrônicos Ltda",
        "cnpj_fornecedor": "12.345.678/0001-90",
        "endereco_fornecedor": "Av. Paulista, 1000 - Bela Vista, São Paulo - SP",
        "cliente": "Inova Soluções Digitais Ltda",
        "cnpj_cliente": "45.123.789/0001-44",
        "endereco_cliente": "Rua Funchal, 200 - Vila Olímpia, São Paulo - SP",
        "natureza_operacao": "Venda de mercadoria adquirida de terceiros",
        "itens": [
            ("Notebook Dell Latitude 5440 i7 16GB SSD 512GB", "UN", 5, 4500.00, 22500.00),
            ("Monitor LG UltraWide 29 polegadas IPS Full HD", "UN", 5, 1200.00, 6000.00)
        ],
        "valor_total": 28500.00,
        "observacoes": "Equipamentos destinados à equipe de engenharia e desenvolvimento de software. Garantia de 12 meses direto com o fabricante."
    },
    {
        "filename": "NF_2085_EscritorioReal.pdf",
        "numero": "2085",
        "serie": "1",
        "data_emissao": "02/02/2026",
        "fornecedor": "Papelaria & Escritório Real S/A",
        "cnpj_fornecedor": "98.765.432/0001-11",
        "endereco_fornecedor": "Rua Direita, 50 - Centro, Belo Horizonte - MG",
        "cliente": "Escola Futuro Brilhante ME",
        "cnpj_cliente": "11.222.333/0001-55",
        "endereco_cliente": "Av. Afonso Pena, 300 - Centro, Belo Horizonte - MG",
        "natureza_operacao": "Venda de materiais escolares e de escritório",
        "itens": [
            ("Papel A4 Chamex Caixa 5 resmas", "CX", 20, 140.00, 2800.00),
            ("Canetas Esferográficas Azul Caixa 50un", "CX", 10, 65.00, 650.00),
            ("Cadeira Ergonômica Presidente NR17", "UN", 8, 850.00, 6800.00)
        ],
        "valor_total": 10250.00,
        "observacoes": "Material escolar e mobiliário para professores do ensino fundamental. Entrega no bloco pedagógico."
    },
    {
        "filename": "NF_3150_ConstrutoraHorizonte.pdf",
        "numero": "3150",
        "serie": "2",
        "data_emissao": "18/02/2026",
        "fornecedor": "Construtora & Materiais Horizonte Ltda",
        "cnpj_fornecedor": "45.678.901/0001-22",
        "endereco_fornecedor": "Rodovia BR-101, Km 42 - Zona Industrial, Curitiba - PR",
        "cliente": "Condomínio Edifício Solar",
        "cnpj_cliente": "77.888.999/0001-00",
        "endereco_cliente": "Rua das Flores, 850 - Batel, Curitiba - PR",
        "natureza_operacao": "Comércio de materiais de construção civil",
        "itens": [
            ("Cimento CP-II 50kg Votoran", "SC", 100, 38.00, 3800.00),
            ("Tinta Acrílica Fosca Branco Neve Lata 18L Suvinil", "LT", 15, 320.00, 4800.00),
            ("Cabo Flexível de Cobre 2,5mm Rolo 100m Sil", "RL", 12, 210.00, 2520.00)
        ],
        "valor_total": 11120.00,
        "observacoes": "Material destinado à reforma da fachada externa e adequação da rede elétrica do condomínio."
    },
    {
        "filename": "NF_4899_AutoPecasCentral.pdf",
        "numero": "4899",
        "serie": "1",
        "data_emissao": "10/03/2026",
        "fornecedor": "AutoPeças & Mecânica Central Eireli",
        "cnpj_fornecedor": "33.444.555/0001-88",
        "endereco_fornecedor": "Av. Brasil, 4500 - Ramos, Rio de Janeiro - RJ",
        "cliente": "Transportadora Rápido Seguro Ltda",
        "cnpj_cliente": "66.777.888/0001-99",
        "endereco_cliente": "Av. Presidente Vargas, 1200 - Centro, Rio de Janeiro - RJ",
        "natureza_operacao": "Venda de autopeças e acessórios automotivos",
        "itens": [
            ("Pneu Michelin Aro 16 Primacy 4 205/55R16", "UN", 8, 750.00, 6000.00),
            ("Óleo Lubrificante 15W40 Mineral Galão 20L", "GL", 4, 390.00, 1560.00),
            ("Jogo de Pastilhas de Freio Dianteiras Bosch", "JG", 6, 180.00, 1080.00)
        ],
        "valor_total": 8640.00,
        "observacoes": "Peças de reposição para manutenção preventiva da frota de veículos leves da transportadora."
    }
]

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontSize=16,
    leading=20,
    textColor=colors.HexColor('#1E293B'),
    alignment=1
)
subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#64748B'),
    alignment=1
)
bold_label = ParagraphStyle(
    'BoldLabel',
    parent=styles['Normal'],
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#0F172A'),
    fontName='Helvetica-Bold'
)
normal_text = ParagraphStyle(
    'NormalText',
    parent=styles['Normal'],
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#334155')
)

for inv in invoices:
    filepath = os.path.join(DOCS_DIR, inv["filename"])
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    # Header DANFE / Nota Fiscal
    story.append(Paragraph("DANFE - DOCUMENTO AUXILIAR DA NOTA FISCAL ELETRÔNICA", title_style))
    story.append(Paragraph(f"Nº {inv['numero']} | SÉRIE {inv['serie']} | DATA DE EMISSÃO: {inv['data_emissao']}", subtitle_style))
    story.append(Spacer(1, 15))
    
    # Emitente / Destinatário
    data_header = [
        [
            Paragraph(f"<b>EMITENTE / FORNECEDOR:</b><br/>{inv['fornecedor']}<br/>CNPJ: {inv['cnpj_fornecedor']}<br/>{inv['endereco_fornecedor']}", normal_text),
            Paragraph(f"<b>DESTINATÁRIO / CLIENTE:</b><br/>{inv['cliente']}<br/>CNPJ: {inv['cnpj_cliente']}<br/>{inv['endereco_cliente']}", normal_text)
        ]
    ]
    t_header = Table(data_header, colWidths=[270, 270])
    t_header.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 10))
    
    # Natureza da operação
    story.append(Paragraph(f"<b>NATUREZA DA OPERAÇÃO:</b> {inv['natureza_operacao']}", normal_text))
    story.append(Spacer(1, 10))
    
    # Tabela de Itens
    items_data = [
        [
            Paragraph("<b>Descrição do Produto / Serviço</b>", bold_label),
            Paragraph("<b>Unid.</b>", bold_label),
            Paragraph("<b>Qtd.</b>", bold_label),
            Paragraph("<b>Valor Unit. (R$)</b>", bold_label),
            Paragraph("<b>Valor Total (R$)</b>", bold_label)
        ]
    ]
    for item in inv["itens"]:
        items_data.append([
            Paragraph(item[0], normal_text),
            Paragraph(item[1], normal_text),
            Paragraph(str(item[2]), normal_text),
            Paragraph(f"R$ {item[3]:,.2f}", normal_text),
            Paragraph(f"R$ {item[4]:,.2f}", normal_text)
        ])
    
    t_items = Table(items_data, colWidths=[260, 45, 45, 95, 95])
    t_items.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_items)
    story.append(Spacer(1, 10))
    
    # Resumo / Total
    tot_data = [
        [
            Paragraph(f"<b>INFORMAÇÕES COMPLEMENTARES:</b><br/>{inv['observacoes']}", normal_text),
            Paragraph(f"<b>VALOR TOTAL DA NOTA:</b><br/><font size='13' color='#1E293B'><b>R$ {inv['valor_total']:,.2f}</b></font>", bold_label)
        ]
    ]
    t_tot = Table(tot_data, colWidths=[360, 180])
    t_tot.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_tot)
    
    doc.build(story)
    print(f"Gerado: {filepath}")

print("Todos os 4 PDFs fictícios foram gerados com sucesso!")
