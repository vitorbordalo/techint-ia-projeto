# ==========================================================
# ASSISTENTE TECHINT IA - VERSÃO PREMIUM
# ==========================================================

# ----------------------------------------------------------
# IMPORTAÇÕES
# ----------------------------------------------------------
# Aqui importamos todas as bibliotecas necessárias:
# - Streamlit → Interface web
# - ChromaDB → Banco vetorial para busca semântica
# - OpenAI (Groq) → Modelo de linguagem
# - PyPDF → Extração de texto dos relatórios
# - dotenv → Segurança da chave de API
# ----------------------------------------------------------

import os
import re
import time
import streamlit as st
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from openai import OpenAI
from pypdf import PdfReader
from dotenv import load_dotenv


# ==========================================================
# CONFIGURAÇÃO INICIAL DO APP
# ==========================================================
# Define título da aba, ícone e layout responsivo.
# Aqui já mostramos preocupação com experiência do usuário.
# ==========================================================

st.set_page_config(
    page_title="Techint AI Assistant",
    page_icon="🏗️",
    layout="wide",
)

# Carrega variáveis do arquivo .env (segurança)
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Se não existir chave, o sistema bloqueia execução
# → Mostra preocupação com governança e segurança.
if not API_KEY:
    st.error("API Key não encontrada.")
    st.stop()


# ==========================================================
# CONFIGURAÇÃO DO MODELO DE IA
# ==========================================================
# Utilizamos Groq via compatibilidade OpenAI.
# Modelo escolhido é leve, rápido e eficiente para POC.
# ==========================================================

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


# ==========================================================
# CONFIGURAÇÃO DO BANCO VETORIAL
# ==========================================================
# Aqui está o diferencial técnico:
# - Transformamos texto em vetores semânticos
# - Permitimos busca inteligente por significado,
#   não apenas por palavra-chave
# ==========================================================

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # Modelo local para gerar embeddings
)

chroma_client = chromadb.Client(
    Settings(persist_directory="./db")  # Banco persistente local
)

collection = chroma_client.get_or_create_collection(
    name="techint_docs",
    embedding_function=embedding_function
)


# ==========================================================
# FUNÇÕES DE PROCESSAMENTO DE DOCUMENTO
# ==========================================================
# Essas funções estruturam a "engenharia de dados"
# antes da IA utilizar o conteúdo.
# ==========================================================

def extrair_texto_pdf(arquivo):
    # Lê todas as páginas do PDF e extrai o texto bruto.
    pdf = PdfReader(arquivo)
    texto = ""
    for pagina in pdf.pages:
        if pagina.extract_text():
            texto += pagina.extract_text()
    return texto


def limpar_texto(texto):
    # Remove quebras de linha, espaços excessivos
    # e ruídos que prejudicam a qualidade semântica.
    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto)
    texto = texto.replace("- ", "")
    return texto


def dividir_texto(texto, tamanho=1200, sobreposicao=200):
    # Técnica chamada "chunking"
    # Divide o texto em blocos menores para:
    # - Melhorar precisão da busca
    # - Evitar perda de contexto
    # - Reduzir custo computacional

    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = inicio + tamanho
        chunks.append(texto[inicio:fim])
        inicio += tamanho - sobreposicao
    return chunks


# ==========================================================
# ESTILO VISUAL (UX CORPORATIVO)
# ==========================================================
# Aqui criamos identidade premium:
# - Paleta escura corporativa
# - Destaque vermelho Techint
# - Layout centralizado
# - Interface estilo SaaS executivo
# ==========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0e1117;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 600;
    color: white;
    margin-bottom: 20px;
}

.main-container {
    max-width: 850px;
    margin: auto;
}

.user-message {
    background: #1f2937;
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: white;
    text-align: right;
}

.bot-message {
    background: #991b1b;
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: white;
    text-align: left;
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# SIDEBAR – UPLOAD DE RELATÓRIOS
# ==========================================================
# Aqui ocorre a indexação dos documentos:
# 1. Upload múltiplo
# 2. Extração
# 3. Limpeza
# 4. Chunking
# 5. Conversão para vetor
# 6. Armazenamento no banco vetorial
# ==========================================================

with st.sidebar:
    st.markdown("<div class='sidebar-title'>🏗️ Techint AI</div>", unsafe_allow_html=True)
    st.caption("Gestão Inteligente de Conhecimento")

    uploaded_files = st.file_uploader(
        "Adicionar Relatórios",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Processar Documentos"):
            with st.spinner("Indexando documentos..."):
                total_chunks = 0
                for uploaded_file in uploaded_files:
                    texto = extrair_texto_pdf(uploaded_file)
                    texto = limpar_texto(texto)
                    chunks = dividir_texto(texto)

                    # Cada chunk vira um vetor semântico
                    for i, chunk in enumerate(chunks):
                        collection.add(
                            documents=[chunk],
                            ids=[f"{uploaded_file.name}_{i}_{time.time()}"]
                        )

                    total_chunks += len(chunks)

            st.success("Documentos indexados.")
            st.caption(f"{total_chunks} blocos adicionados.")


# ==========================================================
# CHAT – INTERAÇÃO EXECUTIVA
# ==========================================================
# Mantém histórico de conversa (estado persistente)
# ==========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.title("Assistente de Documentação Técnica")
st.caption("Baseado em relatórios oficiais da Techint E&C")

for autor, mensagem in st.session_state.chat_history:
    if autor == "user":
        st.markdown(f"<div class='user-message'>{mensagem}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{mensagem}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# ENVIO DE PERGUNTA
# ==========================================================
# Fluxo completo:
# 1. Usuário faz pergunta
# 2. Sistema busca vetores mais relevantes
# 3. Monta contexto
# 4. Envia para IA
# 5. IA responde baseada SOMENTE no contexto
# ==========================================================

with st.form("chat_form", clear_on_submit=True):
    pergunta = st.text_input("Faça uma pergunta sobre os relatórios...")
    submit = st.form_submit_button("Enviar")

if submit and pergunta:

    inicio = time.time()

    # Busca semântica no banco vetorial
    resultados = collection.query(
        query_texts=[pergunta],
        n_results=6
    )

    contexto = ""
    if resultados["documents"]:
        contexto = " ".join(resultados["documents"][0])

    # Geração da resposta baseada no contexto encontrado
    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
Você é um assistente executivo da Techint E&C.
Responda de forma profissional e clara.
Utilize apenas o contexto fornecido.
Se não houver dados suficientes, informe.
"""
            },
            {
                "role": "user",
                "content": f"""
CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}
"""
            }
        ],
        temperature=0
    )

    resposta_final = resposta.choices[0].message.content
    fim = time.time()

    st.session_state.chat_history.append(("user", pergunta))
    st.session_state.chat_history.append(("bot", resposta_final))

    st.rerun()

st.markdown("---")
st.caption("Techint Engineering & Construction | AI Knowledge Assistant")