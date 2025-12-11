import os
import sys
from openai import OpenAI, APIError, APIConnectionError, RateLimitError, AuthenticationError
from dotenv import load_dotenv
from utils.paths_utils import get_config_path, get_prompts_path
from utils.file_manager import read_file, load_data
import json
import cv2
import base64

class OpenAIClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            try:
                load_dotenv(get_config_path())
            except Exception as e:
                print(f"Error al cargar el archivo .env: {e}")
                sys.exit(1)
            
            cls._instance.api_key = os.environ.get("OPENAI_API_KEY")
            try:
                cls._instance.client = OpenAI(api_key=cls._instance.api_key, timeout=90.0)
            except Exception as e:
                print(f"Error al inicializar el cliente de OpenAI: {e}")
                sys.exit(1)       
        return cls._instance     
    
    def __init__(self):
        pass

            
    def printOpenAIMessages(self, audio_text, commands):
        commands_json = json.dumps(commands, ensure_ascii=False, indent=2)
        system_prompt = read_file(get_prompts_path("system_prompt.md"))
        system_prompt = system_prompt.replace('{{COMANDOS_JSON}}', commands_json)
        
        messages=[
            {"role" : "system", "content" : system_prompt}            
        ]                           
        messages.extend(self._build_few_shoot())     
        messages.append({"role": "user", "content": audio_text})
        
        print(messages)
    
    def send_image(self, text, image, model="gpt-4.1", max_tokens=100, temperature=0.2):
        '''
        Llamada a openai para verificar que el gesto de la foto es el que se pide
        '''
                
        sucess, buffer = cv2.imencode('.png', image)
        base64_image = base64.b64encode(buffer).decode('utf-8')

        messages = [
            {
                "role" : "system",
                "content" : "Eres un sistema experto en analisis de imagenes. Di '<Si>' o '<No>' contestando a la pregunta, y despues en una frase corta describe exactamente lo que estas viendo"
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "high" 
                        }
                    }
                ]
            }
        ]
        
        try:    
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )            
            response_text = completion.choices[0].message.content
            print(response_text)
            return response_text
            
        except AuthenticationError as e:
            print(f"Error de autenticacion: API key invalida o incorrecta")
            print(f"   Detalles: {e}")
            sys.exit(1)
        
        except RateLimitError as e:
            print(f"Error: Has excedido tu limite de uso o cuota")
            print(f"   Detalles: {e}")
            sys.exit(1)
            
        except APIConnectionError as e:
            print(f"Error de conexion: No se pudo conectar con OpenAI")
            print(f"   Verifica tu conexion a internet")
            print(f"   Detalles: {e}")
            sys.exit(1)
            
        except APIError as e:
            print(f"Error de la API de OpenAI:")
            print(f"   Codigo: {e.status_code if hasattr(e, 'status_code') else 'N/A'}")
            print(f"   Mensaje: {e}")
            sys.exit(1)
            
        except Exception as e:
            print(f"Error inesperado: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            sys.exit(1)

    
    def send_commands(self, audio_text, commands, model="gpt-4.1", max_tokens=1000, temperature=0.7):
        '''
        Funcion para mandar a openai el texto transcrito para comprobar si hay algun comando que ejecutar
        '''
        
        commands_json = json.dumps(commands, ensure_ascii=False, indent=2)
        system_prompt = read_file(get_prompts_path("system_prompt.md"))
        system_prompt = system_prompt.replace('{{COMANDOS_JSON}}', commands_json)
        
        messages=[
            {"role" : "system", "content" : system_prompt}            
        ]                           
        messages.extend(self._build_few_shoot())     
        messages.append({"role": "user", "content": audio_text})
        
        try:    
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                response_format={"type": "json_object"} # Con esto le obligamos a que el formato que nos mande sea json
            )            
            response_text = completion.choices[0].message.content
            return json.loads(response_text)
            
        except AuthenticationError as e:
            print(f"Error de autenticacion: API key invalida o incorrecta")
            print(f"   Detalles: {e}")
            sys.exit(1)
        
        except RateLimitError as e:
            print(f"Error: Has excedido tu limite de uso o cuota")
            print(f"   Detalles: {e}")
            sys.exit(1)
            
        except APIConnectionError as e:
            print(f"Error de conexion: No se pudo conectar con OpenAI")
            print(f"   Verifica tu conexion a internet")
            print(f"   Detalles: {e}")
            sys.exit(1)
            
        except APIError as e:
            print(f"Error de la API de OpenAI:")
            print(f"   Codigo: {e.status_code if hasattr(e, 'status_code') else 'N/A'}")
            print(f"   Mensaje: {e}")
            sys.exit(1)
            
        except Exception as e:
            print(f"Error inesperado: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            sys.exit(1)
            
    def _build_few_shoot(self):       
        '''
        Funcion para crear mensajes de ejemplo para que openai genere una respuesta exacta
        ''' 
        data = load_data("multishot_comandos_delay.json")
        messages = []
        for message in data:
            if message.get("role") == "assistant":
                message["content"] = json.dumps(message["content"])      
            
            messages.append(message)
            
        return messages