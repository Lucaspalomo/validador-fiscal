# 📊 Validador Fiscal Inteligente (Gemini AI + Streamlit)

Este projeto foi desenvolvido para automatizar a auditoria de cadastros fiscais (NCM e CEST) em sistemas ERP, utilizando Inteligência Artificial para validar dados e reduzir erros tributários em notas fiscais (NF-e).

## 🚀 Funcionalidades

- **🔎 Consulta Unitária:** Validação instantânea de NCM e CEST via EAN-13 ou descrição do produto utilizando o modelo Gemini 2.0 Flash.
- **📂 Processamento de XML (NF-e):** Upload de arquivos XML para extração automática de itens e auditoria em lote.
- **💾 Base de Conhecimento Local:** Sistema de "cache" em JSON que armazena correções manuais, evitando consultas repetitivas à IA e garantindo rapidez no suporte.
- **🛡️ Tratamento de Erros:** Gestão de limites de API (Rate Limit 429) e suporte a caracteres especiais (UTF-8).

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Framework Web:** Streamlit
- **Inteligência Artificial:** Google Gemini API (Generative AI)
- **Manipulação de Dados:** Pandas e XML ElementTree
- **Persistência:** JSON (NoSQL Style)

## 📦 Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/validador-fiscal.git](https://github.com/SEU_USUARIO/validador-fiscal.git)# validador-fiscal
