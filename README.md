# 🏗️ Techint AI Assistant  
### AI-Powered Technical Knowledge Management System

Sistema inteligente de consulta técnica baseado em relatórios oficiais da **Techint Engineering & Construction**, utilizando Inteligência Artificial e busca semântica avançada.

---

## 📌 Visão Geral

O **Techint AI Assistant** transforma relatórios técnicos extensos em uma base inteligente e pesquisável, permitindo que executivos e engenheiros obtenham respostas rápidas, contextualizadas e profissionais.

O sistema combina:

- 📄 Processamento de múltiplos PDFs  
- 🧠 Embeddings locais (sem custo por token)  
- 🔎 Busca semântica inteligente  
- 🤖 LLM para geração de respostas executivas  
- 💬 Interface estilo ChatGPT com layout premium  

---

## 🧠 Arquitetura da Solução

Relatórios PDF  
↓  
Extração de Texto (PyPDF)  
↓  
Divisão em Blocos (Chunking Inteligente)  
↓  
Embeddings Locais (SentenceTransformers)  
↓  
ChromaDB (Banco Vetorial)  
↓  
Busca Semântica  
↓  
LLM (Groq API - OpenAI Compatible)  
↓  
Resposta Executiva ao Usuário  

---

## 🛠️ Stack Tecnológica

- **Frontend:** Streamlit  
- **Backend:** Python  
- **Banco Vetorial:** ChromaDB  
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)  
- **LLM Provider:** Groq (API compatível com OpenAI)  
- **Processamento de PDF:** PyPDF  
- **Gerenciamento de ambiente:** python-dotenv  

---

## 🚀 Principais Funcionalidades

### 📂 Upload de múltiplos relatórios
Permite indexar diversos PDFs simultaneamente em uma única base de conhecimento.

### 🔍 Busca semântica
Não depende de palavras-chave exatas.  
A IA entende o significado contextual do conteúdo.

### 🧠 Embeddings locais
Os vetores são gerados localmente, reduzindo custo e aumentando performance.

### 🤖 Respostas executivas
A IA:
- Usa apenas o contexto encontrado  
- Responde de forma profissional  
- Informa quando não há dados suficientes  

### 🎨 Interface Premium
- Layout dark corporativo  
- Identidade visual alinhada à engenharia  
- Estilo semelhante ao ChatGPT  
- Histórico de conversa persistente  

---

## 📦 Instalação

Clone o repositório:

git clone https://github.com/vitorbordalo/techint-ia-projeto.git  
cd techint-ia-projeto  

Instale as dependências:

pip install -r requirements.txt  

---

## 🔐 Configuração

Crie um arquivo `.env` na raiz do projeto:

OPENAI_API_KEY=sua_chave_groq_aqui  

⚠️ Nunca suba o `.env` para o GitHub.

---

## ▶️ Execução

streamlit run app.py  

Acesse no navegador:

http://localhost:8501  

---

## 📊 Aplicações Reais

Este projeto pode ser utilizado para:

- Gestão de conhecimento corporativo  
- Consulta de relatórios ESG  
- Análise de documentação técnica  
- Apoio estratégico a executivos  
- Transformação digital em engenharia  

---

## 🔒 Segurança

- API Key protegida via `.env`  
- Embeddings processados localmente  
- Banco vetorial persistente local  
- `.gitignore` configurado corretamente  

---

## 📈 Próximas Evoluções

- Deploy em nuvem (AWS / GCP / Azure)  
- Autenticação corporativa  
- Dashboard analítico  
- Permissões por área  
- Integração com SharePoint ou ERP  
- Versionamento automático de relatórios  

---

## 👨‍💻 Autor

**Vitor Bordalo**  
Software Engineering Student  
AI & Intelligent Systems  

---

## 🏗️ Sobre a Techint Engineering & Construction

Projeto demonstrativo de aplicação de Inteligência Artificial na gestão de conhecimento técnico corporativo.
