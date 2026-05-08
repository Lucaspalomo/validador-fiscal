import google.generativeai as genai
import xml.etree.ElementTree as ET

def configurar_ia(chave):
    genai.configure(api_key=chave)

def consultar_gemini(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# ... (restante das suas funções de XML e Base)