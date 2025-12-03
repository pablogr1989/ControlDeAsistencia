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
            print(get_photos_path(file_name))
            cv2.imwrite(get_photos_path(file_name), frame)
            return frame         


    def assign_color_profile(self, photo):
        return cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    
    def get_cod_face(self, photo):
        return fr.face_encodings(photo)[0]    
    
    # Por defecto, el valor de la distancia para determinar si es true o false es 0.6
    def is_the_same(self, user_code, photo_code):
        results = fr.compare_faces([user_code], photo_code)
        return results[0]

    # top, right, botton, left
    # def localizar_cara(fotos_list):
    #     locations = []
    #     for i in fotos_list:
    #         locations.append(fr.face_locations(i)[0]) #puede detectar más caras... nos quedamos con la primera
    #     return locations
    
    # Cargar imagenes
    # def cargar_imagenes(path_list):
    #     fotos = []
    #     for path in path_list:
    #         fotos.append(fr.load_image_file(path))
    #     return fotos

    # # (left, top), (right, bottom)
    # def draw_rectangles(fotos_list, locations):
    #     for (f, l) in zip(fotos_list, locations):
    #         cv2.rectangle(f,
    #                     (l[3], l[0]),
    #                     (l[1], l[2]),
    #                     (0, 255, 0), 2)

    # def show_imgs(fotos_list):
    #     for index, f in enumerate(fotos_list):
    #         cv2.imshow(f'Foto {index}', f)

    # Por defecto, el valor de la distancia para determinar si es true o false es 0.6
    # def compare_all_with_control(cara_cod_list):
    #     results = []
    #     for i,fc in enumerate(cara_cod_list):
    #         if i > 0:
    #             # Con fr.compare_faces([control_cod], cara_cod_comparar, 0.3) podemos modificar el límite por el que determinaría si es true
    #             diferencias = {'misma_cara': fr.compare_faces([cara_cod_list[0]], fc),
    #                         'distancia': fr.face_distance([cara_cod_list[0]], fc)}
    #         elif i == 0:
    #             diferencias = { 'misma_cara': 'control',
    #                             'distancia': '0'}
    #         results.append(diferencias)

    #     return results

    # def show_results(fotos_list, results):
    #     for d,f in zip(results, fotos_list):
    #         resultado = d['misma_cara']
    #         distancia = d['distancia'][0]
    #         cv2.putText(f, f'{resultado} :::: {distancia}',
    #                     (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)