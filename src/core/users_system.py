
from core.voice import Voice
from core.facial import Facial
import numpy as np

class User:
    def __init__(self):
        self.nickname = ""
        self.name = ""
        self.last_name = ""
        self.face_code = ""
        
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.nickname == other.nickname
    
    def __hash__(self):
        return hash(self.nickname)
    
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
        
    def login_user():
        pass
        
    def _exist_users(self):
        return len(self.users) > 0
    
    def login(self):
        pass
    
    
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