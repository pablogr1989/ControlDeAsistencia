from core.rec_voz import *
from core.openai_client import OpenAIClient
from core.ollama_client import OllamaClient
from core.rec_facial import Facial
from utils.file_manager import *
from core.command_actions import *
from utils.paths_utils import *
import time
import threading

def main():
    start_time = time.time()
    openai = OpenAIClient()
    ollama = OllamaClient()
    rec_voice = Voice()
    #rec_facial = Facial()
    sound_player = Sound()
    commands = load_data("commands.json")
    users = load_data("users.json")
    exit = False
    command_list = []
    list_lock = threading.Lock()
    
    
    def background_processor(recognizer, audio):         
        try:
            nonlocal exit, command_list
            nonlocal list_lock
            wake_phrases = ["hey sistema", "buenas sistema", "sistema me escuchas", "hola sistema", "sistema despierta"]
            
            # 1. Transcribir el audio
            text = recognizer.recognize_google(audio, language='es-es')
            print(f"He escuchado: {text}")
            
            if any(phrase in text for phrase in wake_phrases):
                response = ollama.call_ollama(commands=commands, audio_text=text)
                command = extract_command(response)
                with list_lock:
                    command_list.append(command)      
                      
            exit_phrases = ["exit", "salir del programa", "terminar programa", "terminar el programa", "abortar programa"]
            if any(phrase in text for phrase in exit_phrases):
                print("Veo que quieres salir")
                exit = True
            
            # if "sistema" in text.lower() or "hola" in text.lower():
                
            #     response_ollama = ollama.call_ollama(commands=commands, audio_text=text)
                
            #     if response_ollama:
            #         # Aquí va la lógica de extracción y ejecución de comandos
            #         first_command = response_ollama['comandos'][0]
            
        except sr.UnknownValueError:
            # Silencioso en modo fondo para no molestar si no se entendió
            pass 
        except sr.RequestError:
            print("[ERROR] Fallo en el servicio de transcripción de Google.")
        except Exception as e:
            print(f"[ERROR] Procesando audio en fondo: {e}")
            
    rec_voice.recognizer.listen_in_background(rec_voice.micro, background_processor)

        
    while not exit:
        # 1. Verificar si hay comandos
        if command_list:            
            with list_lock:
                command = command_list.pop(0)
                if command.get('comando') == "open_youtube":
                    rec_voice.talk(command.get('frase_de_vuelta'))
                    ejecutar_abrir_youtube(command['parametro'])
                
        else:
            time.sleep(0.05)
        # end_time = time.time()
        # print(f"He tardado: {end_time-start_time}")
        # text = rec_voice.listen()
        # print(f"He escuchado: {text}")
        # if text != "Error":
        #     response_ollama = ollama.call_ollama(commands=commands, audio_text=text)
        #     #response_open = openai.call_openai(commands=commands, audio_text=text)
        #     print(f"Ollama dice: {response_ollama}")
        #     #print(f'OpenAI dice: {response_open}')
        #     first_command = extract_command(response_ollama)
                
        #     # 4. Verificar el valor del campo 'comando'
        #     if first_command.get('comando') == "initial_greetings":
        #         rec_voice.talk(first_command.get('frase_de_vuelta'))
                
        #         text = rec_voice.listen()
        #         print(f"He escuchado: {text}")
        #         response = ollama.call_ollama(commands=commands, audio_text=text)
        #         #response = openai.call_openai(commands=commands, audio_text=text)
        #         print(f"Ollama dice: {response}")
        #         command = extract_command(response)
        #         # Ejecución de la acción
        #         if command.get('comando') == "open_youtube":
        #             rec_voice.talk(command.get('frase_de_vuelta'))
        #             ejecutar_abrir_youtube(command['parametro'])
                
        #         # response = openai.call_openai(commands=commands, audio_text=text)
        #         # print(f"Respuesta: {response['response']}")
        #         # print(f"Tokens: {response['tokens']}") 
                
        #         # # Ejecución de la acción
        #         # if first_command['comando'] == "open_youtube":
        #         #     ejecutar_abrir_youtube(first_command['parametro'])
                
        #         return True
        #     else:
        #         print(f"Comando detectado: {first_command.get('comando')}")
        #         return True

if __name__ == '__main__':
    main()