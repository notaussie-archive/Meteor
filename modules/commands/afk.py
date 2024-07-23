# Guilded imports
import guilded
from guilded.ext import commands

# Utility imports
from utils.jsprint import JSP
from datetime import datetime
from humanfriendly import format_timespan

# View imports
from views import BasicErrorView, WelcomeBackView


# Create the afk module
class Afk(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()

        # Create initial variables
        self.bot: commands.Bot = bot
        self.config: dict = bot.config
        self.console: JSP = bot.console

        self.database = dict()
        """
        {
            "[ server ID ]": {
                "[user ID ]": {
                    "timestamp": datetime,
                    "message": str | None,
                }
            }
        } 
        """

    def add(self, serverId: str, userId: str, message: str = None):
        """Adds a user to the AFK database"""
        if serverId not in self.database:
            self.database[serverId] = {}
        self.database[serverId][userId] = {
            "timestamp": datetime.now(),
            "message": message,
        }

    def delete(self, serverId: str, userId: str):
        """Deletes a user from the AFK database"""
        if serverId in self.database and userId in self.database[serverId]:
            del self.database[serverId][userId]

    def get(self, serverId: str, userId: str) -> dict:
        """Retrieves AFK information for a user"""
        if serverId in self.database and userId in self.database[serverId]:
            return self.database[serverId][userId]
        else:
            return None  # User not found in the AFK database

    @commands.command(description="Set an AFK status to display when you are mentioned")
    @commands.cooldown(5, 5, commands.BucketType.general)
    async def afk(self, ctx: commands.Context, *, message: str = None):

        # Check if the message is too long (or short)
        if message and len(message) > 30:
            await ctx.reply(
                embed=BasicErrorView(
                    "Your AFK message is too long. (Above 30 characters)"
                ),
                private=True,
            )
            return

        self.add(ctx.server.id, ctx.author.id, message=message)

        # Create and send the success embed
        await ctx.reply(
            embed=guilded.Embed(
                title="You're now afk!",
                description=f"You've set your AFK message to be:\n› {message or 'No message set.'}",
                color=guilded.Color.dark_theme(),
            ),
            silent=True,
        )

    @commands.Cog.listener()
    async def on_message_reaction_add(self, event: guilded.MessageReactionAddEvent):

        # Get the user
        user = self.get(event.server_id, event.user_id)
        if user:
            # Create and send a welcome back message
            await event.channel.send(
                content=event.member.mention,
                embed=WelcomeBackView(user),
                private=True,
            )

            # Delete the user
            self.delete(event.server.id, event.member.id)

    @commands.Cog.listener()
    async def on_message(self, event: guilded.MessageEvent):

        # Check if the message was sent by a bot
        if event.message.author.bot:
            return

        # Check if the message starts with the bot's prefix
        if event.message.content.startswith(tuple(self.config["guilded"]["prefixes"])):
            return

        # Check if the author was afk
        author = self.get(event.server_id, event.message.author_id)
        if author:
            # Create and send a welcome back message
            await event.message.reply(
                embed=WelcomeBackView(author),
                delete_after=60,
                private=True,
            )

            # Delete the user
            self.delete(event.server_id, event.message.author_id)

        # Iterate over all user mention
        for mention in event.message.user_mentions:

            mentioned = self.get(event.server_id, mention.id)
            if mentioned:

                await event.message.reply(
                    '{} is currently afk{} "{}" - {}'.format(
                        mention.mention,
                        ":" if mentioned.get("message", False) else ".",
                        mentioned.get("message") or "",
                        format_timespan(datetime.now() - mentioned["timestamp"])
                        + " ago.",
                    ),
                    silent=True,
                    delete_after=30,
                )

        # Iterate over all replies
        previouslyRepliedTo = []
        for message in event.message.replied_to:

            # This check prevents spamming about the same user
            if message.author_id not in previouslyRepliedTo:

                replied = self.get(event.server_id, message.author_id)
                if replied:

                    await event.message.reply(
                        '{} is currently afk{} "{}" - {}'.format(
                            message.author.mention,
                            ":" if replied.get("message", False) else ".",
                            replied.get("message") or "",
                            format_timespan(datetime.now() - replied["timestamp"])
                            + " ago.",
                        ),
                        silent=True,
                        delete_after=30,
                    )

                previouslyRepliedTo.append(message.author_id)


# Setup the cog and add it to the bot
def setup(bot):
    bot.add_cog(Afk(bot))
