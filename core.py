import xml.etree.ElementTree as ET

def processar_xml_nfe(conteudo_xml):
    try:
        # Decodifica se necessário e carrega o XML
        root = ET.fromstring(conteudo_xml)
        
        itens = []
        # O {* } é um seletor universal que ignora o link do portal fiscal (Namespace)
        for i, det in enumerate(root.findall(".//{*}det"), start=1):
            prod = det.find(".//{*}prod")
            if prod is not None:
                item = {
                    "Item": i,
                    # O .text pega apenas o conteúdo, e o {*} ignora a URL técnica
                    "Descrição": prod.find("{*}xProd").text if prod.find("{*}xProd") is not None else "N/A",
                    "NCM": prod.find("{*}NCM").text if prod.find("{*}NCM") is not None else "N/A",
                    "EAN": prod.find("{*}cEAN").text if prod.find("{*}cEAN") is not None else "SEM GTIN"
                }
                itens.append(item)
        return itens
    except Exception as e:
        print(f"Erro ao processar: {e}")
        return []