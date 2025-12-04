import webbrowser
from urllib.parse import quote_plus
import json

def ejecutar_abrir_youtube(parametro_busqueda: str):
        if not parametro_busqueda:
            print("ERROR: Parámetro de búsqueda no proporcionado para Abrir Youtube.")
            return

        # 1. Codificar el parámetro para que sea seguro en la URL
        busqueda_codificada = quote_plus(parametro_busqueda)
        
        # 2. Construir la URL completa
        URL_BASE = "https://www.youtube.com/results?search_query="
        url_completa = URL_BASE + busqueda_codificada
        
        # 3. Abrir en el navegador predeterminado (función multiplataforma)
        print(f"Abriendo navegador con búsqueda: {url_completa}")
        webbrowser.open(url_completa)