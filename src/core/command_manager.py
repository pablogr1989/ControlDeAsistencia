from utils.file_manager import *
from utils.command_actions import *
from core.openai_client import OpenAIClient
from core.ollama_client import OllamaClient
from core.voice import Voice
import threading
from utils.audio_phrases import *
import json

class CommandManager:
    
    def __init__(self):
        self.commands = load_data("commands.json")
        self.command_list = []
        self.list_lock = threading.Lock()
        self.openai = OpenAIClient()
        self.ollama = OllamaClient()
        self.voice = Voice()
        self.exit = False
        self.stop_listening_func = None
        pass
    
    def start_listen(self):                
        self.stop_listening_func = self.voice.recognizer.listen_in_background(self.voice.micro, self._background_processor)
        
    def stop_listen(self):
        if self.stop_listening_func:
            self.stop_listening_func(wait_for_stop=False)
            self.stop_listening_func = None        
        
    def _background_processor(self, recognizer, audio):              
        try:            
            text = recognizer.recognize_google(audio, language='es-es')            
            print(text)
            if any(phrase in text for phrase in get_wake_phrases()):
                #response = self.ollama.call_ollama(commands=self.commands, audio_text=text)
                response = self.openai.call_openai(commands=self.commands, audio_text=text)
                print(f"OpenAI responde:\n {response}")
                commands = self.extract_commands(response)
                with self.list_lock:
                    for cmd in commands:
                        self.command_list.append(cmd)    
                    
            if any(phrase in text for phrase in get_exit_phrases()):
                print("Veo que quieres salir")
                self.exit = True
            
        except recognizer.UnknownValueError:
            print("[ERROR] No he entendido lo que me has dicho")
        except recognizer.RequestError:
            print("[ERROR] Fallo en el servicio de transcripción de Google.")
        except Exception as e:
            print(f"[ERROR] Procesando audio en fondo: {e}")
            
    def get_next_command(self):
        with self.list_lock:
            if self.command_list:
                return self.command_list.pop(0)
        return None

    def extract_commands(self, response):
        # --- 1. Asegurar que data es un diccionario ---
        if isinstance(response, dict):
            data = response

        else:
            try:
                data = json.loads(response)
            except Exception as e:
                print(f"[ERROR] JSON inválido del LLM: {e}")
                return []

        comandos = data.get("comandos", [])
        if not isinstance(comandos, list):
            print("[ERROR] Formato de comandos inválido en la respuesta.")
            return []

        # Si vienen en formato simple (tu ejemplo)
        # {'comando': 'xx', 'parametro': 'yy'}
        # lo convierte al formato estándar
        for cmd in comandos:
            if "parametros" not in cmd:
                cmd["parametros"] = {"valor": cmd.get("parametro")}
            if "despues_de" not in cmd:
                cmd["despues_de"] = None

        # --- 2. Ordenar según dependencias ---
        ordered = []
        pendientes = {i: cmd for i, cmd in enumerate(comandos, start=1)}
        ejecutados = set()

        while pendientes:
            progreso = False

            for cmd_id, cmd in list(pendientes.items()):
                depende = cmd.get("despues_de")

                if depende is not None and depende not in ejecutados:
                    continue

                ordered.append(cmd)
                ejecutados.add(cmd_id)
                del pendientes[cmd_id]
                progreso = True

            if not progreso:
                print("[ERROR] Dependencias circulares.")
                break

        return ordered
