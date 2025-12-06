import json
from .paths_utils import *

def save_data(data, file):
    file_path = get_data_path(file)
    with open(file_path, "w") as j:
        json.dump(data, j)
        
def load_data(file):
    try:
        file_path = get_data_path(file)
        with open(file_path, "r", encoding="utf-8") as j:
            data = json.load(j)
            return data
            
    except FileNotFoundError:
        print(f"No se encontró el archivo {file_path}")
        return []
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON")
        return []
    
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            template = f.read()
            return template
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_path}'.")
        return None
    except Exception as e:
        print(f"Error inesperado al generar el prompt: {e}")
        return None