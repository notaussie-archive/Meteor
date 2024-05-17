# Import required modules
import guilded
from guilded.ext import commands
from utils.jsprint import JSP
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

    @commands.command()
    @commands.cooldown(5, 15, commands.BucketType.user)
    async def anime(self, ctx: commands.Context, *, query: str):
        """Searches `MyAnimeList.net` and gives you infomation about an anime"""
        async with AioJikan(
            session=CachedSession(cache=self.jikanCache),
        ) as client:

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

            # Create the embed
            embed = guilded.Embed(
                title="__" + data["title"] + "__",
                color=guilded.Color.dark_theme(),
            )

            # Set the age rating
            embed.add_field(
                name="Age Rating",
                value="› " + str(data["rating"]).split(" ")[0],
                inline=True,
            )

            # Set the rating
            embed.add_field(
                name="Rating",
                value="› " + str(data["score"]),
                inline=True,
            )

            # Set the episode count
            embed.add_field(
                name="Total Episodes",
                value="› " + str(data["episodes"]),
                inline=True,
            )

            # Set the rank
            if data["rank"]:
                embed.add_field(
                    name="MyAnimeList Rank",
                    value="› #" + str(data["rank"]),
                    inline=True,
                )

            # Set the embed image
            embed.set_image(url=data["images"]["jpg"]["image_url"])

            # Set the footer
            embed.set_footer(
                icon_url=self.config["malLogo"],
                text="Powered by MyAnimeList.net",
            )

            await ctx.reply(embed=embed)


# Setup the cog and add it to the bot
def setup(bot):
    bot.add_cog(Anime(bot))
