# 🤖 Control de Asistencia y Asistente de Voz IA

Sistema híbrido desarrollado en Python que integra autenticación biométrica (reconocimiento facial con prueba de vida) y un asistente virtual potenciado por OpenAI para la ejecución de comandos de voz en lenguaje natural.

## 🚀 Características Principales

* **Autenticación Biométrica**: Login mediante reconocimiento facial.
* **Prueba de Vida (Liveness)**: Verificación de gestos aleatorios (ej. "levanta dos dedos") validada por IA para evitar suplantación con fotos.
* **Registro por Voz**: Flujo guiado por voz (TTS/STT) para dar de alta nuevos usuarios y capturar sus datos y biometría.
* **Asistente Inteligente**: Interpretación de comandos complejos usando OpenAI (GPT).
* **Ejecución de Tareas**:
    * Reproducción de música en Spotify.
    * Búsqueda y reproducción en YouTube.
    * Apertura de aplicaciones locales (Calculadora, Paint, etc.).
    * Gestión de alarmas y temporizadores.
* **Registro de Asistencia**: Guardado automático de fichajes en JSON.

## 🛠️ Requisitos e Instalación

### Prerrequisitos

* Python 3.8 o superior.
* Cámara web y micrófono funcionales.
* Cuenta y API Key de OpenAI.
* Cuenta de Spotify (para funciones musicales).

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd ControlDeAsistencia
   ```

2. **Crear entorno virtual (Recomendado)**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
   *Nota: `face_recognition` requiere CMake y dlib instalados previamente.*

4. **Configuración (.env)**
   
   Crea un archivo `.env` en la carpeta `config/` con el siguiente contenido:
   ```env
   OPENAI_API_KEY=tu_clave_de_openai
   SPOTIPY_CLIENT_ID=tu_cliente_id_spotify
   SPOTIPY_CLIENT_SECRET=tu_secreto_spotify
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
   ```

## 📂 Estructura del Proyecto

```text
├── config/                 # Configuración del entorno
│   └── .env                # Variables de entorno (API Keys)
├── core/                   # Módulos principales del sistema
│   ├── attendance_system.py # Gestión de fichajes en JSON
│   ├── command_manager.py   # Orquestador: escucha audio -> LLM -> ejecuta acción
│   ├── facial.py            # Lógica de cámara, reconocimiento facial y liveness
│   ├── openai_client.py     # Cliente API OpenAI (Texto e Imágenes)
│   ├── spotify_client.py    # Control de reproducción de Spotify
│   ├── users_system.py      # Lógica de Login, Registro y gestión de usuarios
│   └── voice.py             # Motores de STT (Google) y TTS (Pyttsx3)
├── data/                   # Almacenamiento de datos
│   ├── attendance.json      # Log de registros de asistencia
│   ├── commands.json        # Definición de comandos para el prompt
│   ├── facial_phrases.json  # Instrucciones para la prueba de vida
│   ├── users.json           # Base de datos de usuarios y encodings faciales
│   └── multishot_...json    # Ejemplos (few-shot) para el contexto del LLM
├── documents/              # Documentación y requisitos
├── photos/                 # Almacenamiento temporal de capturas
├── prompts/                # Prompts del sistema para el LLM
│   └── system_prompt.md     # Instrucciones maestras para el parser de comandos
├── sounds/                 # Assets de audio (beeps)
├── utils/                  # Utilidades transversales
│   ├── audio_phrases.py     # Palabras clave (Wake words, confirmaciones)
│   ├── command_actions.py   # Implementación real de las acciones (abrir apps, web)
│   ├── file_manager.py      # Helpers para lectura/escritura de archivos
│   ├── paths_utils.py       # Gestión de rutas absolutas
│   ├── sound.py             # Reproductor de efectos de sonido
│   └── time_utils.py        # Conversión de texto a segundos
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Lista de librerías necesarias
└── README.md               # Documentación del proyecto
```

## 🕹️ Uso

### Iniciar la aplicación

```bash
python src/main.py
```

### Login / Registro

* Mira a la cámara.
* Si el sistema te reconoce, te pedirá realizar un gesto (ej. "tócate la nariz") para verificar tu identidad.
* Si no estás registrado, el asistente te guiará por voz para crear tu perfil.

### Asistente de Voz

Una vez logueado, di "Hey Sistema" o "Sistema despierta".

Espera el pitido y di tu comando.

**Ejemplos:**

* "Pon música de AC/DC en Spotify"
* "Abre la calculadora y pon una alarma en 10 minutos"
* "Búscame un tutorial de Python en YouTube"

## 💻 Tecnologías Usadas

* **Python 3**: Lenguaje base.
* **OpenCV & Face Recognition**: Visión artificial y biometría.
* **OpenAI API (GPT-4o/GPT-4-turbo)**: Motor de inteligencia para parsing de comandos y visión (gestos).
* **SpeechRecognition (Google API)**: Transcripción de voz a texto.
* **Pyttsx3**: Síntesis de voz (Texto a Voz).
* **Spotipy**: Integración con API de Spotify.
* **Pygame**: Gestión de efectos de sonido.