import cv2
from utils.sound import Sound
from utils.paths_utils import get_photos_path
import time
import face_recognition as fr

class Facial:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Facial, cls).__new__(cls)
            cls._instance.camara = cv2.VideoCapture(0)
            cls._instance.sound = Sound()
            
        return cls._instance   
    
    def __init__(self):
        pass        
        
    def take_photo(self, file_name):
        self.sound.play_sound(self.sound.START_SOUND)
        time.sleep(0.5)
        exito, frame = self.camara.read()
        self.sound.play_sound(self.sound.END_SOUND)
        if exito:
            return frame
        
        print("No he hecho foto")
        return None

    def assign_color_profile(self, photo):
        return cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    
    def get_cod_face(self, photo):
        codes = fr.face_encodings(photo)
        if len(codes) > 0:
            return codes[0]
    
    # Por defecto, el valor de la distancia para determinar si es true o false es 0.6
    def is_the_same(self, user_code, photo_code):
        results = fr.compare_faces([user_code], photo_code)
        return results[0]