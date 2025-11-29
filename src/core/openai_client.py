import os
import sys
from openai import OpenAI, APIError, APIConnectionError, RateLimitError, AuthenticationError
from dotenv import load_dotenv
from utils.paths_utils import get_config_path
from utils.logger import logger
import json

class OpenAIClient:
    
    def __init__(self):
        try:
            load_dotenv(get_config_path())
        except Exception as e:
            logger.error(f"Error al cargar el archivo .env: {e}")
            sys.exit(1)
        
        self.api_key = os.environ.get("OPENAI_API_KEY")
        try:
            self.client = OpenAI(api_key=self.api_key, timeout=90.0)
        except Exception as e:
            logger.error(f"Error al inicializar el cliente de OpenAI: {e}")
            sys.exit(1)

    
    def call_openai(self, audio_text, commands, model="gpt-4.1", max_tokens=1000, temperature=0.7):
        
        messages=[
                    {"role": "user", "content": self._build_user_message(audio_text=audio_text, commands=commands)}
                ]        
        try:    
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                response_format={"type": "json_object"}
            )            
            response_text = completion.choices[0].message.content
            return json.loads(response_text)
                    
            return {
                "response": response_text,
                "model": completion.model,
                "tokens": {
                    "total": completion.usage.total_tokens,
                    "prompt": completion.usage.prompt_tokens,
                    "completion": completion.usage.completion_tokens
                }
            }
            
        except AuthenticationError as e:
            logger.error(f"Error de autenticacion: API key invalida o incorrecta")
            logger.error(f"   Detalles: {e}")
            sys.exit(1)
        
        except RateLimitError as e:
            logger.error(f"Error: Has excedido tu limite de uso o cuota")
            logger.error(f"   Detalles: {e}")
            sys.exit(1)
            
        except APIConnectionError as e:
            logger.error(f"Error de conexion: No se pudo conectar con OpenAI")
            logger.error(f"   Verifica tu conexion a internet")
            logger.error(f"   Detalles: {e}")
            sys.exit(1)
            
        except APIError as e:
            logger.error(f"Error de la API de OpenAI:")
            logger.error(f"   Codigo: {e.status_code if hasattr(e, 'status_code') else 'N/A'}")
            logger.error(f"   Mensaje: {e}")
            sys.exit(1)
            
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            logger.error(f"   Tipo de error: {type(e).__name__}")
            sys.exit(1)

    def _build_commands_table(self, commands):        
        # --- TABLA 1: Reglas de Extracción de Parámetros ---
        table_rows_params = ["| Comando | Intenciones Típicas | Descripción del Parámetro (`parametro`) |", 
                            "| :--- | :--- | :--- |"]
                        
        # --- TABLA 2: Instrucciones de Procesamiento Específicas (NUEVO) ---
        table_rows_inst = ["| Comando | Instrucción de Procesamiento Específica |", 
                        "| :--- | :--- |"]
        
        for item in commands:
            # Excluir el comando "No identificado" del prompt para no confundir al LLM
            if item.get("comando") == "No identificado":
                continue 
            
            # 1. Llenar la Tabla de Parámetros
            intenciones_str = ", ".join(item.get("intenciones", []))
            table_rows_params.append(
                f"| `{item.get('comando')}` | {intenciones_str} | {item.get('descripcion_parametro', 'No requiere') } |"
            )
            
            # 2. Llenar la Tabla de Instrucciones Específicas
            table_rows_inst.append(
                f"| `{item.get('comando')}` | {item.get('instruccion_llm', 'Ninguna.') } |"
            )
                
        return "\n".join(table_rows_params), "\n".join(table_rows_inst)


    def _build_user_message(self, audio_text, commands):        
        # Generar las dos tablas
        commands_table_markup, instructions_table_markup = self._build_commands_table(commands)
        
        # El template usa f-strings. Las llaves internas del JSON se escapan con doble barra invertida (\\)
        USER_MESSAGE_TEMPLATE = f"""
    [INSTRUCCIONES DE PROCESAMIENTO Y ROL]
    Eres un Analizador de Comandos de Voz. Tu tarea es analizar el texto del usuario y extraer comandos de acción específicos. Tu respuesta debe ser **ÚNICA Y EXCLUSIVAMENTE** un objeto JSON.

    **REGLAS CRÍTICAS:**
    1. Formato de Salida: Responde ÚNICAMENTE con JSON, conteniendo una lista bajo la clave "comandos". NO uses texto, explicaciones o comentarios.
    2. **Generación de Respuesta Conversacional:** Para cada comando, genera una frase corta, amigable y conversacional (frase_de_vuelta) que reconozca la solicitud del usuario.
    3. Multicomando: Si hay múltiples acciones, lístalas todas.
    4. **DECODIFICACIÓN Y OPTIMIZACIÓN DEL PARÁMETRO:** El campo `parametro` debe ser el texto más limpio y **optimizado** para la ejecución. DEBES eliminar relleno conversacional ("eh", "algo por el estilo"), pero PRESERVAR nombres propios y palabras clave esenciales.
    5. **CUMPLIMIENTO DE INSTRUCCIÓN ESPECÍFICA (OBLIGATORIO): DEBES LEER y CUMPLIR RIGUROSAMENTE con la 'Instrucción de Procesamiento Específica' provista en la segunda tabla a continuación.**

    **ESQUEMA JSON ESTRICTO (ACTUALIZADO):**
    {{\\"comandos\\": [ 
    {{\\"comando\\": \\"NOMBRE_DEL_COMANDO\\", 
    \\"parametro\\": \\"VALOR_EXTRAÍDO_o_null\\",
    \\"frase_de_vuelta\\": \\"Frase amigable generada por el asistente\\" }} 
    ] }}

    **TABLA 1: COMANDOS PERMITIDOS Y GUÍA DE PARÁMETROS**
    {commands_table_markup}

    ---

    **TABLA 2: INSTRUCCIONES DE PROCESAMIENTO ESPECÍFICAS (CUMPLIMIENTO OBLIGATORIO)**
    {instructions_table_markup}

    [TEXTO DE VOZ DEL USUARIO A ANALIZAR]
    {audio_text}
    """
        return USER_MESSAGE_TEMPLATE.strip()