# Guilded imports
import guilded
from guilded.ext import commands

# Utility imports
from utils.jsprint import JSP

# View imports
from views import PartialServerView


# Create the tools module
class Tools(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()

        # Create initial variables
        self.bot: commands.Bot = bot
        self.config: dict = bot.config
        self.console: JSP = bot.console

    @commands.group()
    async def tools(self, ctx: commands.Context):
        """Tool related commands"""
        if ctx.invoked_subcommand:
            return

    @tools.command()
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def idtoguild(self, ctx: commands.Context, id: str):
        """Tries to reverse search a server ID to a servers"""

        # Attempt to get the Guild via public lookup
        try:
            server = await self.bot.fetch_public_server(id)

        # Handle if no server was found
        except guilded.NotFound:
            await ctx.reply(
                embed=guilded.Embed(
                    title="Uh oh",
                    description="Failed to find a server matching the provided id.",
                    color=guilded.Color.dark_theme(),
                ),
                private=True,
            )
            return

        await ctx.reply(embed=PartialServerView(server))


# Setup the cog and add it to the bot
def setup(bot):
    bot.add_cog(Tools(bot))
