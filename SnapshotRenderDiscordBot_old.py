# bot.py
import os

import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import nest_asyncio
import aiofiles
import aiofiles.os
from typing import List, Literal, Union

nest_asyncio.apply()

intents = discord.Intents.default()
intents.message_content = True
from dotenv import load_dotenv

load_dotenv()

from . import DISCORD_GUILD, DISCORD_TOKEN
TOKEN = DISCORD_TOKEN
GUILD = DISCORD_GUILD

# client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = "/", intents = intents)

# tree = app_commands.CommandTree(bot)
tree = bot.tree
from modular.toontown.snapshot import SnapshotClient


# @client.event
# async def on_ready():
#     await tree.sync(guild = discord.Object(id = GUILD))
#     print(f'!!!We have logged in as {client.user}')


@bot.event
async def on_ready():
    await bot.tree.sync(guild = discord.Object(id = GUILD))
    print(f'We have logged in as {bot.user}')


# @bot.command()
# async def toontown(ctx, *args):
#     arguments = ', '.join(args)
#     asyncio.get_event_loop().run_until_complete(SnapshotClient.requestRender())
#     await ctx.send(f'{len(args)} arguments: {arguments}')


def build_json(*args):
    RenderDict = dict()
    type = args[0]
    if type == "toon":
        RenderDict["randomDNA"] = args[1]


# @bot.tree.command(name = "render", description = "Renders random NPC Toon", guild = discord.Object(id = GUILD))  #
# Add the
# # guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it
# # will take some time (up to an hour) to register the command if it's for all guilds.
# async def render(interaction):
#     asyncio.get_event_loop().run_until_complete(SnapshotClient.test())
#
#     with open(SnapshotClient.response, 'rb') as f:
#         picture = discord.File(f)
#         await interaction.response.send_message(file = picture)


# @bot.command()
# async def render(ctx, *args):
#     arguments = ', '.join(args)
#
#     asyncio.get_event_loop().run_until_complete(SnapshotClient.test())
#
#     with open(SnapshotClient.response, 'rb') as f:
#         picture = discord.File(f)
#         await ctx.send(file = picture)
#     # await ctx.send(SnapshotClient.response)
# the @app_commands.guilds and @app_commands.default_permissions decorators (also including checks) can be used above
# the class.
# these will apply to ALL subcommands, subcommands cannot have invidual perms!
@app_commands.guild_only()
class RenderGroup(app_commands.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        self.name = "render"
        self.renderConfig = {
            "type": "npc",
            "randomDNA": True,
            "haphazardDNA": False,  # for stuff like Suits
            "npcID": None,
            "dnaString": None,
            "randomExpression": True
        }


    # subcommand of Group
    @app_commands.command(name = "toon")
    async def render_toon_random(self, interaction: discord.Interaction) -> None:
        self.renderConfig["type"] = "toon"
        self.renderConfig["randomDNA"] = True
        asyncio.get_event_loop().run_until_complete(SnapshotClient.requestRender(self.renderConfig))

        async with aiofiles.open(SnapshotClient.response, 'rb') as f:
            picture = discord.File(SnapshotClient.response)
            await interaction.response.send_message(file = picture)
        # todo: option to preserve renders in out/
        # await aiofiles.os.remove(SnapshotClient.response)


    # subcommand of Group
    @app_commands.command(name = "doodle")
    async def render_doodle(self, interaction: discord.Interaction) -> None:
        self.renderConfig["type"] = "doodle"
        self.renderConfig["randomDNA"] = True
        asyncio.get_event_loop().run_until_complete(SnapshotClient.requestRender(self.renderConfig))

        with open(SnapshotClient.response, 'rb') as f:
            picture = discord.File(f)
            await interaction.response.send_message(file = picture)

    # subcommand of Group
    #
    # npcnametest = {
    #     3127: "Ifalla Yufalla",
    #     3128: "Sticky George",
    #     3129: "Baker Bridget",
    #     3130: "Sandy",
    #     3131: "Lazy Lorenzo",
    #     3132: "Ashy",
    #     3133: "Dr. Friezeframe",
    #     3134: "Lounge Lassard",
    #     3135: "Soggy Nell",
    #     3136: "Happy Sue",
    #     3137: "Mr. Freeze",
    #     3138: "Chef Bumblesoup",
    #     3139: "Granny Icestockings",
    #     3140: "Fisherman Lucille",
    # }
    #
    # npcChoices = []
    #
    # for k, v in npcnametest.items():
    #     # print(k)
    #     # print(v)
    #     # print("======")
    #     npcChoices.append(
    #         app_commands.Choice(name = v, value = str(f"npc-{k}"))
    #     )
    #
    # async def npc_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    #     options = []
    #     for i in range(15):
    #         k, v = random.choice(list(NPCToonNames.items()))
    #         # print([k, v])
    #         options.append([k, v])
    #     print(options)
    #     # for k, v in options:
    #     #     print(v)
    #
    #     return [
    #         app_commands.Choice(name = entry[1], value = f"npc-{entry[0]}")
    #         for entry in options
    #     ]
    #
    # @app_commands.autocomplete(fruit = fruit_autocomplete)
    @app_commands.command(name = "suit")
    async def render_suit(self, interaction: discord.Interaction, ) -> None:
        self.renderConfig["type"] = "suit"
        self.renderConfig["randomDNA"] = False
        self.renderConfig["haphazardDNA"] = True

        asyncio.get_event_loop().run_until_complete(SnapshotClient.requestRender(self.renderConfig))

        with open(SnapshotClient.response, 'rb') as f:
            picture = discord.File(f)
            await interaction.response.send_message(file = picture)

    toon_npc_group = app_commands.Group(name = "npc", description = "This a nested group!")

    @toon_npc_group.command(name = "random", description = "NPC Toon")
    async def render_toon_npc(self, interaction: discord.Interaction) -> None:
        self.renderConfig["type"] = "npc"
        asyncio.get_event_loop().run_until_complete(SnapshotClient.requestRender(self.renderConfig))

        with open(SnapshotClient.response, 'rb') as f:
            picture = discord.File(f)
            await interaction.response.send_message(file = picture)


# unlike commands.GroupCog, you need to add this class to your tree yourself.
bot.tree.add_command(RenderGroup(bot), guild = discord.Object(id = GUILD))

#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')


# client.run(TOKEN)
bot.run(TOKEN)
