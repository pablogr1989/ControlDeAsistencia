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
            users = json.load(j)
            return users
            
    except FileNotFoundError:
        print(f"No se encontró el archivo {file_path}")
        return []
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON")
        return []