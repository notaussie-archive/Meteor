# Import required modules
import guilded
from guilded.ext import commands
from utils.jsprint import JSP
import subprocess


# Create the anime module
class Information(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()

        # Create initial variables
        self.bot: commands.Bot = bot
        self.config: dict = bot.config
        self.console: JSP = bot.console

        # Get the SHA
        commandResult = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.STDOUT, text=True
        )

        # Strip the SHA of any trailing newline characters
        sha = commandResult.strip()

        # Store the SHA
        self.sha: str | None = sha

        # Get the current branch
        commandResult = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.STDOUT,
            text=True,
        )

        # Strip the branch name of any trailing newline characters
        branch = commandResult.strip()

        # Store the branch
        self.branch: str | None = branch

    @commands.command()
    async def info(self, ctx: commands.Context):
        """Shows information about the bot"""

        # Create embed
        embed = guilded.Embed(
            title=f"{self.bot.user.name}'s information",
            color=guilded.Color.dark_theme(),
        )

        # Add statistics
        embed.add_field(
            name="👥 Servers",
            value=f"› {str(len(self.bot.servers))}",
            inline=False,
        )

        # Add Git field
        embed.add_field(
            name="🧵 Version",
            value=f"› {self.branch.title()} (`{self.sha}`)",
            inline=False,
        )

        await ctx.reply(embed=embed)


# Setup the cog and add it to the bot
def setup(bot):
    bot.add_cog(Information(bot))
