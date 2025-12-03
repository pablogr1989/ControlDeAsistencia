import speech_recognition as sr
import pyttsx3
from utils.sound import Sound

class Voice:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Voice, cls).__new__(cls)
            cls._instance.sound = Sound()
            cls._instance.recognizer = sr.Recognizer()
            cls._instance.micro = sr.Microphone()
            with cls._instance.micro as source:
                cls._instance.recognizer.adjust_for_ambient_noise(source, duration=1.5)
                
            cls._instance.recognizer.energy_threshold = cls._instance.recognizer.energy_threshold * 50
            cls._instance.recognizer.pause_threshold = 2
            cls._instance.recognizer.non_speaking_duration = 2
            
        return cls._instance    
    
    def __init__(self):
        pass

            
    def listen(self):    
        # Recognizer   
        # Configuramos el micro
        with self.micro as origin:                        
            # Informamos que comienza la grabación
            self.sound.play_sound(self.sound.START_SOUND)                       
            try:
                audio = self.recognizer.listen(origin, phrase_time_limit=None)
                self.sound.play_sound(self.sound.END_SOUND)
                text = self.recognizer.recognize_google(audio, language='es-es')
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
            
    def talk(self, msg):
        newVoiceRate = 180
        
        # Encender motor pyttsx3
        engine = pyttsx3.init()
        
        engine.setProperty('voice', 'com.apple.eloquence.es-ES.Monica')
        engine.setProperty('rate', newVoiceRate)
        # Pronunciar mensjaje
        engine.say(msg)
        engine.runAndWait()