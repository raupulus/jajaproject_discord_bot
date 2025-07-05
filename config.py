import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Jokes API configuration
JOKES_API_URL = os.getenv('JOKES_API_URL')
JOKES_API_KEY = os.getenv('JOKES_API_KEY')

# Bot command prefix
COMMAND_PREFIX = '!'

# Check if required environment variables are set
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set. Please set it in the .env file.")

if not JOKES_API_URL:
    raise ValueError("JOKES_API_URL environment variable is not set. Please set it in the .env file.")