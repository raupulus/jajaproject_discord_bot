import discord
from discord.ext import commands
from discord.ext import tasks
import random
import sys
import traceback
import asyncio
from config import DISCORD_TOKEN, COMMAND_PREFIX
from jokes_service import JokesService

# Inicializo el servicio de chistes
jokes_service = JokesService()

# Configuro intents (True para que funcione leer mensajes)
intents = discord.Intents.default()
intents.message_content = True

# Diccionario para traducir entradas de usuario a slugs de grupo
GROUP_TRANSLATIONS = {
    "dev": "chistes-devs",
    "lepe": "chistes-lepe",
    "general": "chistes-general",
    "malo": "chistes-malos",
    "infantil": "chistes-infantiles",
}

# Diccionario para metadatos de comandos
COMMANDS = {
    "help": {
        "function": "help_command",
        "title": "Ayuda",
        "description": "Muestra la lista de comandos disponibles",
        "color": discord.Color.blue()
    },
    "colaborar": {
        "function": "colaborar",
        "title": "Colaborar",
        "description": "Información sobre cómo contribuir con tus propios chistes",
        "color": discord.Color.green()
    }
}

# Lista de estados del bot para rotar
BOT_STATUSES = [
    #Compitiendo en...
    "Pelar papas 🫏 🥔",
    "Matar Bots 🫏 🤖",
    "Compilar Cartero 🫏 📮",
    "Reirme solo 🫏 😂",
    "Leer memes 🫏 📱",
    "Hacer el vago 🫏 😴",
    "Echarme la siesta 🫏 💤",
    "Programar nuevos chistes 🫏 💻",
    "Estudiar comedia 🫏 📚",
    "Ver Netflix 🫏 📺",
    "Jugar al escondite 🫏 👻",
    "Comer pizza 🫏 🍕",
    "Bailar solo 🫏 💃",
    "Cantar bajo la ducha 🫏 🚿",
    "Dibujar garabatos 🫏 ✏️",
    "Cocinar armondigas 🫏 🍝",
    "Esperando el fin de semana 🫏 📅",
    "Cocinar Croquetas de bacalao 🫏 🐟",
    "Cazar un pollo 🫏 🐔",
    "Comer Polvorones 🫏 🍪",
    "Soplar el Puchero 🫏 🍲",
    "Tostar almendras 🫏 🌰",
    "Mascar Gomas de borrar 🫏 🟩",
    "Miss Risitas de este año 🫏 👑",
]


# Índice del estado actual
current_status_index = 0

# Crear la instancia del bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

@tasks.loop(minutes=50)
async def change_status():
    """Tarea en segundo plano para cambiar el estado del bot cada 50 minutos."""
    global current_status_index

    # Obtener el estado actual
    current_status = BOT_STATUSES[current_status_index]

    # Crear una lista de estados posibles excluyendo el actual
    available_statuses = [s for s in BOT_STATUSES if s != current_status]

    # Seleccionar un estado aleatorio de los disponibles
    new_status = random.choice(available_statuses)

    # Actualizar el índice para el nuevo estado
    current_status_index = BOT_STATUSES.index(new_status)

    # Actualizar el estado del bot
    #await bot.change_presence(activity=discord.Game(name=new_status))
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.competing,name=new_status))

    print(f"Estado cambiado a: {new_status}")

@bot.event
async def on_ready():
    """Evento que se activa cuando el bot está listo y conectado a Discord."""
    print(f'Bot conectado como {bot.user.name}')
    print(f'ID del Bot: {bot.user.id}')
    print('------')

    # Establecer el estado inicial inmediatamente
    await change_status()

    # Iniciar la tarea de cambio de estado para actualizaciones futuras
    change_status.start()

@bot.event
async def on_command_error(ctx, error):
    """Manejador global de errores para los comandos del bot."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Lo que has escrito no tiene ningún sentido, usa '!chiste help' para ver todas las opciones antes de partirte los dedos machacando teclas absurdamente")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Falta un argumento requerido. Usa `{COMMAND_PREFIX}help {ctx.command}` para ver el uso correcto.")
    else:
        # Registrar el error
        print(f'Error en el comando {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        await ctx.send("Ha ocurrido un error al procesar el comando.")

@bot.command(name="chiste")
async def chiste(ctx, arg=None):
    """
    Obtiene un chiste de la API de chistes.

    Args:
        arg: Argumento opcional para especificar el tipo o grupo de chiste
             - 'random': Obtiene un chiste aleatorio por tipo
             - 'help': Muestra la ayuda para este comando
             - Cualquier otro valor: Intenta emparejarlo con un grupo en GROUP_TRANSLATIONS
    """
    if arg is None or arg.lower() == 'help':
        # Mostrar ayuda para el comando
        embed = discord.Embed(
            title="Ayuda del comando chiste",
            description="Bot para chistacos subidos por nuestros hermosos jajajeros para la comunidad",
            color=discord.Color.blue()
        )
        embed.add_field(
            name=f"{COMMAND_PREFIX}chiste",
            value="Muestra este mensaje de aiuda",
            inline=False
        )
        embed.add_field(
            name=f"{COMMAND_PREFIX}chiste random",
            value="Obtiene un chiste aleatorio entre todos los existentes",
            inline=False
        )

        # Añadir campos para cada grupo en GROUP_TRANSLATIONS
        for user_input, group_slug in GROUP_TRANSLATIONS.items():
            embed.add_field(
                name=f"{COMMAND_PREFIX}chiste {user_input}",
                value=f"Obtiene un chiste aleatorio del grupo '{group_slug}'",
                inline=False
            )

        # Añadir campo para el comando colaborar
        embed.add_field(
            name=f"{COMMAND_PREFIX}chiste colaborar",
            value="Información sobre cómo contribuir con tus propios chistes",
            inline=False
        )

        await ctx.send(embed=embed)
        return

    joke_data = None

    if arg.lower() == 'random':
        # Obtengo un chiste aleatorio por tipo
        joke_data = jokes_service.get_random_joke_by_type('chistes')
    elif arg.lower() == 'colaborar':
        # Llamo al comando colaborar
        await colaborar(ctx)
        return
    elif arg.lower() in GROUP_TRANSLATIONS:
        # Obtengo un chiste del grupo especificado
        group_slug = GROUP_TRANSLATIONS[arg.lower()]
        joke_data = jokes_service.get_random_joke_by_group(group_slug)
    else:
        await ctx.send(f"Lo que has escrito no tiene ningún sentido, usa '{COMMAND_PREFIX}chiste help' para ver todas las opciones antes de partirte los dedos machacando teclas absurdamente")
        return

    # Compruebo si hay error en joke_data
    if joke_data and 'error' in joke_data:
        await ctx.send(joke_data['error'])
        return

    if not joke_data:
        await ctx.send("En estos momentos hay un elefante pisoteando nuestros servidores, inténtalo más tarde y si persiste contacta con el administrador para espantarlos.")
        return

    # Formateo el chiste
    if isinstance(joke_data, dict) and joke_data.get('success') == True and 'data' in joke_data and joke_data['data']:
        # Obtengo el primer chiste del array de datos
        joke = joke_data['data'][0]

        # Creo embed para formatear el mensaje
        embed = discord.Embed(
            title=joke.get('title', 'Chiste'),
            description=joke.get('content', 'No hay contenido disponible actualmente.'),
            color=discord.Color.green()
        )

        # Añadir información del contribuidor si está disponible
        if 'uploader' in joke:
            embed.set_footer(text=f"Subido por {joke['uploader']}")

        # Añadir imagen si está disponible
        if joke.get('urlImage'):
            embed.set_image(url=joke['urlImage'])

        await ctx.send(embed=embed)
    else:
        # Alternativa para formato desconocido o error
        #joke_text = str(joke_data)
        joke_text = "En estos momentos hay un elefante pisoteando nuestros servidores, inténtalo más tarde y si persiste contacta con el administrador para espantarlos."
        await ctx.send(joke_text)


@bot.command(name="colaborar")
async def colaborar(ctx):
    """
    Proporciona información sobre cómo contribuir con chistes a la comunidad.
    """
    await ctx.send("Puedes colaborar subiendo tu propio chiste a la comunidad desde la web https://jaja.raupulus.dev antes de que se te olvide")

@bot.command(name="help")
async def help_command(ctx, command_name=None):
    """
    Muestra información de ayuda para los comandos del bot.

    Args:
        command_name: Nombre opcional de un comando específico para obtener ayuda
    """
    if command_name:
        # Ayuda para un comando específico
        command = bot.get_command(command_name)
        if command:
            embed = discord.Embed(
                title=f"Ayuda: {COMMAND_PREFIX}{command.name}",
                description=command.help or "No hay descripción disponible.",
                color=discord.Color.blue()
            )
            usage = f"{COMMAND_PREFIX}{command.name}"
            if command.signature:
                usage += f" {command.signature}"
            embed.add_field(name="Uso", value=f"`{usage}`", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Comando `{command_name}` no encontrado.")
    else:
        # Ayuda general
        embed = discord.Embed(
            title="Ayuda de JajaBot",
            description="Aquí están los comandos disponibles:",
            color=discord.Color.blue()
        )

        for command in sorted(bot.commands, key=lambda x: x.name):
            embed.add_field(
                name=f"{COMMAND_PREFIX}{command.name}",
                value=command.help or "No hay descripción disponible.",
                inline=False
            )

        await ctx.send(embed=embed)

def run_bot():
    """Ejecuta el bot de Discord."""
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("Error: Token de Discord inválido. Por favor, revisa tu archivo .env.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_bot()
