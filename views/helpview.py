import guilded
from guilded.ext import commands


def GroupCommandsView(ctx: commands.Context, group: commands.Group) -> guilded.Embed:
    # Create the embed
    embed = guilded.Embed(
        title=f"All commands for {group.name.title()}",
        color=guilded.Color.dark_theme(),
    )

    # Create the string to store commands in
    commands = ""

    # Iterate over all commands
    for name, command in group.all_commands.copy().items():

        # Format the string and append it to commands
        commands = (
            commands
            + f"`{ctx.prefix}{command.qualified_name}` - {command.description.removesuffix('.') if command.description else 'No description given'}.\n"
        )

    embed.add_field(
        name="Commands",
        value=commands.strip(),
        inline=False,
    )

    return embed
