
from core.voice import Voice
from core.facial import Facial
import numpy as np
from unidecode import unidecode
from utils.audio_phrases import *
import time

class User:
    def __init__(self):
        self.nickname = ""
        self.name = ""
        self.last_name = ""
        self.face_code = None
        
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.nickname == other.nickname
    
    def __hash__(self):
        return hash(self.nickname)
    
    def initialize(self, nick, name, last_name, face_code):
        self.nickname = nick
        self.name = name
        self.last_name = last_name
        self.face_code = face_code
    
    def to_dict(self):
        face_data = self.face_code
        if hasattr(face_data, 'tolist'):
            face_data = face_data.tolist()
            
        return {
            "nickname": self.nickname,
            "name": self.name,
            "last_name": self.last_name,
            "face_code": face_data
        }
    
    def from_dict(self, data):
        self.nickname = data["nickname"]
        self.name = data["name"]
        self.last_name = data["last_name"]
        
        raw_face_code = data.get("face_code")
        if raw_face_code and isinstance(raw_face_code, list):
            self.face_code = np.array(raw_face_code)
        else:
            self.face_code = None
        
    def print_info(self):
        print(f"- Usuario: {self.nickname}, Nombre: {self.name}, Apellidos: {self.last_name}, Code: {self.face_code}")

class Login:
    def __init__(self, users):
        self.users = users
        self.user_logged = None
        self.voice = Voice()
        self.facial = Facial()
        
    def login_user(self):
        if len(self.users) > 0:
            user = self.check_face()
            if user is not None:
                self.user_logged = user
                self.voice.talk(f"Bivenido al sistema {user.name}")
                return True
                
            self.voice.talk("Bienvenido. Digame su nombre de usuario")
            user_name = self.voice.listen().replace(" ", "")
            
            if user_name in self.users:
                self.user_logged = self.users[user_name]
                self.voice.talk(f"Inicio de sesion correcto. Buenos dias {self.user_logged.name}. Por favor pongase delante de la camara para verificar que es usted")
                if self.check_user_face(self.user_logged):
                    self.voice.talk(f"Perfecto {self.user_logged.name} ya esta logueado en el sistema")
            else:
                self.voice.talk(f"El nombre del usuario {user_name} no existe en la base de datos. ¿Quiere registrarte?")
                confirmation = self.voice.listen()
                if any(phrase in confirmation for phrase in get_confirmation_phrases()):
                    self.voice.talk(f"Perfecto, vamos a registrarte")
                    return self.register_user()
                else:
                    self.voice.talk(f"Pues hasta luego")
                    return False
        else:
            self.voice.talk(f"No hay registrados usuarios nuevos. ¿Quieres registrarte?")
            confirmation = self.voice.listen()
            if any(phrase in confirmation for phrase in get_confirmation_phrases()):
                self.voice.talk(f"Perfecto, vamos a registrarte")
                return self.register_user()
            else:
                self.voice.talk(f"Pues hasta luego")
                return False
                
    def register_user(self):
        nickname = self._register_nickname()
        name = self._register_name()
        last_name = self._register_last_name()
        photo_code = self._register_photo()
        user = User()
        user.initialize(nick=nickname, name=name, last_name=last_name, face_code=photo_code)
        self.user_logged = user
        self.users[nickname] = user
        self.voice.talk(f"Usuario {nickname} registrado.")
        UserUtils.save_users(self.users, "users.json")
        return True
            
    def _register_nickname(self):
        exit = False
        nickname = ""
        
        self.voice.talk(f"Dime tu nombre de usuario")
        while not exit:            
            n = self.voice.listen().replace(" ", "")
            self.voice.talk(f"¿Es {n} tu nombre de usuario?")
            confirmation = self.voice.listen()
            print(confirmation)
            if any(phrase in confirmation for phrase in get_confirmation_phrases()):
                nickname = n
                exit = True
            else:
                self.voice.talk(f"Vale, pues repitemelo de nuevo")
        
        return nickname
    
    def _register_name(self):
        exit = False
        name = ""
        
        self.voice.talk(f"Dime tu nombre")
        while not exit:            
            n = self.voice.listen()
            self.voice.talk(f"¿Es {n} tu nombre?")
            confirmation = self.voice.listen()
            if any(phrase in confirmation for phrase in get_confirmation_phrases()):
                name = n
                exit = True
            else:
                self.voice.talk(f"Vale, pues repitemelo de nuevo")        
        return name
    
    def _register_last_name(self):
        exit = False
        last_name = ""
        
        self.voice.talk(f"Dime tus apellidos")
        while not exit:            
            n = self.voice.listen()
            self.voice.talk(f"¿Son {n} tus apellidos?")
            confirmation = self.voice.listen()
            if any(phrase in confirmation for phrase in get_confirmation_phrases()):
                last_name = n
                exit = True
            else:
                self.voice.talk(f"Vale, pues repitemelos de nuevo")        
        return last_name
    
    def _register_photo(self):
        self.voice.talk(f"Ahora vamos a registrar tu cara en el sistema. Colocate delante de la camara en cuanto suene el primer pitito. Despues espera a un segundo antes de quitarte")
        time.sleep(0.5)
        #photo = self.facial.take_photo("user.png")
        photo = self.facial.open_webcam()
        photo = self.facial.assign_color_profile(photo)
        photo_code = self.facial.get_cod_face(photo)
        return photo_code
            
    def check_face(self):
        photo = self.facial.take_photo("user.png")
        photo = self.facial.assign_color_profile(photo)
        photo_code = self.facial.get_cod_face(photo)
        
        if photo_code is not None:        
            for user in self.users.values():
                if user.face_code is not None and self.facial.is_the_same(user.face_code, photo_code):
                    return user            
            return None
        else:
            return None
        
    def check_user_face(self, user):
        photo = self.facial.take_photo("user.png")
        photo = self.facial.assign_color_profile(photo)
        photo_code = self.facial.get_cod_face(photo)
        
        if photo_code is not None:        
            if user.face_code is not None and self.facial.is_the_same(user.face_code, photo_code):
                return True
        else:
            return False
        
    def _exist_users(self):
        return len(self.users) > 0
    
    
class UserUtils:    
    @staticmethod
    def load_users(file):
        from utils.file_manager import load_data
        users_json = load_data(file)
        users = {}
        
        if users_json:
            for user_data in users_json:
                user = User()
                user.from_dict(user_data)
                users[user.nickname] = user         
        return users

    @staticmethod
    def save_users(users, file):
        from utils.file_manager import save_data
        data = [user.to_dict() for user in users.values()]
        save_data(data, file)
        
    @staticmethod
    def print_users(users):
        for user in users.values():
            user.print_info()
    
    
class Register:
    def __init__(self):
        pass
    
    
        # def record_words(self):
    #     stop = False
    #     while not stop:
    #         #Activar el micro y guardar la request en un string
    #         self.talk("Bienvenido. Digame su nombre de usuario")
    #         usuario = self.listen().lower()
    #         usuario = unidecode(usuario)
    #         print(f"Su usuario es {usuario}")
    #         self.talk(f"Es su nombre de usuario {usuario}")
    #         confirmation = self.listen().lower()
    #         confirmation = unidecode(confirmation)
    #         print(f"Confirmacion: {confirmation}")
    #         if "si" in confirmation:
    #             self.registered_users.append({"User": usuario})
    #             save_users(self.registered_users)
    #             stop = True