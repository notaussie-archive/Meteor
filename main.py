# Import required modules
import guilded
from guilded.ext import commands
import pymongo.errors
from utils.jsprint import JSP
import subprocess
import yaml
import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from database import all
import pymongo

# Open the config
with open("./config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Create the bot
bot = commands.Bot(
    command_prefix=config["guilded"]["prefixes"],
    help_command=commands.MinimalHelpCommand(),
    features=guilded.ClientFeatures(
        experimental_event_style=True,
        official_markdown=True,
    ),
)
bot.config = config

# Create the console
console = JSP()
bot.console = console


# Create the module loader
def loadModules(bot: commands.Bot):
    """Loads all modues in the `modules` directory (including subdirectories)"""
    for root, dirs, files in os.walk("./modules"):
        for file in files:
            if file.endswith(".py"):
                # Load the extension using dot-qualified name
                cog_path = os.path.relpath(os.path.join(root, file), start="./modules")
                bot.load_extension(
                    f'modules.{cog_path.replace(os.sep, ".").replace(".py", "")}'
                )
                console.success(f"Loaded {cog_path}")


loadModules(bot)


@bot.event
async def on_ready():
    console.success("Connected to Guilded")

    # Create the Motor client
    client = AsyncIOMotorClient(config["mongodb"]["uri"])

    # Check if the cluster is online
    try:
        await client.admin.command("ping")
        console.success("Pinged Mongo successfully")
    except Exception as e:
        if  isinstance(e, pymongo.errors.OperationFailure):
            console.warn("Failed to ping Mongo")
            
        else:
            console.error("Unexpected error occurred while pinging Mongo")
            console.trace(str(e))


    # Initialize Beanie using the previously created Motor client
    await init_beanie(client[config["mongodb"]["database"]], document_models=all)
    console.info("Beanie initialization complete")

    # Print success/info stack
        
    console.info(f'Logged into Guilded as "{bot.user.name}"')
    console.info(f'Using database "{config["mongodb"]["database"]}" on Mongo cluster')


bot.run(config["guilded"]["token"])
