# JajaBot - Discord Bot para chistes

JajaBot es un bot de Discord que consume una API de chistes y los comparte en tu servidor de Discord.

Link para añadirlo a tu servidor: [Bot para Discord](https://discord.com/oauth2/authorize?client_id=1391159444490158202&permissions=274877908992&integration_type=0&scope=bot)

¡Puedes colaborar añadiendo más chistes en [https://jaja.raupulus.dev](https://jaja.raupulus.dev) antes de que se te olviden!

## Características

- Obtener chistes aleatorios por tipo o grupo
- Fácil de desplegar con Docker o venv
- Extensible para añadir nuevos comandos

## Requisitos Previos

- Python 3.13 o superior (si no usas Docker)
- Docker y Docker Compose (opcional, para despliegue con contenedores)
- Token de bot de Discord
- URL de la API de chistes

## Configurar tu propio bot (Para no usar el anterior)

### 1. Crear un Bot de Discord

1. Ve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Haz clic en "New Application" y dale un nombre
3. Ve a la sección "Bot" y haz clic en "Add Bot"
4. Bajo la sección "TOKEN", haz clic en "Copy" para copiar tu token
5. En la sección "Privileged Gateway Intents", activa "MESSAGE CONTENT INTENT"
6. Guarda los cambios

### 2. Invitar el Bot a tu Servidor

1. En el portal de desarrolladores, ve a la sección "OAuth2" > "URL Generator"
2. En "SCOPES", selecciona "bot"
3. En "BOT PERMISSIONS", selecciona:
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
4. Copia la URL generada y ábrela en tu navegador
5. Selecciona el servidor al que quieres añadir el bot y confirma

### 3. Configurar Variables de Entorno

1. Crea un archivo `.env` basado en el archivo `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Edita el archivo `.env` y añade tu token de Discord y la URL de la API de chistes:
   ```
   DISCORD_TOKEN=tu_token_aquí
   JOKES_API_URL=https://raupulus.dev/api/v1
   JOKES_API_KEY=your_api_key_here
   ```

## Ejecución

### Usando Docker (Recomendado)

1. Asegúrate de tener Docker y Docker Compose instalados
2. Ejecuta el bot con:
   ```bash
   docker-compose up -d
   ```
3. Para ver los logs:
   ```bash
   docker-compose logs -f
   ```
4. Para detener el bot:
   ```bash
   docker-compose down
   ```

### Sin Docker (usando venv)

1. Crea un entorno virtual:
   ```bash
   python3.13 -m venv .venv
   ```
2. Activa el entorno virtual:
   - En Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - En Windows:
     ```bash
     .venv\Scripts\activate
     ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta el bot:
   ```bash
   python main.py
   ```
5. Para desactivar el entorno virtual cuando termines:
   ```bash
   deactivate
   ```

## Comandos del Bot

- `!chiste` - Muestra la ayuda del comando chiste
- `!chiste random` - Obtiene un chiste aleatorio por tipo
- `!chiste dev` - Obtiene un chiste aleatorio del grupo de desarrolladores
- `!chiste lepe` - Obtiene un chiste aleatorio del grupo de Lepe
- `!chiste malo` - Obtiene un chiste aleatorio del grupo de Malos
- `!chiste infantil` - Obtiene un chiste aleatorio del grupo de Infantiles
- `!chiste add [contenido]` - Envía una sugerencia de contenido directamente a la API
- `!colaborar` - Muestra información sobre cómo contribuir con tus propios chistes
- `!help` - Muestra la lista de comandos disponibles
- `!help [comando]` - Muestra ayuda detallada sobre un comando específico

## Personalización

Puedes modificar el prefijo de comandos (`!` por defecto) editando la variable `COMMAND_PREFIX` en el archivo `config.py`.

## Solución de Problemas

### El bot no responde a los comandos
- Asegúrate de que el bot tenga los permisos necesarios en el servidor
- Verifica que el token en el archivo `.env` sea correcto
- Comprueba que la API de chistes esté funcionando correctamente

### Errores al ejecutar con Docker
- Asegúrate de que Docker y Docker Compose estén instalados correctamente
- Verifica que el archivo `.env` exista y contenga las variables necesarias
- Comprueba los logs con `docker-compose logs -f`

## Contribuir

Las contribuciones son bienvenidas. Por favor, siente libre de abrir un issue o enviar un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia GNU General Public License v3.0 - ver el archivo [LICENSE](LICENSE) para más detalles.

## TODO

- Añadir posibilidad de reportar contenido
