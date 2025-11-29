import cv2
from utils.sound import Sound
from utils.paths_utils import get_photos_path
import time

class Facial:
    def __init__(self):
        self.camara = cv2.VideoCapture(0)
        self.sound = Sound()

        
    def take_photo(self):
        self.sound.play_sound(self.sound.START_SOUND)
        time.sleep(0.5)
        exito, frame = self.camara.read()
        self.sound.play_sound(self.sound.END_SOUND)
        if exito:
            cv2.imwrite(get_photos_path("captura.png"), frame)
