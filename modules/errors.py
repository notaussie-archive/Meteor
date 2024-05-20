# Import required modules
import guilded
from guilded.ext import commands
from utils.jsprint import JSP
from utils.detailedtrace import getDetailed


# Create the anime module
class Errors(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()

        # Create initial variables
        self.bot: commands.Bot = bot
        self.config: dict = bot.config
        self.console: JSP = bot.console

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """Handles errors that occur while a command is running."""

        # Using a try block to gracefuly handle errors
        try:
            # Handle command not found errors
            if isinstance(error, commands.CommandNotFound):
                # Create error embed
                embed = guilded.Embed(
                    title="Uh oh",
                    description=f"The inputted command was not found.",
                    color=guilded.Color.dark_theme(),
                )

                await ctx.reply(embed=embed, private=True)

            # Handle bad argument erors
            elif isinstance(error, commands.BadArgument):
                # Create error embed
                embed = guilded.Embed(
                    title="Uh oh",
                    description=f"You've put an invalid argument.",
                    color=guilded.Color.dark_theme(),
                )

                # Add the invalid argument field
                embed.add_field(
                    name="Invalid Argument",
                    value=f"› `{error.args[0].split(' ')[0]}`",
                    inline=False,
                )

                await ctx.reply(
                    f'**You put invalid arguments!**\n***Arguments Wrong:***\n{", ".join(error.args)}',
                    private=True,
                )

            # Handle missing argument errors
            elif isinstance(error, commands.MissingRequiredArgument):
                # Create error embed
                embed = guilded.Embed(
                    title="Uh oh",
                    description=f"You're missing required arguments!",
                    color=guilded.Color.dark_theme(),
                )

                # Add the missing arguments field
                embed.add_field(
                    name="Missing Argument",
                    value=f"› `{error.args[0].split(' ')[0]}`",
                    inline=False,
                )

                await ctx.reply(embed=embed, private=True)

            # Handle command cooldowns
            elif isinstance(error, commands.CommandOnCooldown):
                # Create error embed
                embed = guilded.Embed(
                    title="Uh oh",
                    description=f"This command is on cooldown!",
                    color=guilded.Color.dark_theme(),
                )

                # Add the cooldown field
                embed.add_field(
                    name="Time Remaining",
                    value=f"› `{round(error.retry_after, 2)}` seconds",
                    inline=False,
                )

                await ctx.reply(embed=embed, private=True)

            # If none of the predefined handlers were called then use the blanket handler
            else:
                # Print the error to console
                self.console.error(
                    f"An error occurred while running {ctx.command.qualified_name}"
                )
                self.console.trace(getDetailed(error))

                # Send the error message
                await ctx.reply(
                    embed=guilded.Embed(
                        title="Uh oh",
                        description="Something went wrong while we were processing your request. :<",
                        color=guilded.Color.dark_theme(),
                    ),
                    private=True,
                )
                return

        except:
            ...


# Setup the cog and add it to the bot
def setup(bot):
    bot.add_cog(Errors(bot))
