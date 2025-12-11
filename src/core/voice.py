import speech_recognition as sr
import pyttsx3
from unidecode import unidecode
from utils.sound import Sound

class Voice:
    _instance = None
    
    def __new__(cls):
            if cls._instance is None:
                cls._instance = super(Voice, cls).__new__(cls)
                cls._instance.sound = Sound()
                cls._instance.recognizer = sr.Recognizer()
                cls._instance.recognizer.pause_threshold = 0.8
                                
                try:
                    cls._instance.micro = sr.Microphone()
                    
                    with cls._instance.micro as source:
                        cls._instance.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                        
                except OSError as e:
                    raise RuntimeError(f"No se detecta ningún micrófono conectado o configurado.")
                except Exception as e:
                    raise RuntimeError(f"Error inesperado al iniciar el micrófono: {e}")
                    
            return cls._instance              
    
    def __init__(self):
        pass
            
    def listen(self):
        with self.micro as origin:                        
            # Informamos que comienza la grabación            
            self.sound.play_sound(self.sound.START_SOUND)                       
            try:
                audio = self.recognizer.listen(origin)
                self.sound.play_sound(self.sound.END_SOUND)
                text = self.recognizer.recognize_google(audio, language='es-es')
                text = unidecode(text).lower()
                print(f" Listen: {text}")
                return text
            except sr.UnknownValueError:
                print('Ups, no te entendí')
                return "Error"
            except sr.RequestError:
                print('Ups, sin servicio')
                return "Error"
            except:
                print('Ups, algo ha salido mal')
                return "Error"
            
    def set_mode_background(self):
        # Antigua configuracion dejada por si acaso vuelve a fallar
        # with self.micro as source:
        #     self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            
        # self.recognizer.energy_threshold = self.recognizer.energy_threshold * 100
        # self.recognizer.pause_threshold = 2
        
        # Nueva configuracion para modo background
        self.recognizer.non_speaking_duration = 0.7
        self.recognizer.pause_threshold = 1
            
    def talk(self, msg):
        newVoiceRate = 180
        engine = pyttsx3.init()
        
        engine.setProperty('voice', 'com.apple.eloquence.es-ES.Monica')
        engine.setProperty('rate', newVoiceRate)
        print(msg)
        engine.say(msg)
        engine.runAndWait()