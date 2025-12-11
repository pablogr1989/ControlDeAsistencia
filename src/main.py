from core.voice import *
from core.facial import Facial
from utils.file_manager import *
from utils.paths_utils import *
from core.users_system import Login, UserUtils
from core.command_manager import CommandManager
from core.attendance_system import AttendanceManager
from core.openai_client import OpenAIClient
import time
import sys

def main():
    print("============================================")
    print("=          CONTROL DE ASISTENCIA           =")
    print("============================================")    
    try:    
        attendance = AttendanceManager()
        voice = Voice()
        facial = Facial()
        sound_player = Sound()
        openai = OpenAIClient()
        users = UserUtils.load_users("users.json")    
        login = Login(users)
        command_manager = CommandManager()
        
    except RuntimeError as e:
        print(f"\n[ERROR CRÍTICO] {e}")
        print("No se puede iniciar el sistema. Cerrando aplicación...")
        sys.exit(1)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        sys.exit(1)
    
    if login.login_user():
        try:
            attendance.register_entry(login.user_logged)
            voice.talk(f"Sistema de comandos activado. Di Sistema para indicar cualquier comando")
            command_manager.start_listen()
            
            while not command_manager.exit:
                cmd = command_manager.get_next_command()
                if cmd:
                    print(cmd.print())
                    command_manager.process_command(cmd)
                else:
                    time.sleep(0.05)
                    
        except KeyboardInterrupt:
            print("\nInterrupción de teclado detectada.")

        finally:
            voice.talk(f"Cerrando el sistema de reconocimiento de comandos...")
            command_manager.stop_listen()
            time.sleep(1)
            voice.talk(f"Hasta la vista")
            time.sleep(1)        
        return

if __name__ == '__main__':
    main()