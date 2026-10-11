# RAG + Teophilo — Pipeline RAG Didático

Sistema educacional de **Retrieval-Augmented Generation (RAG)** focado em observabilidade, arquitetura limpa e rastreabilidade total do processo de IA generativa aplicada a documentos (Notas Fiscais em PDF).

---

## 🎯 Objetivos Educacionais

Diferente de chatbots genéricos, esta aplicação foi desenhada para tornar visível cada engrenagem de um pipeline RAG:
1. **Ingestão & OCR**: Leitura de PDFs e extração de dados tabulares estruturados.
2. **Chunking**: Divisão em blocos semânticos com metadados detalhados de rastreabilidade.
3. **Tokenização**: Contagem e decomposição didática de tokens com `tiktoken`.
4. **Embeddings Locais**: Geração de vetores numéricos de 384 dimensões em ONNX Runtime local via **FastEmbed** (`BAAI/bge-small-en-v1.5`).
5. **Banco Vetorial Supabase (PGVector)**: Persistência de vetores e busca vetorial por similaridade de cosseno com `top_k = 5`.
6. **Prompt Aumentado**: Construção transparente unindo Pergunta + Contexto Recuperado + Instruções do Sistema.
7. **LLM via OpenRouter**: Resposta fundamentada com o modelo `openrouter/auto`.
8. **Regra Estrita Anti-Alucinação**: Caso a pergunta não possua dados suficientes no banco, o sistema retorna exatamente `"Sem dados disponiveis na base"`.

---

## 🛠️ Stacks Utilizadas

- **Backend**: Python 3.11+ / 3.13, FastAPI, Uvicorn, Pydantic, ReportLab, PDFPlumber, PyPDF, TikToken, FastEmbed.
- **Banco de Dados**: Supabase (PostgreSQL 15+ com extensão `pgvector`).
- **Embeddings**: FastEmbed ONNX (`BAAI/bge-small-en-v1.5`, 384 dimensões).
- **LLM**: OpenRouter API (`openrouter/auto`).
- **Frontend**: Next.js 16 (App Router, TypeScript, Vanilla CSS com Glassmorphism e tema tecnológico).

---

## 📋 Pré-requisitos

- **Python** (versão 3.10 ou superior)
- **Node.js** (versão 18 ou superior) e **npm**
- Conta e projeto no **Supabase** (com `pgvector` habilitado)
- Chave de API no **OpenRouter**

---

## ⚙️ Procedimento de Configuração do Ambiente Python

Siga os passos abaixo para configurar o ambiente virtual e instalar as dependências do backend:

### 1. Clonar ou Acessar a Raiz do Repositório
Abra o terminal na pasta raiz do projeto:
```bash
cd rag
```

### 2. Criar o Ambiente Virtual (`venv`)

- **No Windows (PowerShell ou Prompt de Comando)**:
  ```powershell
  python -m venv venv
  ```
- **No Linux / macOS**:
  ```bash
  python3 -m venv venv
  ```

### 3. Ativar o Ambiente Virtual

- **No Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(Caso ocorra restrição de política de execução no PowerShell, execute primeiro `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

- **No Windows (CMD / Prompt de Comando)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

- **No Linux / macOS**:
  ```bash
  source venv/bin/activate
  ```

### 4. Atualizar o `pip` e Instalar os Pacotes do `requirements.txt`

Com o ambiente virtual ativado, execute:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 Configuração das Variáveis de Ambiente (`.env`)

Crie um arquivo `.env` na raiz do projeto (ou copie a partir do [.env.example](file:///.env.example)):

```ini
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_PUBLISHABLE_KEY=sua_publishable_key
SUPABASE_SECRET_KEY=sua_secret_service_role_key

# OpenRouter
OPENROUTER_API_KEY=sk-or-v1-...
```

> **Atenção de Segurança**: O arquivo `.env` contém chaves confidenciais e **nunca** deve ser versionado no Git. Ele já está devidamente listado no [.gitignore](file:///.gitignore).

---

## 📑 Gerar as Notas Fiscais Fictícias de Teste

Para criar os 4 documentos PDF de notas fiscais de teste em `documentos/`:

```bash
python backend/generate_sample_invoices.py
```

Os seguintes arquivos serão gerados:
- `NF_1042_TechByte.pdf` (Informática e Eletrônicos)
- `NF_2085_EscritorioReal.pdf` (Mobiliário e Papelaria)
- `NF_3150_ConstrutoraHorizonte.pdf` (Materiais de Construção)
- `NF_4899_AutoPecasCentral.pdf` (Autopeças e Lubrificantes)

---

## 🚀 Como Executar o Projeto

Abra dois terminais na raiz do projeto. Ative o ambiente virtual Python no terminal do backend.

### Terminal 1 — Iniciar o Backend (FastAPI)
Com o `venv` ativado:
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
A API estará disponível em:
- **API Base**: `http://127.0.0.1:8000`
- **Documentação Swagger**: `http://127.0.0.1:8000/docs`

### Terminal 2 — Iniciar o Frontend (Next.js)
Navegue até a pasta `frontend` e instale as dependências (se for a primeira vez):
```bash
cd frontend && npm run dev
```

Se esta for a primeira execução do frontend, instale antes suas dependências, dentro de `frontend`, com `npm install`. Depois que os dois terminais estiverem rodando, acesse **[http://localhost:3000](http://localhost:3000)**.

---

## 🧪 Como Testar a Aplicação

1. **Aba 📥 Pipeline de Ingestão**:
   - Clique em **"⚡ Ingerir Todos os 4 PDFs"**.
   - Observe a animação e o progresso em 5 fases: `Ingestão/OCR ➔ Chunking ➔ Tokenização ➔ Embedding ➔ Índice Vetorial`.
   - Veja a tabela com o percentual de campos válidos, amostra de tokens e previews vetoriais de cada chunk.

2. **Aba 💬 Consulta RAG**:
   - Faça perguntas de exemplo:
     - *"Quais modelos de notebook foram comprados e qual foi o total da nota?"*
     - *"Quanto custou a tinta acrílica e o cimento na reforma?"*
     - *"Quais pneus foram adquiridos para a frota?"*
   - Teste a regra de **Ausência de Dados**:
     - *"Qual a receita de bolo de chocolate?"*
     - Resultado esperado: `"Sem dados disponiveis na base"`.
   - Clique em **"▼ Inspecionar Pipeline RAG (Passo a Passo)"** no balão da resposta para visualizar a tokenização da sua pergunta, vetor gerado, Top 5 candidatos no PGVector com scores de similaridade, prompt aumentado construído e métricas de tempo em milissegundos.

---

## 📂 Estrutura de Diretórios

```text
rag/
├── .env                       # Variáveis de ambiente locais (ignorado no Git)
├── .env.example               # Exemplo de configuração do .env
├── .gitignore                 # Filtro de arquivos e diretórios desnecessários
├── requirements.txt           # Dependências Python do backend
├── README.md                  # Documentação completa do projeto
├── prompt                     # Especificação mestre de requisitos
├── rag.txt                    # Definições de ambiente e arquitetura
├── documentos/                # PDFs de teste das Notas Fiscais
│   ├── NF_1042_TechByte.pdf
│   ├── NF_2085_EscritorioReal.pdf
│   ├── NF_3150_ConstrutoraHorizonte.pdf
│   └── NF_4899_AutoPecasCentral.pdf
├── backend/                   # Código-fonte da API Python (FastAPI)
│   ├── config.py              # Leitura de variáveis com python-dotenv
│   ├── database.py            # Integração Supabase e chamadas PGVector
│   ├── extractor.py           # Extração OCR e estruturação tabular
│   ├── chunker.py             # Divisão em chunks e metadados
│   ├── tokenizer.py           # Tokenização explícita via TikToken
│   ├── embedder.py            # FastEmbed BAAI/bge-small-en-v1.5 (384d)
│   ├── rag_service.py         # Pipeline completo de RAG e regras de negócio
│   ├── main.py                # Rotas da API FastAPI
│   └── generate_sample_invoices.py  # Gerador dos PDFs fictícios
└── frontend/                  # Aplicação web moderna em Next.js
    ├── app/
    │   ├── globals.css        # Design system e Glassmorphism
    │   ├── layout.tsx         # Layout base e metadados
    │   └── page.tsx           # Interface com Chat, Ingestão e PGVector
    ├── package.json
    └── next.config.ts         # Configuração de rewrites para a API
```


## Frontend restaurado

Na pasta `frontend`, execute `npm install` e `npm run dev`. Acesse http://127.0.0.1:3000. O Next.js encaminha `/api/*` ao backend em http://127.0.0.1:8000. Para outro endereço, configure `BACKEND_URL` no ambiente do processo Next.js. Nenhuma chave Supabase ou OpenRouter é enviada ao navegador.

O chat consulta `POST /api/query` com `pergunta`, `top_k` e `min_threshold`. Cada consulta é independente: o histórico visual não é memória conversacional. A inspeção mostra trechos recuperados, IDs, metadados, scores, prompt aumentado e tempos medidos pelo backend após a conclusão. A tokenização tiktoken é didática e independente da tokenização interna do FastEmbed e do modelo de geração. Os tokens de entrada, saída e total são retornados pelo OpenRouter; campos ausentes aparecem como não informados. A API também retorna o modelo efetivamente utilizado.

A ingestão usa `POST /api/ingest`. A tela consulta os nomes dos documentos e a quantidade de chunks associados no Supabase; exibe apenas PDFs locais ainda sem chunks e informa o total de documentos e chunks vetorizados. O botão para ingerir todos também respeita esse filtro. A identificação usa o nome do arquivo: substituir o conteúdo mantendo o mesmo nome não dispara nova ingestão automaticamente. O extrator atual lê texto de PDFs, sem OCR de páginas escaneadas. O projeto deve permanecer local para esta prática; suas rotas de ingestão e exclusão não possuem autenticação.
