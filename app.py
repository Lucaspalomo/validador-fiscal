with tab2:
    arquivo = st.file_uploader("Suba o XML da NF-e", type=['xml'])
    if arquivo:
        # Lê e processa o XML usando a função do core.py
        itens = processar_xml_nfe(arquivo.read())
        
        if itens:
            df = pd.DataFrame(itens)
            st.write(f"Itens encontrados: {len(df)}")
            st.dataframe(df, use_container_width=True)
            
            if st.button("🚀 Iniciar Auditoria Completa"):
                for item in itens:
                    with st.expander(f"📦 Item {item['Item']} - {item['Descrição']}"):
                        with st.spinner("IA analisando NCM/CEST..."):
                            # Aumentamos o tempo para 12 segundos para garantir que não trave
                            time.sleep(12) 
                            
                            prompt = f"""
                            Analise o seguinte item de nota fiscal:
                            Produto: {item['Descrição']}
                            NCM informado: {item['NCM']}
                            
                            Verifique se o NCM está correto para este produto. 
                            Se estiver errado, sugira o NCM correto e o CEST correspondente.
                            Responda de forma curta e objetiva.
                            """
                            
                            # AQUI A MÁGICA ACONTECE:
                            resposta = consultar_gemini(prompt)
                            st.info(resposta)
        else:
            st.error("Erro ao ler o XML. Verifique se é um arquivo de NF-e válido.")