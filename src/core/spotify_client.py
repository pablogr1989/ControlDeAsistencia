import os
import time
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from utils.paths_utils import get_config_path

class SpotifyClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SpotifyClient, cls).__new__(cls)
            try:
                load_dotenv(get_config_path())
                
                # Definimos los permisos necesarios
                scope = "user-modify-playback-state user-read-playback-state"
                
                cls._instance.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    scope=scope,
                    open_browser=False 
                ))
            except Exception as e:
                print(f"Error inicializando Spotify: {e}")
                cls._instance.sp = None
                
        return cls._instance

    def _get_active_device_id(self):
        """
        Método auxiliar para obtener un ID de dispositivo válido.
        Si no hay ninguno, intenta abrir Spotify y espera.
        """
        devices = self.sp.devices()
        
        # Si la lista de dispositivos está vacía, intentamos abrir Spotify
        if not devices['devices']:
            print("Spotify cerrado. Intentando abrir aplicación...")
            webbrowser.open("spotify:")
            time.sleep(5)
            devices = self.sp.devices()

        # Si sigue vacía después de intentar abrirlo
        if not devices['devices']:
            return None

        # 1. Prioridad: Devolver el que ya esté activo (reproduciendo)
        for d in devices['devices']:
            if d['is_active']:
                return d['id']
        
        # 2. Si ninguno está activo, devolvemos el primero disponible (suele ser este PC)
        return devices['devices'][0]['id']

    def play_song(self, query):
        if not self.sp:
            return "Error de conexión con Spotify"
            
        try:
            # 1. Obtener un dispositivo válido (o abrir la app si hace falta)
            device_id = self._get_active_device_id()
            
            if not device_id:
                return "No pude detectar ningún dispositivo de Spotify activo, incluso tras intentar abrirlo."

            # 2. Buscar la canción
            results = self.sp.search(q=query, limit=1, type='track')
            tracks = results['tracks']['items']
            
            if not tracks:
                return f"No encontré la canción {query}"
            
            track_uri = tracks[0]['uri']
            track_name = tracks[0]['name']
            artist_name = tracks[0]['artists'][0]['name']
            
            # 3. Mandar orden de reproducción AL DISPOSITIVO ESPECÍFICO
            print(f"Reproduciendo en dispositivo ID: {device_id}")
            self.sp.start_playback(device_id=device_id, uris=[track_uri])
            
            return f"Reproduciendo {track_name} de {artist_name}"
            
        except spotipy.exceptions.SpotifyException as e:
            return f"Error de Spotify: {e}"