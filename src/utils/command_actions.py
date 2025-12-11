import webbrowser
from urllib.parse import quote_plus
from utils.time_utils import parsear_tiempo
import json
import subprocess
import os
import time
import sys
import threading
import winsound
import pyautogui
from core.spotify_client import SpotifyClient

PROGRAMAS = {
    "calculadora": "calc.exe",
    "bloc de notas": "notepad.exe",
    "paint": "mspaint.exe",
    "navegador": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
}

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
        
def ejecutar_programa(nombre):
    """
    Busca el nombre en el diccionario y lanza el proceso sin bloquear el asistente.
    """
    if not nombre:
        print("Error: Nombre de programa vacío.")
        return

    key = nombre.lower().strip()
    ruta = PROGRAMAS.get(key)

    if ruta:
        print(f"[ACCION] Iniciando {key}...")
        try:
            # Popen lanza el proceso y permite que Python siga ejecutándose
            subprocess.Popen(ruta)
        except FileNotFoundError:
            print(f"Error: No se encontró el ejecutable en: {ruta}")
        except Exception as e:
            print(f"Error lanzando programa: {e}")
    else:
        print(f"Advertencia: No tengo configurada la ruta para '{nombre}'.")
        print(f"Disponibles: {list(PROGRAMAS.keys())}")

def ejecutar_alarma(tiempo_str):
    """
    Recibe '3 minutos' o '1 hora', calcula los segundos 
    y programa el sonido en un hilo aparte.
    """
    segundos = parsear_tiempo(tiempo_str)
    
    if segundos > 0:
        print(f"[SISTEMA] Alarma configurada para dentro de {segundos} segundos.")
        # Programamos que suene CUANDO pase el tiempo
        t = threading.Timer(segundos, _sonar_pitidos_alarma, args=[tiempo_str])
        t.start()
    else:
        print(f"[ERROR] No he entendido el tiempo de la alarma: {tiempo_str}")

def _sonar_pitidos_alarma(tiempo_original):
    """Esta es la función que realmente hace ruido"""
    print(f"\n[ALARMA] ¡Han pasado {tiempo_original}! ⏰")
    
    # Lógica de sonido
    try:
        for _ in range(5):
            winsound.Beep(1000, 500)
            time.sleep(0.1)
    except Exception:
        print("\a" * 5) # Fallback
        
def ejecutar_reproducir_spotify(cancion):
    if not cancion:
        print("ERROR: No se ha especificado ninguna canción.")
        return
    
    client = SpotifyClient()
    result = client.play_song(cancion)
    print(result)