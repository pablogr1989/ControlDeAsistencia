from utils.file_manager import *
from utils.command_actions import *
from core.openai_client import OpenAIClient
from core.ollama_client import OllamaClient
from core.voice import Voice
import threading

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
            wake_phrases = ["hey sistema", "buenas sistema", "sistema me escuchas", "hola sistema", "sistema despierta"]
            
            text = recognizer.recognize_google(audio, language='es-es')
            print(f"He escuchado: {text}")
            
            if any(phrase in text for phrase in wake_phrases):
                response = self.ollama.call_ollama(commands=self.commands, audio_text=text)
                command = extract_command(response)
                with self.list_lock:
                    self.command_list.append(command)      
                    
            exit_phrases = ["exit", "salir del programa", "terminar programa", "terminar el programa", "abortar programa"]
            if any(phrase in text for phrase in exit_phrases):
                print("Veo que quieres salir")
                self.exit = True
            
        except recognizer.UnknownValueError:
            # No me ha entendido, pero no voy a decir nada
            pass 
        except recognizer.RequestError:
            print("[ERROR] Fallo en el servicio de transcripción de Google.")
        except Exception as e:
            print(f"[ERROR] Procesando audio en fondo: {e}")
            
    def get_next_command(self):
        with self.list_lock:
            if self.command_list:
                return self.command_list.pop(0)
        return None
        