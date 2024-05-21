# Import required modules
import guilded
from guilded.ext import commands
from utils.jsprint import JSP
from utils.detailedtrace import getDetailed

# Import documents
from database.documents import Server


# Create the anime module
class OnBotRemoved(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()

        # Create initial variables
        self.bot: commands.Bot = bot
        self.config: dict = bot.config
        self.console: JSP = bot.console

    @commands.Cog.listener()
    async def on_bot_remove(self, event: guilded.BotRemoveEvent):
        """Handle the bot being removed"""

        self.console.log(f"Removed from {event.server_id} by {event.member_id}")

        # Run the operation in a try expect block
        try:
            # Delete any document with the server's id (This is to protect from any extra documents)
            await Server.find_many(Server.serverId == event.server_id).delete()

        # Expect any errors
        except Exception as e:
            # Log the error
            self.console.error("Failed to delete server")
            self.console.trace(getDetailed(e))


# Setup the cog and add it to the bot
def setup(bot):
    bot.add_cog(OnBotRemoved(bot))
