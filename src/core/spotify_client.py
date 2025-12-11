import os
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
                
                # Definimos los permisos necesarios (Scope)
                # user-modify-playback-state: para dar play/pause/next
                # user-read-playback-state: para ver qué suena
                scope = "user-modify-playback-state user-read-playback-state"
                
                cls._instance.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    scope=scope,
                    open_browser=False # Evita que abra el navegador cada vez si ya tiene token
                ))
            except Exception as e:
                print(f"Error inicializando Spotify: {e}")
                cls._instance.sp = None
                
        return cls._instance

    def play_song(self, query):
        if not self.sp:
            return "Error de conexión con Spotify"
            
        try:
            # 1. Buscar la canción
            results = self.sp.search(q=query, limit=1, type='track')
            tracks = results['tracks']['items']
            
            if not tracks:
                return f"No encontré la canción {query}"
            
            track_uri = tracks[0]['uri']
            track_name = tracks[0]['name']
            artist_name = tracks[0]['artists'][0]['name']
            
            # 2. Mandar orden de reproducción
            # IMPORTANTE: Spotify debe estar abierto en algún dispositivo (PC, Móvil)
            self.sp.start_playback(uris=[track_uri])
            return f"Reproduciendo {track_name} de {artist_name}"
            
        except spotipy.exceptions.SpotifyException as e:
            if "NO_ACTIVE_DEVICE" in str(e):
                return "Abre Spotify en tu ordenador para que pueda controlarlo."
            return f"Error de Spotify: {e}"