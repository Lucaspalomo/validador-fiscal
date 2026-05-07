import streamlit as st
import pandas as pd
import time
from core import *

# --- CONFIGURAÇÃO INICIAL ---
# Pega a chave de uma configuração segura, não escrita no código
CHAVE_API = st.secrets["GEMINI_API_KEY"]
configurar_ia(CHAVE_API)

st.set_page_config(page_title="Validador Fiscal Pro", layout="wide")
st.title("?? Auditoria Fiscal (XML + Base Local)")

# Menu em Abas
tab1, tab2, tab3 = st.tabs(["?? Consulta Unitária", "?? Processar XML", "?? Base de Dados"])

# --- TAB 1: CONSULTA UNITÁRIA ---
with tab1:
    entrada = st.text_input("Digite o EAN ou Nome do Produto:")
    if st.button("Validar Item"):
        base = carregar_base()
        if entrada in base:
            st.success("? Encontrado na Base de Conhecimento Local!")
            st.write(base[entrada])
        else:
            with st.spinner("Consultando IA..."):
                resultado = consultar_gemini(f"Valide NCM/CEST para: {entrada}. Retorne tabela.")
                st.markdown(resultado)

# --- TAB 2: PROCESSAR XML ---
with tab2:
    arquivo = st.file_uploader("Suba o XML da NF-e", type=['xml'])
    if arquivo:
        # Lê o conteúdo do arquivo
        conteudo_xml = arquivo.read()
        itens = processar_xml_nfe(conteudo_xml)
        
        if itens:
            df = pd.DataFrame(itens)
            st.write(f"Itens encontrados: {len(df)}")
            st.dataframe(df, use_container_width=True)
            
            if st.button("Auditar todos os itens da nota"):
                for item in itens:
                    with st.expander(f"Item {item['Item']} - {item['Descrição']}"):
                        prompt = f"Analise o NCM {item['NCM']} para o produto {item['Descrição']}. Responda se está correto ou sugira o certo."
                        resposta = consultar_gemini(prompt)
                        st.write(resposta)
                        time.sleep(4) # Aumentamos para 4 segundos para evitar o bloqueio
        else:
            st.error("Não foi possível extrair itens deste XML. Verifique o formato.")

# --- TAB 3: BASE DE DADOS ---
with tab3:
    st.subheader("Gerenciar Conhecimento")
    with st.expander("? Adicionar/Corrigir Dados Manuais"):
        c1, c2, c3 = st.columns(3)
        ean_input = c1.text_input("EAN")
        ncm_input = c2.text_input("NCM Correto")
        cest_input = c3.text_input("CEST Correto")
        if st.button("Salvar Correção"):
            if ean_input:
                salvar_na_base(ean_input, {"ncm": ncm_input, "cest": cest_input})
                st.success(f"Item {ean_input} salvo com sucesso!")
            else:
                st.warning("Informe ao menos o EAN para salvar.")

    base_atual = carregar_base()
    if base_atual:
        st.write("Registros salvos na sua base local:")
        df_base = pd.DataFrame.from_dict(base_atual, orient='index')
        st.table(df_base)
