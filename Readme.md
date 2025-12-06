# 🤖 Sistema de Control de Asistencia y Asistente de Voz IA

Este proyecto es un sistema híbrido desarrollado en Python que combina autenticación biométrica mediante reconocimiento facial con un asistente virtual inteligente impulsado por Modelos de Lenguaje (LLM) como OpenAI GPT y Ollama (Llama 3).

## 📋 Descripción

El sistema permite gestionar el acceso de usuarios y ejecutar comandos de voz complejos. Funciona en dos fases principales:

1. **Login/Registro**: Identifica al usuario mediante la cámara. Si el usuario no existe, inicia un flujo de registro guiado por voz para capturar datos y biometría facial.
2. **Asistente Virtual**: Una vez autenticado, el sistema escucha en segundo plano palabras clave (wake words) para ejecutar acciones como abrir programas, realizar búsquedas en YouTube o configurar alarmas.

## 🚀 Características

### 👤 Identificación y Seguridad

- **Reconocimiento Facial**: Uso de `face_recognition` y `OpenCV` para validación biométrica.
- **Registro Interactivo**: Flujo de alta de usuarios mediante voz (STT) y captura automática de perfil facial.
- **Persistencia**: Almacenamiento de usuarios y perfiles biométricos en JSON.

### 🧠 Inteligencia Artificial y Voz

- **Modelos LLM**: Integración con OpenAI API y Ollama (local) para interpretación de lenguaje natural.
- **Extracción de Comandos**: Convierte peticiones habladas en objetos JSON estructurados para ejecución programática.
- **Voz a Texto (STT)**: Google Speech Recognition para capturar comandos.
- **Texto a Voz (TTS)**: Retroalimentación auditiva mediante `pyttsx3`.

### ⚡ Acciones del Asistente

- **Control de Aplicaciones**: Abre herramientas locales (Calculadora, Paint, Spotify, Navegador).
- **Navegación Web**: Búsquedas directas en YouTube.
- **Gestión del Tiempo**: Configuración de alarmas y temporizadores con ejecución diferida (hilos).

## 🛠️ Requisitos Previos

- Python 3.8+
- Cámara Web
- Micrófono
- Conexión a Internet (para Google STT y OpenAI)
- Ollama instalado y ejecutándose (si se usa el modo local)

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/control-asistencia-ia.git
cd control-asistencia-ia
```

### 2. Crear entorno virtual (Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

**Nota**: `face_recognition` requiere `dlib`. Asegúrate de tener CMake instalado.

```bash
pip install opencv-python face-recognition SpeechRecognition pyttsx3 openai requests pygame python-dotenv numpy unidecode winsound
```

### 4. Configuración de entorno

Crea un archivo `.env` en la carpeta `config/` con tu clave de API:

```env
OPENAI_API_KEY=sk-tu-clave-api-aqui
```

## 📂 Estructura del Proyecto

```
├── config/             # Archivos de configuración (.env)
├── core/               # Lógica central (Voice, Facial, Clientes LLM)
├── data/               # Bases de datos JSON (users.json, commands.json)
├── photos/             # Almacenamiento temporal de capturas
├── prompts/            # Prompts de sistema para el LLM
├── sounds/             # Efectos de sonido (mp3)
├── utils/              # Utilidades (archivos, rutas, tiempo, sonido)
├── main.py             # Punto de entrada (asumido)
└── README.md
```

## ⚙️ Uso

### 1. Ejecuta el script principal

```bash
python main.py
```

### 2. Login

Mira a la cámara. Si no estás registrado, sigue las instrucciones de voz.

### 3. Comandos

Una vez dentro, di una frase de activación como "Hey Sistema" seguido de tu orden.

**Ejemplos:**

- "Hey sistema, abre la calculadora y pon una alarma en 5 minutos"
- "Hola sistema, ponme música en Spotify"

## 🔧 Tecnologías

- **Python**
- **OpenCV & Face Recognition**
- **OpenAI API / Ollama**
- **SpeechRecognition & Pyttsx3**
- **Pygame** (Audio feedback)