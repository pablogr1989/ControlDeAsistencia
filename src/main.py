from core.voice import *
from core.facial import Facial
from utils.file_manager import *
from utils.paths_utils import *
from core.users_system import Login, UserUtils
from core.command_manager import CommandManager
import time

def main():
    #start_time = time.time()
    voice = Voice()
    facial = Facial()
    sound_player = Sound()
    file_name = "users.json"
    users = UserUtils.load_users(file_name)    
    login = Login(users)
    command_manager = CommandManager()     
       
    user = users['teivko']    
    photo = facial.take_photo(user.nickname + ".png")
    photo = facial.assign_color_profile(photo)
    photo_code = facial.get_cod_face(photo)
    
    print(f"Foto actual:\n{photo_code}")
    print(f"\n\n")
    print(f"Foto usuario:\n{user.face_code}")
    
    if facial.is_the_same(user.face_code, photo_code):
        voice.talk(f"Bienvenido {user.name}")
    
    #UserUtils.save_users(users, file_name)
        
    return
  
    exit = False
    command_list = []
    
    
    
    # try:
    #     command_manager.start_listen()
        
    #     while not command_manager.exit:
    #         command = command_manager.get_next_command()
    #         if command:
    #             print(f"Ejecutando: {command['comando']}")
    #         else:
    #             time.sleep(0.1)
                
    # except KeyboardInterrupt:
    #     # Esto captura si el usuario pulsa Ctrl+C en la consola
    #     print("\nInterrupción de teclado detectada.")

    # finally:

    #     print("Cerrando recursos...")
    #     command_manager.stop_listen() 
    #     print("Programa terminado.")
    
    return       
    

        
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