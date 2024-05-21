import guilded
from utils.assets import malLogo
from utils.texttools import remove_source


def DetailedAnimeView(data: dict) -> guilded.Embed:
    """A detailed anime embed."""

    # Create the embed
    embed = guilded.Embed(
        title=data["title_english"] or data["title"],
        description=(
            remove_source(str(data["synopsis"])).strip() if data["synopsis"] else ""
        ),
        color=guilded.Color.dark_theme(),
        url=data["url"],
    )

    # Set the age rating
    embed.add_field(
        name="Age Rating",
        value="› " + str(data["rating"]).split(" ")[0].upper(),
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
        icon_url=malLogo,
        text="Powered by MyAnimeList.net",
    )

    return embed
