import cv2
from utils.sound import Sound
from utils.paths_utils import get_photos_path
import time
import face_recognition as fr
from core.voice import Voice

class Facial:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Facial, cls).__new__(cls)
            cls._instance.camara = cv2.VideoCapture(0)
            
            if not cls._instance.camara.isOpened():
                raise RuntimeError("No se detecta ninguna cámara web conectada.")
            
            cls._instance.sound = Sound()
            cls._instance.voice = Voice()
            
        return cls._instance   
    
    def __init__(self):
        pass        
    
    def take_single_face(self):
        problem_start = None       # Contador para abortar (20s de problemas continuos)
        success_start = None       # Contador para éxito (3s de cara correcta)
        multi_face_start = None    # Contador para aviso de múltiples caras (5s)
        
        last_reported_sec = 0      # Control de pitidos
        warned_multi_face = False  # Evitar repetir aviso de voz
        
        while True:
            ret, frame = self.camara.read()
            if ret:
                locations = self.locate_faces(frame)
                
                # Si locations es None, asumimos 0 caras
                num_faces = len(locations) if locations else 0
                
                # Si hay 0 caras o mas de 1, no es valido, asi que empieza el contador para abortar
                if num_faces != 1:
                    if problem_start is None:
                        problem_start = time.time()
                    
                    if time.time() - problem_start > 20:
                        self.voice.talk("No se ha podido detectar una cara válida durante demasiado tiempo. Cancelando.")
                        cv2.destroyAllWindows()
                        return None
                else:
                    # Si hay 1 cara, reseteamos el contador de problemas
                    problem_start = None
                
                # Escenario A - Una sola cara
                if num_faces == 1:
                    # Resetear contadores de error
                    multi_face_start = None
                    warned_multi_face = False
                    
                    if success_start is None:
                        success_start = time.time()
                        last_reported_sec = 0
                    
                    elapsed_time = time.time() - success_start
                    
                    # ÉXITO: 5 segundos
                    if elapsed_time >= 5:
                        self.sound.play_sound(self.sound.END_SOUND)
                        cv2.destroyAllWindows()
                        return frame
                    
                    # Pitidos de progreso
                    if int(elapsed_time) > last_reported_sec:
                        self.sound.play_sound(self.sound.START_SOUND)
                        last_reported_sec = int(elapsed_time)
                    
                    self.draw_rectangles(frame, locations, color=(0, 255, 0))

                # Escenario B, multiples caras
                elif num_faces > 1:
                    success_start = None
                    last_reported_sec = 0
                    
                    if multi_face_start is None:
                        multi_face_start = time.time()
                    
                    if (time.time() - multi_face_start > 5) and not warned_multi_face:
                        self.voice.talk("Solo puede registrar una cara")
                        warned_multi_face = True
                    
                    self.draw_rectangles(frame, locations, color=(0, 0, 255))

                # Escenario C, ninguna cara
                else:
                    success_start = None
                    multi_face_start = None
                    last_reported_sec = 0
                    warned_multi_face = False

                imS = self.resize_with_aspect_ratio(frame, width=480) 
                cv2.imshow('Webcam', imS)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    return None
            else:
                print("Error: No se pudo leer el fotograma.")
                break
    
    def take_photo(self):
        init_time = time.time()
        start_time = None
        abort_time = time.time()
        last_reported_sec = 0
        last_noface_sec = 0
        
        while True:
            ret, frame = self.camara.read()
            if ret:               
                locations = self.locate_faces(frame)
                if locations is not None:
                    self.draw_rectangles(frame, locations)
                    
                    if start_time is None:
                        start_time = time.time()
                        last_reported_sec = 0
                        abort_time = None
                        last_noface_sec = 0
                    
                    elapsed_time = time.time() - start_time
                    
                    if elapsed_time >= 5:
                        self.sound.play_sound(self.sound.END_SOUND)
                        cv2.destroyAllWindows()
                        time.sleep(1)
                        cv2.imwrite(get_photos_path("user.png"), frame)
                        return frame
                    
                    if int(elapsed_time) > last_reported_sec:
                        self.sound.play_sound(self.sound.START_SOUND)
                        last_reported_sec = int(elapsed_time)
                        
                    self.draw_rectangles(frame, locations)
                else:
                    # Si deja de detectar la cara, reiniciamos el contador inmediatamente
                    if start_time is not None:
                        start_time = None
                        last_reported_sec = 0
                        abort_time = time.time()
                        last_noface_sec = 0
                        self.voice.talk("No hemos detectado su cara. Por favor pongase delante de la camara")
                    else:
                        # Conforme pase el tiempo y no reconozca la cara, aumentaremos el tiempo para abortar
                        elapsed_time = time.time() - abort_time
                        last_noface_sec = int(elapsed_time)
                    
                imS = self.resize_with_aspect_ratio(frame, width=720) 
                cv2.imshow('Webcam', imS)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    return frame
            else:
                print("Error: No se pudo leer el fotograma.")
                
            if last_noface_sec > 20:
                self.voice.talk("Parece que hay problemas reconociendo su cara. Intentelo en unos minutos")
                cv2.destroyAllWindows()
                return None
            
    def draw_rectangles(self, photo, locations, color=(0, 255, 0)):
        for l in locations:
            cv2.rectangle(photo,
                        (l[3], l[0]),
                        (l[1], l[2]),
                        color, 2)
        
    def locate_faces(self, photo):
        locations = fr.face_locations(photo)
        if locations:
            return locations
        else:
            return None

    def assign_color_profile(self, photo):
        return cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    
    def get_cod_face(self, photo):
        codes = fr.face_encodings(photo)
        if codes:
            return codes

    def is_the_same(self, user_code, photo_code):
        results = fr.compare_faces([user_code], photo_code)
        distance = fr.face_distance([user_code], photo_code)
        return results[0]
    
    def resize_with_aspect_ratio(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)