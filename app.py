import streamlit as st
import pandas as pd
import time
from core import *

# --- CONFIGURAÇÃO INICIAL ---
CHAVE_API = "AIzaSyB5EZ5euiuNxbLOSlQ3VCf_FhGq9SNK4_w"
configurar_ia(CHAVE_API)

st.set_page_config(page_title="Validador Fiscal Pro", layout="wide")

# Título único
st.title("Auditoria Fiscal")

# AQUI ESTAVA O ERRO: As abas precisam ser criadas primeiro!
tab1, tab2, tab3 = st.tabs(["Consulta", "XML", "Base"])

# --- TAB 1: CONSULTA UNITÁRIA ---
with tab1:
    st.header("Pesquisa Rápida")
    entrada = st.text_input("Digite o EAN ou Nome do Produto:")
    if st.button("Validar Item"):
        with st.spinner("Consultando..."):
            resultado = consultar_gemini(f"Valide NCM/CEST para: {entrada}")
            st.markdown(resultado)

# --- TAB 2: PROCESSAR XML ---
with tab2:
    st.header("Análise de NF-e")
    arquivo = st.file_uploader("Suba o XML da NF-e", type=['xml'])
    if arquivo:
        itens = processar_xml_nfe(arquivo.read())
        if itens:
            df = pd.DataFrame(itens)
            st.write(f"Itens encontrados: {len(df)}")
            st.dataframe(df, use_container_width=True)
            
            if st.button("🚀 Iniciar Auditoria Completa"):
                for item in itens:
                    with st.expander(f"Item {item['Item']} - {item['Descrição']}"):
                        with st.spinner("IA analisando..."):
                            time.sleep(12) # Delay anti-bloqueio
                            prompt = f"Analise o NCM {item['NCM']} para o produto {item['Descrição']}. Está correto? Se não, sugira o certo e o CEST."
                            resposta = consultar_gemini(prompt)
                            st.info(resposta)
        else:
            st.error("Erro ao ler o XML.")

# --- TAB 3: BASE DE DADOS ---
with tab3:
    st.header("Configurações")
    st.write("Base de conhecimento local ativa.")