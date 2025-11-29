from pygame import mixer
from utils.paths_utils import get_sounds_path

class Sound:
    _instance = None   
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sound, cls).__new__(cls)
            cls._instance.START_SOUND = get_sounds_path("start_beep.mp3")
            cls._instance.END_SOUND = get_sounds_path("stop_beep.mp3")
            mixer.init()
        return cls._instance

    def __init__(self):
        pass

    def play_sound(self, file_path, volume=0.3):
        sound_obj = mixer.Sound(file_path)        
        sound_obj.set_volume(volume)        
        sound_obj.play()