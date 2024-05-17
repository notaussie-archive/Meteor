# Import required modules
import guilded
from guilded.ext import commands
from utils.jsprint import JSP
import subprocess
import yaml
import os

# Open the config
with open("./config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Create the bot
bot = commands.Bot(
    command_prefix=config["guilded"]["prefix"],
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
    console.success(f'Logged in as "{bot.user.name}"!')


bot.run(config["guilded"]["token"])
