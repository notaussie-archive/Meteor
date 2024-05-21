# Import required modules
import guilded
from guilded.ext import commands
from utils.jsprint import JSP
from utils.detailedtrace import getDetailed

# Import documents
from database.documents import Server


# Create the anime module
class OnBotAdded(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()

        # Create initial variables
        self.bot: commands.Bot = bot
        self.config: dict = bot.config
        self.console: JSP = bot.console

    @commands.Cog.listener()
    async def on_bot_add(self, event: guilded.BotAddEvent):
        """Handle the bot being added"""

        self.console.log(f"Added to {event.server_id} by {event.member_id}")

        # Run the operation in a try expect block
        try:
            # Create a new server document
            server = Server(serverId=event.server_id)

            # Check if the server already exists
            if Server.find_one(Server.serverId == event.server_id) is None:
                # Insert the server
                await server.save()

        # Expect any errors
        except Exception as e:
            # Get the server's default channel
            ch = await event.server.fetch_default_channel()

            # Create error embed
            embed = guilded.Embed(
                title="Uh oh",
                description=f"Something went wrong while adding your server, the bot has automatically left, try re-adding {self.bot.user.name}.",
                color=guilded.Color.dark_theme(),
            )

            # Send the embed using a try block
            try:
                await ch.send(embed=embed)
            except:
                pass

            # Leave the server
            await event.server.leave()

            # Log the error
            self.console.error("Failed to save server")
            self.console.trace(getDetailed(e))

            return  # Using return to prevent any 403 errors

        # Get the inviter
        inviter = await self.bot.getch_user(event.member_id)

        # Creat the thank you embed
        embed = guilded.Embed(
            title="Thanks for adding Meteor!",
            description=f"Run `{self.bot.command_prefix[0]}help` for a list of commands.",
            url=f"https://www.guilded.gg/b/{self.bot.user.bot_id}",
            color=guilded.Color.dark_theme_embed(),
        )

        # Add the inviter field
        embed.add_field(
            name="✨ Added by",
            value=f"› {inviter.mention}",
            inline=False,
        )

        # Get the server's default channel
        ch = await event.server.fetch_default_channel()

        # Send the embed using a try block
        try:
            await ch.send(embed=embed)
        except:
            pass


# Setup the cog and add it to the bot
def setup(bot):
    bot.add_cog(OnBotAdded(bot))
