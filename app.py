import streamlit as st
import pandas as pd
import core  # Importa a sua lógica do core.py
import time

# Configuração da página (deve ser a primeira instrução Streamlit)
st.set_page_config(page_title="Validador Fiscal", layout="wide")

# Título limpo e sem caracteres que causam erro de encoding
st.title("📊 Auditoria Fiscal")
st.markdown("---")

# Criação das abas
tab1, tab2, tab3 = st.tabs(["🔍 Consulta IA", "📄 Processar XML", "💾 Base de Dados"])

with tab1:
    st.header("Consulta com Inteligência Artificial")
    pergunta = st.text_input("O que deseja validar no NCM/CEST?")
    
    if st.button("Consultar IA"):
        if pergunta:
            with st.spinner("Analisando..."):
                # Aqui chama a função de IA que criamos no core.py
                resposta = core.consultar_ia(pergunta)
                st.write(resposta)
                time.sleep(1) # Delay para evitar erro de quota
        else:
            st.warning("Por favor, digite uma pergunta.")

with tab2:
    st.header("Análise de Arquivos XML")
    uploaded_file = st.file_uploader("Arraste seu XML de NF-e aqui", type=["xml"])
    
    if uploaded_file is not None:
        xml_content = uploaded_file.read()
        # Chama a função de limpeza que remove os links/namespaces
        dados_xml = core.processar_xml_nfe(xml_content)
        
        if dados_xml:
            df = pd.DataFrame(dados_xml)
            st.subheader("Itens Identificados")
            st.table(df) # Exibe a tabela limpa
        else:
            st.error("Não foi possível extrair dados deste XML.")

with tab3:
    st.header("Base de Conhecimento Local")
    # Exemplo de visualização da base local
    if st.button("Verificar Base"):
        base = core.carregar_base_local()
        st.json(base)

# Rodapé simples
st.sidebar.info("Versão 1.0 - Suporte Automações")