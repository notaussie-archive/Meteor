# Guilded imports
import guilded
from guilded.ext import commands

# Utility imports
from utils.jsprint import JSP
from utils.assets import malLogo

# View imports
from views import DetailedAnimeView

# Jikan imports
from aiohttp_client_cache import CachedSession, CacheBackend
from jikanpy import AioJikan


# Create the anime module
class Anime(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()

        # Create initial variables
        self.bot: commands.Bot = bot
        self.config: dict = bot.config
        self.console: JSP = bot.console

        # Setup an AioHTTP cache
        self.jikanCache: CacheBackend = CacheBackend(
            cache_name="jikan-cache",
            include_headers=True,
            allowed_codes=(
                200,
                304,
                404,
            ),
            expire_after=900,
        )

    @commands.group()
    async def anime(self, ctx: commands.Context):
        """Anime related commands"""
        if ctx.invoked_subcommand:
            return

        await ctx.reply(
            embed=guilded.Embed(
                title="Top 5 MAL animes",
                color=guilded.Color.dark_theme(),
            )
        )

    @anime.command()
    async def top(self, ctx: commands.Context):
        """Gets the top animes from `MyAnimeList.net`"""
        async with AioJikan(
            session=CachedSession(cache=self.jikanCache),
        ) as client:
            # Request to MAL
            result = await client.top("anime")

            # Create embed
            embed = guilded.Embed(
                title="Top 5 MAL animes",
                color=guilded.Color.dark_theme(),
            )

            # Iterate over the result
            for i in range(0, 5):

                # Get the anime
                data = result["data"][i]

                # Add the field
                embed.add_field(
                    name=f"#{str(i + 1)} - [{data['title_english'] or data['title']}]({data['url']})",
                    value=f"› Total episodes: {str(data['episodes'])}\n› Age rating: {str(data['rating']).split(' ')[0].upper()}",
                    inline=False,
                )

            # Set the footer
            embed.set_footer(
                icon_url=malLogo,
                text="Powered by MyAnimeList.net",
            )

            await ctx.reply(embed=embed)

    @anime.command()
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def random(self, ctx: commands.Context):
        """Gets a random anime from `MyAnimeList.net`"""
        async with AioJikan() as client:
            # Request to MAL
            result = await client.random("anime")

            # Store the data
            data = result["data"]

            # Send a detailed anime view
            await ctx.reply(embed=DetailedAnimeView(data))

    @anime.command()
    @commands.cooldown(5, 30, commands.BucketType.user)
    async def search(self, ctx: commands.Context, *, query: str):
        """Searches `MyAnimeList.net` and returns an anime matching your query"""
        async with AioJikan(
            session=CachedSession(cache=self.jikanCache),
        ) as client:
            # Request to MAL
            result = await client.search("anime", query=query)

            # Check if result contains no data
            if result["data"] == []:
                await ctx.reply(
                    embed=guilded.Embed(
                        title="Uh oh",
                        description="Failed to find an anime matching your search query.",
                        color=guilded.Color.dark_theme(),
                    ),
                    private=True,
                )
                return

            # Store the first anime in the result data
            data = result["data"][0]

            # Send a detailed anime view
            await ctx.reply(embed=DetailedAnimeView(data))


# Setup the cog and add it to the bot
def setup(bot):
    bot.add_cog(Anime(bot))
