import streamlit as st
import pandas as pd
import time
from core import * # Isso importa tudo do seu core.py

# --- CONFIGURAÇÃO INICIAL ---
CHAVE_API = "AIzaSyB5EZ5euiuNxbLOSlQ3VCf_FhGq9SNK4_w"

try:
    configurar_ia(CHAVE_API)
except NameError:
    st.error("Erro: A função 'configurar_ia' não foi encontrada no core.py")

st.set_page_config(page_title="Validador Fiscal Pro", layout="wide")
st.title("Auditoria Fiscal")

tab1, tab2, tab3 = st.tabs(["Consulta", "XML", "Base"])

with tab1:
    st.header("Pesquisa Rápida")
    entrada = st.text_input("Digite o EAN ou Nome do Produto:")
    if st.button("Validar Item"):
        with st.spinner("Consultando..."):
            res = consultar_gemini(f"Valide NCM/CEST para: {entrada}")
            st.markdown(res)

with tab2:
    st.header("Análise de NF-e")
    arquivo = st.file_uploader("Suba o XML", type=['xml'])
    if arquivo:
        itens = processar_xml_nfe(arquivo.read())
        if itens:
            st.dataframe(pd.DataFrame(itens), use_container_width=True)
            if st.button("🚀 Iniciar Auditoria Completa"):
                for item in itens:
                    with st.expander(f"Item - {item['Descrição']}"):
                        time.sleep(12) 
                        prompt = f"Analise o NCM {item['NCM']} para {item['Descrição']}."
                        resposta = consultar_gemini(prompt)
                        st.info(resposta)

with tab3:
    st.write("Base local operacional.")