import xml.etree.ElementTree as ET

def processar_xml_nfe(conteudo_xml):
    try:
        root = ET.fromstring(conteudo_xml)
        # O {*} faz a mágica de ignorar o link do portal fiscal e pegar só o nome da tag
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'} 
        
        itens = []
        # Procura todos os produtos na nota
        for i, det in enumerate(root.findall(".//{*}det"), start=1):
            prod = det.find(".//{*}prod")
            item = {
                "Item": i,
                "Descrição": prod.find("{*}xProd").text,
                "NCM": prod.find("{*}NCM").text,
                "EAN": prod.find("{*}cEAN").text if prod.find("{*}cEAN") is not None else "SEM GTIN"
            }
            itens.append(item)
        return itens
    except Exception as e:
        print(f"Erro ao ler XML: {e}")
        return []