import speech_recognition as sr
from utils.file_manager import *
from utils.command_actions import *
from core.openai_client import OpenAIClient
from core.ollama_client import OllamaClient
from core.voice import Voice
import threading
from utils.audio_phrases import *
import json
from urllib.parse import quote_plus
from utils.time_utils import *

class Command:
    def __init__(self):
        self.comando = None
        self.parametros = None
        self.delay = False
        self.delayType = None
        self.delayValue = None
        self.timeUnit = None
        
    def print(self):
        return f"<Command: {self.comando} | Params: {self.parametros} | Delay: {self.delay} ({self.delayValue} {self.timeUnit})>"

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
        self.actions = {
            "open_youtube": ejecutar_abrir_youtube,
            "run_program": ejecutar_programa,
            "set_alarm": ejecutar_alarma
        }
    
    
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
                #print(f"OpenAI responde:\n {response}")
                commands = self.extract_commands(response)
                with self.list_lock:
                    for cmd in commands:
                        self.command_list.append(cmd)    
                    
            if any(phrase in text for phrase in get_exit_phrases()):
                print("Veo que quieres salir")
                self.exit = True
                
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))      
        except Exception as e:
            print(f"[ERROR] Procesando audio en fondo: {e}")
            
    def get_next_command(self):
        with self.list_lock:
            if self.command_list:
                return self.command_list.pop(0)
        return None   
    
    def extract_commands(self, mensaje):
        try:
            #content_str = mensaje.get("content", "{}")
            data = mensaje
            raw_commands = data.get("comandos", [])
        except json.JSONDecodeError:
            print("Error: El contenido no es un JSON válido.")
            return []

        command_map = {}  
        dependency_map = {} 

        for item in raw_commands:
            cmd = Command()
            cmd.comando = item.get("comando")
            cmd.parametros = item.get("parametros", {}) 
            
            # Procesar delay si existe
            if "delay" in item and item["delay"]:
                cmd.delay = True
                cmd.delayType = item["delay"].get("tipo")
                cmd.delayValue = item["delay"].get("valor")
                cmd.timeUnit = item["delay"].get("medida")
            
            cmd_id = item.get("id")
            parent_id = item.get("despues_de")
            
            command_map[cmd_id] = cmd
            dependency_map[cmd_id] = parent_id

        ordered_commands = []
        processed_ids = set()

        # Repetimos mientras queden comandos por procesar
        while len(ordered_commands) < len(command_map):
            progress = False
            
            for cmd_id, cmd in command_map.items():
                if cmd_id in processed_ids:
                    continue
                
                parent_id = dependency_map[cmd_id]
                
                # Un comando está listo si no tienen dependencias, o si ya la hemos procesado
                if parent_id is None or parent_id in processed_ids:
                    ordered_commands.append(cmd)
                    processed_ids.add(cmd_id)
                    progress = True
            
            if not progress:
                # Evitar bucle infinito si hay dependencias circulares o IDs inexistentes
                print("Error: Dependencia circular o ID faltante detectado.")
                break
        
        return ordered_commands
        
    def process_command(self, cmd):
        if cmd.delay and cmd.delayValue:
            if cmd.delayType == "temporizador":
                seconds = convert_to_seconds(cmd.delayValue, cmd.timeUnit)
                print(f"--> Programando '{cmd.comando}' en {seconds} segundos...")
            elif cmd.delayType == "tiempo":
                seconds = convert_time_to_seconds(cmd.delayValue)
            
            # Ejecución no bloqueante en hilo aparte
            timer = threading.Timer(seconds, self._dispatch, args=[cmd])
            timer.start()
        else:
            # Ejecución inmediata
            self._dispatch(cmd)
            

    def _dispatch(self, cmd):
        action_func = self.actions.get(cmd.comando)        
        if action_func:
            valor = cmd.parametros.get("valor", "")
            try:
                action_func(valor)
            except Exception as e:
                print(f"Error ejecutando {cmd.comando}: {e}")
        else:
            print(f"Advertencia: Comando '{cmd.comando}' no implementado.")