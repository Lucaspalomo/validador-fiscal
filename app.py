import streamlit as st
import pandas as pd
import time
from core import *

st.set_page_config(page_title="Validador Fiscal Pro", layout="wide")

# Título único e sem caracteres especiais que quebram o encoding
st.title("?? Auditoria Fiscal")

tab1, tab2, tab3 = st.tabs(["?? Consulta", "?? XML", "?? Base"])

with tab1:
    entrada = st.text_input("Digite o EAN ou Nome do Produto:")
    if st.button("Validar Item"):
        # Sua lógica de consulta aqui...
        pass

with tab2:
    arquivo = st.file_uploader("Suba o XML da NF-e", type=['xml'])
    if arquivo:
        itens = processar_xml_nfe(arquivo.read())
        if itens:
            df = pd.DataFrame(itens)
            st.dataframe(df, use_container_width=True)
            
            if st.button("Auditar todos os itens da nota"):
                for item in itens:
                    with st.expander(f"Item {item['Item']} - {item['Descrição']}"):
                        with st.spinner("Consultando IA..."):
                            # Aumentamos o delay para 10 segundos para evitar o erro de limite da IA gratuita
                            time.sleep(10) 
                            prompt = f"Valide o NCM {item['NCM']} para {item['Descrição']}"
                            # resposta = consultar_gemini(prompt)
                            st.write("Resultado da Auditoria...")