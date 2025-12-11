# # CLASE DEPRECATED POR AHORA

# # Imports que necesitas
# import requests
# import json

# class OllamaClient:
    
#     def __init__(self):
#         self.OLLAMA_API = "http://localhost:11434/api/chat" 
#         self.HEADERS = {"Content-Type": "application/json"}
#         self.MODEL = "llama3:8b"
    
#     def call_ollama(self, audio_text, commands):
        
#         messages = [
#             {"role": "user", "content": self._build_user_message(audio_text, commands)}
#         ]

#         # Construcción del payload
#         payload = {
#             "model": self.MODEL,
#             "messages": messages,
#             "stream": False,
#             "options": {
#                 "temperature": 0.2,
#                 "top_p" : 0.9,
#                 "num_predict": 2048
#                 } 
#         }
        
#         try:        
#             # Con stream=True, usamos stream=True en requests también
#             resp = requests.post(self.OLLAMA_API, json=payload, headers=self.HEADERS, timeout=120, stream=False)
#             resp.raise_for_status()
#             data = resp.json()
#             response_json_string = data['message']['content']
#             return json.loads(self._extract_json_message(response_json_string))
            
#         except requests.exceptions.ConnectionError as e:
#             print("[ERROR] Servidor no disponible. Verifica que Ollama esté ejecutándose con: ps aux | grep ollama")
#             print(e)
#         except requests.exceptions.HTTPError as e:
#             print("[ERROR] Error HTTP. Posible modelo no descargado. Ejecuta: ollama pull llama3.2")
#             print(e)
#         except requests.exceptions.RequestException as e:
#             print("[ERROR] Error general de red o timeout. Aumenta el timeout si el modelo es lento.")
#             print(e)
            
#     def _extract_json_message(self, response_json_string):
#         # Buscamos el inicio y el fin del bloque JSON
#         start_index = response_json_string.find('{')
#         end_index = response_json_string.rfind('}')
        
#         if start_index == -1 or end_index == -1:
#             # Si no encuentra las llaves, el modelo falló catastróficamente
#             raise json.JSONDecodeError(
#                 f"No se encontró un bloque JSON válido en la respuesta del LLM.", 
#                 response_json_string, 0
#             )

#         # Extraemos y limpiamos solo el bloque entre las llaves
#         clean_json_string = response_json_string[start_index : end_index + 1].strip()
#         return clean_json_string

        
#     def _build_commands_table(self, commands):        
#         # --- TABLA 1: Reglas de Extracción de Parámetros ---
#         table_rows_params = ["| Comando | Intenciones Típicas | Descripción del Parámetro (`parametro`) |", 
#                             "| :--- | :--- | :--- |"]
                        
#         # --- TABLA 2: Instrucciones de Procesamiento Específicas (NUEVO) ---
#         table_rows_inst = ["| Comando | Instrucción de Procesamiento Específica |", 
#                         "| :--- | :--- |"]
        
#         for item in commands:
#             # Excluir el comando "No identificado" del prompt para no confundir al LLM
#             if item.get("comando") == "No identificado":
#                 continue 
            
#             # 1. Llenar la Tabla de Parámetros
#             intenciones_str = ", ".join(item.get("intenciones", []))
#             table_rows_params.append(
#                 f"| `{item.get('comando')}` | {intenciones_str} | {item.get('descripcion_parametro', 'No requiere') } |"
#             )
            
#             # 2. Llenar la Tabla de Instrucciones Específicas
#             table_rows_inst.append(
#                 f"| `{item.get('comando')}` | {item.get('instruccion_llm', 'Ninguna.') } |"
#             )
                
#         return "\n".join(table_rows_params), "\n".join(table_rows_inst)


#     def _build_user_message(self, audio_text, commands):        
#         # Generar las dos tablas
#         commands_table_markup, instructions_table_markup = self._build_commands_table(commands)
        
#         # El template usa f-strings. Las llaves internas del JSON se escapan con doble barra invertida (\\)
#         USER_MESSAGE_TEMPLATE = f"""
# [INSTRUCCIONES DE PROCESAMIENTO Y ROL]
# Eres un **Extractor de JSON de Comandos de Alta Fidelidad**. Tu única y exclusiva función es analizar el texto y generar el JSON solicitado. Tu rol no es sugerir, resumir ni ser conversacional; eres un PARSER estricto y preciso. Tu respuesta debe ser **ÚNICA Y EXCLUSIVAMENTE** un objeto JSON.

# **REGLAS CRÍTICAS:**
# 1. FORMATO DE SALIDA (CRÍTICO): Responde ÚNICAMENTE con JSON. El JSON DEBE ESTAR EN UNA SOLA LÍNEA, sin saltos de línea (\n) ni espacios adicionales, y DEBE ser estructuralmente completo.
# 2. **MULTICOMANDO (OBLIGATORIO SUPREMO):** DEBES identificar y listar CADA ACCIÓN solicitada por el usuario, incluso si son múltiples. NUNCA DEBES OMITIR un comando solicitado. Si el usuario dice 'alarma y youtube', debes generar AMBOS comandos.
# 3. **PROHIBICIÓN DE ALUCINACIÓN (CRÍTICO):** NUNCA DEBES INCLUIR en la lista 'comandos' NINGUNA ACCIÓN que no haya sido solicitada **EXPLÍCITAMENTE** en el TEXTO DE VOZ DEL USUARIO A ANALIZAR. Si solo saluda, genera **SOLO** el comando 'initial_greetings'.
# 4. DECODIFICACIÓN Y OPTIMIZACIÓN DEL PARÁMETRO: El campo `parametro` debe ser el texto más limpio y optimizado para la ejecución. Elimina relleno conversacional ("eh", "o algo por el estilo"), pero PRESERVA nombres propios y palabras clave esenciales.
# 5. CUMPLIMIENTO DE INSTRUCCIÓN ESPECÍFICA (OBLIGATORIO): DEBES LEER y CUMPLIR RIGUROSAMENTE con la 'Instrucción de Procesamiento Específica' provista en la segunda tabla.
    
#     **ESQUEMA JSON ESTRICTO (COMPACTO):**
#     {{"comandos": [ {{"comando": \\"NOMBRE_DEL_COMANDO\\", \\"parametro\\": \\"VALOR_EXTRAÍDO_o_null\\", \\"frase_de_vuelta\\": \\"Frase amigable generada por el asistente\\" }} ]}}
    
#     **TABLA 1: COMANDOS PERMITIDOS Y GUÍA DE PARÁMETROS**
#     {commands_table_markup}

#     ---

#     **TABLA 2: INSTRUCCIONES DE PROCESAMIENTO ESPECÍFICAS (CUMPLIMIENTO OBLIGATORIO)**
#     {instructions_table_markup}

#     [TEXTO DE VOZ DEL USUARIO A ANALIZAR]
#     {audio_text}
#     """
#         return USER_MESSAGE_TEMPLATE.strip()