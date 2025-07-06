import discord
from discord.ext import commands
from discord.ext import tasks
import random
import sys
import traceback
import asyncio
from config import DISCORD_TOKEN, COMMAND_PREFIX
from jokes_service import JokesService

# Initialize the jokes service
jokes_service = JokesService()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content

# Dictionary for translating user inputs to group slugs
GROUP_TRANSLATIONS = {
    "dev": "chistes-devs",
    "lepe": "chistes-lepe"
}

# Dictionary for command metadata
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

# List of bot statuses to rotate through
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


# Current status index
current_status_index = 0

# Create the bot instance
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

@tasks.loop(minutes=50)
async def change_status():
    """Background task to change the bot's status every 50 minutes."""
    global current_status_index

    # Get the current status
    status = BOT_STATUSES[current_status_index]

    # Update the bot's status
    #await bot.change_presence(activity=discord.Game(name=status))
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.competing,name=status))

    # Move to the next status (loop back to the beginning if we reach the end)
    current_status_index = (current_status_index + 1) % len(BOT_STATUSES)

    print(f"Status changed to: {status}")

@bot.event
async def on_ready():
    """Event triggered when the bot is ready and connected to Discord."""
    print(f'Bot connected as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')

    # Set the initial status immediately
    await change_status()

    # Start the status change task for future updates
    change_status.start()

@bot.event
async def on_command_error(ctx, error):
    """Global error handler for bot commands."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Lo que has escrito no tiene ningún sentido, usa '!chiste help' para ver todas las opciones antes de partirte los dedos machacando teclas absurdamente")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Falta un argumento requerido. Usa `{COMMAND_PREFIX}help {ctx.command}` para ver el uso correcto.")
    else:
        # Log the error
        print(f'Error in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        await ctx.send("Ha ocurrido un error al procesar el comando.")

@bot.command(name="chiste")
async def chiste(ctx, arg=None):
    """
    Get a joke from the jokes API.

    Args:
        arg: Optional argument to specify joke type or group
             - 'random': Get a random joke by type
             - 'help': Show help for this command
             - Any other value: Try to match it to a group in GROUP_TRANSLATIONS
    """
    if arg is None or arg.lower() == 'help':
        # Show help for the command
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

        # Add fields for each group in GROUP_TRANSLATIONS
        for user_input, group_slug in GROUP_TRANSLATIONS.items():
            embed.add_field(
                name=f"{COMMAND_PREFIX}chiste {user_input}",
                value=f"Obtiene un chiste aleatorio del grupo '{group_slug}'",
                inline=False
            )

        # Add field for colaborar command
        embed.add_field(
            name=f"{COMMAND_PREFIX}chiste colaborar",
            value="Información sobre cómo contribuir con tus propios chistes",
            inline=False
        )

        await ctx.send(embed=embed)
        return

    joke_data = None

    if arg.lower() == 'random':
        # Get a random joke by type
        joke_data = jokes_service.get_random_joke_by_type('chistes')
    elif arg.lower() == 'colaborar':
        # Call the colaborar command
        await colaborar(ctx)
        return
    elif arg.lower() in GROUP_TRANSLATIONS:
        # Get a joke from the specified group
        group_slug = GROUP_TRANSLATIONS[arg.lower()]
        joke_data = jokes_service.get_random_joke_by_group(group_slug)
    else:
        await ctx.send(f"Lo que has escrito no tiene ningún sentido, usa '{COMMAND_PREFIX}chiste help' para ver todas las opciones antes de partirte los dedos machacando teclas absurdamente")
        return

    # Check for error in joke_data
    if joke_data and 'error' in joke_data:
        await ctx.send(joke_data['error'])
        return

    if not joke_data:
        await ctx.send("En estos momentos hay un elefante pisoteando nuestros servidores, inténtalo más tarde y si persiste contacta con el administrador para espantarlos.")
        return

    # Format the joke based on the API response structure
    if isinstance(joke_data, dict) and joke_data.get('success') == True and 'data' in joke_data and joke_data['data']:
        # Get the first joke from the data array
        joke = joke_data['data'][0]

        # Create an embed for better formatting
        embed = discord.Embed(
            title=joke.get('title', 'Chiste'),
            description=joke.get('content', 'No hay contenido disponible actualmente.'),
            color=discord.Color.green()
        )

        # Add uploader information if available
        if 'uploader' in joke:
            embed.set_footer(text=f"Subido por {joke['uploader']}")

        # Add image if available
        if joke.get('urlImage'):
            embed.set_image(url=joke['urlImage'])

        await ctx.send(embed=embed)
    else:
        # Fallback for unknown format or error
        joke_text = str(joke_data)
        await ctx.send(joke_text)


@bot.command(name="colaborar")
async def colaborar(ctx):
    """
    Provides information on how to contribute jokes to the community.
    """
    await ctx.send("Puedes colaborar subiendo tu propio chiste a la comunidad desde la web https://jaja.raupulus.dev antes de que se te olvide")

@bot.command(name="help")
async def help_command(ctx, command_name=None):
    """
    Display help information for bot commands.

    Args:
        command_name: Optional name of a specific command to get help for
    """
    if command_name:
        # Help for a specific command
        command = bot.get_command(command_name)
        if command:
            embed = discord.Embed(
                title=f"Help: {COMMAND_PREFIX}{command.name}",
                description=command.help or "No description available.",
                color=discord.Color.blue()
            )
            usage = f"{COMMAND_PREFIX}{command.name}"
            if command.signature:
                usage += f" {command.signature}"
            embed.add_field(name="Usage", value=f"`{usage}`", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Command `{command_name}` not found.")
    else:
        # General help
        embed = discord.Embed(
            title="JajaBot Help",
            description="Here are the available commands:",
            color=discord.Color.blue()
        )

        for command in sorted(bot.commands, key=lambda x: x.name):
            embed.add_field(
                name=f"{COMMAND_PREFIX}{command.name}",
                value=command.help or "No description available.",
                inline=False
            )

        await ctx.send(embed=embed)

def run_bot():
    """Run the Discord bot."""
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("Error: Invalid Discord token. Please check your .env file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting bot: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_bot()
