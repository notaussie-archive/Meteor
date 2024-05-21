import guilded

EmptyEmbed = guilded.embed._EmptyEmbed()


def PartialServerView(server: guilded.Server):
    """A partial server embed."""

    # Create the embed
    embed = guilded.Embed(
        title=server.name,
        color=guilded.Color.dark_theme(),
    )

    # Set the thumbail
    embed.set_thumbnail(url=server.icon.url)

    # Add created at field
    embed.add_field(
        name="Created at",
        value=f"› {server.created_at.strftime('%A %m %Y')}",
        inline=False,
    )

    return embed


def DetailedServerView(): ...
