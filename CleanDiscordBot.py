import discord
from discord import app_commands
from discord.ext import commands


from . import *


guild = DISCORD_GUILD
if guild.isdigit():
    MY_GUILD = discord.Object(id = DISCORD_GUILD)  # replace with your guild id
else:
    MY_GUILD = None


class SnapshotRenderBot(commands.Bot):
    def __init__(self, intents, command_prefix, description):
        super().__init__(intents = intents, command_prefix = command_prefix, description = description)
        self.pfp = None

    async def prepare_bot_tree(self):
        print(f"Preparing bot tree (guild = {MY_GUILD})")
        self.tree.clear_commands(guild = MY_GUILD)

        if MY_GUILD:
            # This copies the global commands over to your guild.
            self.tree.copy_global_to(guild = MY_GUILD)

        await self.tree.sync(guild = MY_GUILD)


    async def setup_hook(self):
        """
        A coroutine to be called to setup the bot, by default this is blank.
        This performs an asynchronous setup after the bot is logged in,
        but before it has connected to the Websocket (quoted from d.py docs)
        """
        await self.prepare_bot_tree()
        print("Connecting...")
        # if guild:
        #     await self.tree.sync()
        # else:
        #     self.tree.copy_global_to(guild = MY_GUILD)
        #     await self.tree.sync(guild = MY_GUILD)

    async def on_ready(self):
        """
        Function called when the bot is ready. Emits the '[Bot] has connected' message
        Loads the extensions
        """
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


intents = discord.Intents.default()

bot = SnapshotRenderBot(command_prefix = '/', description = 'blah', intents = intents)


bot.run(DISCORD_TOKEN)