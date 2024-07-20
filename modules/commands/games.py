# Guilded imports
import guilded
from guilded.ext import commands

# Utility imports
from utils.jsprint import JSP
from utils.igdb import Client
from utils.assets import igdbLogo
from aiohttp_client_cache import CachedSession, CacheBackend

# View imports
from views import GroupCommandsView


# Create the games module
class Games(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()

        # Create initial variables
        self.bot: commands.Bot = bot
        self.config: dict = bot.config
        self.console: JSP = bot.console
        self.client = Client(self.config["igdb"]["secret"], self.config["igdb"]["id"])

        # Setup an aiohttp cache
        self.igdbCache: CacheBackend = CacheBackend(
            cache_name="igdb-cache",
            include_headers=True,
            allowed_codes=(
                200,
                304,
                404,
            ),
            expire_after=900,
        )

    @commands.group(description="Game/gaming related commands")
    async def games(self, ctx: commands.Context):
        if ctx.invoked_subcommand:
            return

        await ctx.reply(
            embed=GroupCommandsView(ctx, self.games),
            private=ctx.message.private,
        )

    @games.command(description="Searches IGDB and returns a game matching your query")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def search(self, ctx: commands.Context, *, query: str):
        # Query igdb
        data = await self.client.request(
            "/games/",
            "get",
            cache=self.igdbCache,
            params={
                "search": query,
                "fields": "id,name,summary",
                "limit": 1,
            },
        )
        # Check if no results were given
        if len(data) <= 0:
            await ctx.reply(
                embed=guilded.Embed(
                    title="Uh oh",
                    description="Failed to find a game matching your search query.",
                    color=guilded.Color.dark_theme(),
                ),
                private=True,
            )
            return

        # Grab the game
        game = data[0]

        # Create the game embed
        embed = guilded.Embed(
            title=game["name"],
            description=game["summary"],
            color=guilded.Color.dark_theme(),
            url=game["url"],
        )

        embed.set_footer(icon_url=igdbLogo, text="Powered by IGDB")

        await ctx.reply(embed=embed)


# Setup the cog and add it to the bot
def setup(bot):
    bot.add_cog(Games(bot))
