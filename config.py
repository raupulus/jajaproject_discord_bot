import os
from dotenv import load_dotenv

# Cargo las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Configuración de la API de chistes
JOKES_API_URL = os.getenv('JOKES_API_URL')
JOKES_API_KEY = os.getenv('JOKES_API_KEY')

# Prefijo de comandos del bot
COMMAND_PREFIX = '!'

# Compruebo si las variables de entorno requeridas están configuradas
if not DISCORD_TOKEN:
    raise ValueError("La variable de entorno DISCORD_TOKEN no está configurada. Por favor, configúrala en el archivo .env.")

if not JOKES_API_URL:
    raise ValueError("La variable de entorno JOKES_API_URL no está configurada. Por favor, configúrala en el archivo .env.")
