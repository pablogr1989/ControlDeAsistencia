import speech_recognition as sr
import pyttsx3
from utils.sound import Sound

class Voice:        
    def __init__(self):
        self.sound = Sound()
            
    def listen(self):    
        # Recognizer
        r = sr.Recognizer()
        m = sr.Microphone()        
        # Configuramos el micro
        with m as origin:
            # Tiempo que espera para ver si has dejado de hablar
            r.pause_threshold = 2
            r.non_speaking_duration = 2
            
            # Durante 1.5 segundos graba el sonido para ver el cual es el nivel 
            # de ruido del ambiente y asi determinar que es silencio y que no
            r.adjust_for_ambient_noise(origin, duration=1.5)
            
            # Informamos que comienza la grabación
            print('Puedes comenzar a hablar')
            self.sound.play_sound(self.sound.START_SOUND) 
                       
            try:
                audio = r.listen(origin, phrase_time_limit=None)
                self.sound.play_sound(self.sound.END_SOUND)
                text = r.recognize_google(audio, language='es-es')
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
        
