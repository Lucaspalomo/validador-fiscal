import xml.etree.ElementTree as ET
import google.generativeai as genai
import json
import os
import io

DB_FILE = "base_conhecimento.json"

def configurar_ia(chave):
    genai.configure(api_key=chave)

def carregar_base():
    if os.path.exists(DB_FILE):
        # O 'encoding=utf-8' impede que os emojis virem '??'
        with open(DB_FILE, "r", encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def salvar_na_base(ean, dados):
    base = carregar_base()
    base[ean] = dados
    with open(DB_FILE, "w", encoding='utf-8') as f:
        # ensure_ascii=False permite salvar acentos e emojis corretamente
        json.dump(base, f, indent=4, ensure_ascii=False)

def processar_xml_nfe(xml_content):
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    try:
        # Decodifica garantindo que caracteres especiais do XML não quebrem
        root = ET.fromstring(xml_content)
        itens = []
        for det in root.findall('.//nfe:det', ns):
            prod = det.find('nfe:prod', ns)
            if prod is not None:
                itens.append({
                    "Item": det.attrib.get('nItem'),
                    "EAN": prod.findtext('nfe:cEAN', ns),
                    "Descrição": prod.findtext('nfe:xProd', ns),
                    "NCM": prod.findtext('nfe:NCM', ns),
                    "CEST": prod.findtext('nfe:CEST', ns) or "N/A"
                })
        return itens
    except Exception as e:
        return None

def consultar_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            # Retornamos um texto limpo sem emojis complexos para testar a estabilidade
            return "AVISO: Limite de consultas atingido. Aguarde alguns segundos antes de tentar o proximo item."
        return f"Erro na consulta: {str(e)}"