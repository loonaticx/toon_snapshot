from typing import Optional, List

import asyncio

import json

import discord
from discord import app_commands
from discord.ext import commands

from modtools.extensions.toon_snapshot import SnapshotRenderClient
from toontown.toon import NPCToons

from toontown.toonbase import TTLocalizerEnglish as localizer
import random

from toontown.toonbase.TTLocalizerEnglish import NPCToonNames
from . import *
from modtools.extensions.toon_snapshot.snapshot.RenderEnums import *
from modtools.extensions.toon_snapshot.snapshot import RenderSettings

import aiofiles
import aiofiles.os

import nest_asyncio

nest_asyncio.apply()

guild = DISCORD_GUILD
if guild == -1:
    pass
else:
    MY_GUILD = discord.Object(id = DISCORD_GUILD)  # replace with your guild id

RenderArgs = {
    # /render
    "RENDER_TYPE": RenderType.Toon,
    "WANT_NAMETAG": True,
    "CHAT_BUBBLE_TYPE": ChatBubbleType.Normal,
    "CUSTOM_PHRASE": None,  # alt to speedchat phrase; not none = user gave input
    "FRAME_TYPE": FrameType.Random,

    # /render: context-specific
    "NAME": None,  # generate random if None
    "DNA_RANDOM": True,
    "DNA_HAPHAZARD": False,  # Special cases like the Suits
    "SPEEDCHAT_PHRASE": None,  # speedchat phrase id if not None
    "POSE_PRESET": None,  # context specific, None -> random
    "DNA_STRING": None,  # generate random dna if None, might be a literal dna (list; not netstring)

    # /toon and /npc
    "EYE_TYPE": EyeType.NormalOpen,
    "MUZZLE_TYPE": MuzzleType.Neutral,

    # /npc
    "NPC_ID": None,  # none -> random

}


class SnapshotRenderBot(commands.Bot):
    def __init__(self, intents, command_prefix, description):
        super().__init__(intents = intents, command_prefix = command_prefix, description = description)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        if guild:
            await self.tree.sync()
        else:
            self.tree.copy_global_to(guild = MY_GUILD)
            await self.tree.sync(guild = MY_GUILD)


intents = discord.Intents.default()
intents.message_content = True  # required for dropdown

bot = SnapshotRenderBot(command_prefix = '/', description = 'blah', intents = intents)
client = bot

global bot_pfp
bot_pfp = None


def setup_bot_pfp():
    global bot_pfp
    if bot_pfp:
        return
    renderArgs = {
        "RENDER_TYPE": RenderType.Toon,
        "WANT_NAMETAG": False,
        "FRAME_TYPE": FrameType.Headshot,

    }
    asyncio.get_event_loop().run_until_complete(SnapshotRenderClient.requestRender(renderArgs))
    response = json.loads(SnapshotRenderClient.response)

    pfp_path = response["RENDER_IMAGE"]
    fp = open(pfp_path, 'rb')
    bot_pfp = fp.read()
    return bot_pfp


setup_bot_pfp()


@bot.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    # do an initial toon render here and set the bots pfp to it
    # ( might be good to do a headshot/toptoons pic for it as well
    pfp = bot_pfp
    await bot.user.edit(avatar = pfp)
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.competing, name = "toontow"))


def generateQuestEmbed(avName="Toon", questID=None):
    quests = localizer.QuestDialogDict
    if not questID:
        questID, dialog = random.choice(list(quests.items()))
    else:
        dialog = quests[questID]

    dialog = dialog.get(localizer.QUEST).replace('\a', '\n').replace('_avName_', f'**{avName}**')

    em = discord.Embed(
        title = "ToonTask",
        description = dialog,
    )
    em.set_footer(text = f"Quest ID: {questID}\nTotal Quest Entries: {len(quests)}", icon_url = "attachment://task.png")

    file = discord.File(f"{OP_DIR}/img/task.png", filename = "task.png")
    em.set_thumbnail(url = "attachment://task.png")
    return (em, file)


def generateNpcInfo(npcID):
    # set NpcInfo attrs here by looking up npcID stuff
    print(npcID)
    print(NPCToons.NPCToonDict.get(npcID)[0])
    bldg = localizer.zone2TitleDict[NPCToons.NPCToonDict.get(npcID)[0]]
    info = {
        # 2309(npcid)[0] = bldgid
        "Building": bldg,
        "Location": "Punchline Place, Toontown Central",
        "Type": "Shopkeeper",
        "Random DNA": "False"
    }
    return info


def generateNPCRender(renderArgs):
    """
    DO NOT DIRECTLY CALL FROM ME unless you are part of the toon command
    """
    # generate toonsnapshot, pass args if needed?
    asyncio.get_event_loop().run_until_complete(SnapshotRenderClient.requestRender(renderArgs))

    with open(SnapshotRenderClient.response, 'rb') as f:
        fname = SnapshotRenderClient.response.replace(f"{SNAPSHOT_DIR}/", "")
        file = discord.File(SnapshotRenderClient.response)

    # file = discord.File(f"{OP_DIR}/test/image_test.png", filename = "image_test.png")

    # get npc info
    npcID = renderArgs.get("NPC_ID")
    if not npcID:
        npcID = random.choice(list(NPCToons.NPCToonDict.items()))[0]
    npcInfo = generateNpcInfo(npcID)
    # RenderArgs["RENDER_TYPE"] = RenderType.NPC

    em = discord.Embed(
        title = "NPC Toon",
        description = f"{NPCToonNames.get(npcID)}",
    )
    em.set_image(url = f"attachment://{fname}")

    for name, value in npcInfo.items():
        em.add_field(name = name, value = value)

    em.set_footer(text = f"NPC ID: {npcID} (420 NPCs total)")
    return em, file


# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label = 'Red', description = 'Your favourite colour is red', emoji = '🟥'),
            discord.SelectOption(label = 'Green', description = 'Your favourite colour is green', emoji = '🟩'),
            discord.SelectOption(label = 'Blue', description = 'Your favourite colour is blue', emoji = '🟦'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder = 'Choose your favourite colour...', min_values = 1, max_values = 1,
                         options = options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


# Define a simple View that gives us a confirmation menu
class ToggleRenderAttributesView(discord.ui.View):
    def __init__(self, embed):
        super().__init__()
        self.value = None
        self.embed = embed

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label = 'Toggle Nametag', style = discord.ButtonStyle.secondary)
    async def toggle_nametag(self, interaction: discord.Interaction, button: discord.ui.Button):
        file = discord.File(f"{OP_DIR}/img/test/image_test_full.png", filename = "image_test_full.png")
        self.embed.set_image(url = "attachment://image_test_full.png")
        await interaction.response.edit_message(attachments = [file], embed = self.embed, view = self)
        # await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        # self.stop()

    @discord.ui.button(label = 'Randomize', style = discord.ButtonStyle.primary)
    async def new_render(self, interaction: discord.Interaction, button: discord.ui.Button):
        # re-render whatever we just rendered but ensure random dna, or random npc id, or random whatever is set
        await interaction.response.send_message(f'placeholder entry', ephemeral = True)


# Define a simple View that gives us a confirmation menu
class GenerateQuestView(discord.ui.View):
    def __init__(self, icon):
        super().__init__()
        self.icon = icon

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label = 'Random ToonTask', style = discord.ButtonStyle.primary)
    async def regenerate_quest(self, interaction: discord.Interaction, button: discord.ui.Button):
        em, file = generateQuestEmbed(interaction.user.display_name)
        await interaction.response.edit_message(embed = em, view = self)


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


@bot.command()
async def color(ctx):
    """Sends a message with our dropdown containing colours"""

    # Create the view containing our dropdown
    view = DropdownView()

    # Sending a message containing our view
    await ctx.send('Pick your favourite colour:', view = view)


@bot.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@bot.tree.command()
@app_commands.describe(
    first_value = 'The first value you want to add something to',
    second_value = 'The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')


# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@bot.tree.command()
async def quest(interaction: discord.Interaction, quest_id: Optional[int] = None):
    # QuestDialogDict may only be mainline tasks though.? if QuestDict focuses on JFF this will add on to the count

    em, file = generateQuestEmbed(interaction.user.display_name, questID = quest_id)
    # todo: integrate Quests.py to fix _where_ and others
    # todo: replace QuestDialogDict with Quests.QuestDict
    view = GenerateQuestView(file)

    await interaction.response.send_message(embed = em, view = view, file = file)
    await view.wait()


@bot.tree.command()
async def holiday(interaction: discord.Interaction):
    holidays = localizer.HolidayNamesInCalendar
    id, holiday = random.choice(list(holidays.items()))
    em = discord.Embed(
        title = holiday[0],
        description = holiday[1]
    )
    em.set_footer(text = f"Holiday ID: {id}\nTotal Holiday Entries: {len(holidays)}")
    await interaction.response.send_message(embed = em)


# @bot.tree.command()
# async def stats(interaction: discord.Interaction):
#     # collect cool toontown stats like total unique name combinations
#     holidays = localizer.HolidayNamesInCalendar
#     id, holiday = random.choice(list(holidays.items()))
#     em = discord.Embed(
#         title = holiday[0],
#         description = holiday[1]
#     )
#     em.set_footer(text = f"Holiday ID: {id}\nTotal Holiday Entries: {len(holidays)}")
#     await interaction.response.send_message(embed=em)


@bot.tree.command()
async def building(interaction: discord.Interaction, count: Optional[bool] = False):
    bldgs = localizer.zone2TitleDict
    bldgName = ""
    if count:
        await interaction.response.send_message(f"Total Building Entries = {len(bldgs)}")
    else:
        # Since this command spits out building names, we don't want to it to print *nothing*
        while not bldgName:
            _, title = random.choice(list(bldgs.items()))
            bldgName = title[0]
        await interaction.response.send_message(bldgName)


@bot.tree.command()
async def knockknock(interaction: discord.Interaction, general_jokes: Optional[bool] = True,
                     contest_jokes: Optional[bool] = True):
    jokeChoices = []
    if general_jokes:
        jokeChoices += localizer.KnockKnockJokes
    if contest_jokes:
        # this is formatted much differently than the general jokes
        for jokeid in localizer.KnockKnockContestJokes.keys():
            if isinstance(localizer.KnockKnockContestJokes[jokeid], dict):
                for i in localizer.KnockKnockContestJokes[jokeid].keys():
                    jokeChoices += [localizer.KnockKnockContestJokes[jokeid][i]]
            else:
                jokeChoices += [localizer.KnockKnockContestJokes[jokeid]]

    if not jokeChoices:
        await interaction.response.send_message(f"Hey! You need at least one option to be True!", ephemeral = True)
        return

    jokeIndex = random.randrange(len(jokeChoices))
    first, second = jokeChoices[jokeIndex]

    em = discord.Embed(
        title = "Knock Knock Joke!",
        description = f"**Knock Knock**\n*Who's there?*\n**{first}**\n*{first} who?*\n**{second}**"
    )
    em.set_footer(text = f"Selected Joke #{jokeIndex} (out of {len(jokeChoices)})")

    await interaction.response.send_message(embed = em)


@bot.tree.command()
async def emtest(interaction: discord.Interaction):

    # file2 = discord.File(f"{OP_DIR}/test/image_toon_full.png", filename = "image_toon_full.png")

    # embed = discord.Embed()
    # await channel.send(file = file, embed = embed)
    em, file = generateNPCRender(RenderArgs)

    # in future, pass file since it'll be re=rendered
    # NB: make it easier just re-render and use that output??? but then cache.. fuck
    # maybe have an option to pass a custom file name to toonrender
    view = ToggleRenderAttributesView(embed = em)

    await interaction.response.send_message(files = [file], embed = em, view = view)
    await view.wait()
    if view.value is None:
        print('Timed out...')
    elif view.value:
        # this is where you would re-call the toon render operation?
        # actually this might be called after the view :b so no
        print("confirm")
    else:
        print('Cancelled...')


@bot.tree.command()
async def toontip(interaction: discord.Interaction,
                  general_tip: Optional[bool] = True, street_tip: Optional[bool] = True,
                  minigame_tip: Optional[bool] = True, coghq_tip: Optional[bool] = True,
                  estate_tip: Optional[bool] = True, karting_tip: Optional[bool] = True,
                  golf_tip: Optional[bool] = True,
                  count: Optional[bool] = False):
    tips = localizer.TipDict
    # del tips[localizer.TIP_NONE]
    tipChoices = ()
    if general_tip:
        tipChoices += tips[localizer.TIP_GENERAL]
    if street_tip:
        tipChoices += tips[localizer.TIP_STREET]
    if minigame_tip:
        tipChoices += tips[localizer.TIP_MINIGAME]
    if coghq_tip:
        tipChoices += tips[localizer.TIP_COGHQ]
    if estate_tip:
        tipChoices += tips[localizer.TIP_ESTATE]
    if karting_tip:
        tipChoices += tips[localizer.TIP_KARTING]
    if golf_tip:
        tipChoices += tips[localizer.TIP_GOLF]

    if not tipChoices:
        await interaction.response.send_message(f"Hey! You need at least one option to be True!", ephemeral = True)
        return

    """Sends the text into the current channel."""
    if count:
        # QuestDialogDict may only be mainline tasks though.? if QuestDict focuses on JFF this will add on to the count
        await interaction.response.send_message(f"Total Toon Tip Entries = {len(tipChoices)}")
    else:
        tip = random.choice(tipChoices)
        await interaction.response.send_message(tip)


# todo: option to preserve renders in out/


# @app_commands.guild_only()
class RenderGroup(app_commands.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        self.name = "render"


    def render_image(self, render_config):
        # run the render process
        asyncio.get_event_loop().run_until_complete(SnapshotRenderClient.requestRender(render_config))
        response = json.loads(SnapshotRenderClient.response)
        image_path_nodir = response["RENDER_IMAGE"].replace(f"{SNAPSHOT_DIR}/", "")
        image = discord.File(response["RENDER_IMAGE"])
        # async with aiofiles.open(SnapshotRenderClient.response, 'rb') as f:
        em = discord.Embed(
            title = response["ACTOR_NAME"],
            description = f"Description",
            color = discord.Color.from_str("#49F147"),
        )
        em.set_image(url = f"attachment://{image_path_nodir}")

        # Generate disclaimer footer
        custom_name = bool(render_config["NAME"])

        footer = f"Custom name: {custom_name} | "
        em.set_footer(text = footer)

        return image, em

    async def npc_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        options = []
        for i in range(15):
            k, v = random.choice(list(NPCToonNames.items()))
            options.append([k, v])
        return [
            app_commands.Choice(name = entry[1], value = f"npc-{entry[0]}")
            for entry in options
        ]

    @app_commands.command(name = "toon")
    @app_commands.describe(
        random_dna = 'Render a Random Toon',
        npc = "Name of NPC to render",
        toon_name = "Name of toon",
        nametag = "Display nametag?"
    )
    @app_commands.autocomplete(
        npc = npc_autocomplete
    )
    async def render_toon(
            self, interaction: discord.Interaction,
            random_dna: Optional[bool] = True, npc: Optional[str] = None,
            toon_name: Optional[str] = None, nametag: Optional[bool] = True,
            frame_type: Optional[FrameType] = FrameType.Bodyshot,
            eye_type: Optional[EyeType] = EyeType.NormalOpen,
            chatbubble_type: Optional[ChatBubbleType] = ChatBubbleType.Normal,
            say: Optional[str] = None):
        renderConfig = RenderSettings.RenderSettings().renderConfig

        # ToonSnapshot will handle it from here ~
        renderConfig["NAME"] = toon_name
        renderConfig["WANT_NAMETAG"] = nametag
        renderConfig["FRAME_TYPE"] = frame_type
        renderConfig["CUSTOM_PHRASE"] = say
        renderConfig["CHAT_BUBBLE_TYPE"] = chatbubble_type
        renderConfig["EYE_TYPE"] = eye_type
        if not npc:
            renderConfig["RENDER_TYPE"] = RenderType.Toon
        else:
            renderConfig["RENDER_TYPE"] = RenderType.NPC
            # todo: check to see if user passed actual npc toon name manually,
            # convert the name to the id if possible
            renderConfig["NPC_ID"] = int(npc.replace('npc-', ''))
            # em, file = generateNPCRender(RenderArgs)
        file, embed = self.render_image(renderConfig)

        # Add on to the embed
        if npc:
            npcInfo = self.generateNpcInfo(renderConfig["NPC_ID"])
            for name, value in npcInfo.items():
                embed.add_field(name = name, value = value)
        await interaction.response.send_message(file = file, embed = embed)

    @app_commands.command(name = "doodle")
    async def render_doodle(
            self, interaction: discord.Interaction, random_dna: Optional[bool] = True,
            say: Optional[str] = None, doodle_name: Optional[str] = None, nametag: Optional[bool] = True,

    ) -> None:
        renderConfig = RenderSettings.RenderSettings().renderConfig

        renderConfig["RENDER_TYPE"] = RenderType.Doodle
        renderConfig["DNA_RANDOM"] = random_dna
        renderConfig["NAME"] = doodle_name
        renderConfig["WANT_NAMETAG"] = nametag
        renderConfig["CUSTOM_PHRASE"] = say

        file, embed = self.render_image(renderConfig)
        await interaction.response.send_message(file = file, embed = embed)

    def generateNpcInfo(self, npcID):
        # set NpcInfo attrs here by looking up npcID stuff
        bldg = localizer.zone2TitleDict[NPCToons.NPCToonDict.get(npcID)[0]][0]
        info = {
            # 2309(npcid)[0] = bldgid
            "Building": bldg,
            "Location": "Punchline Place, Toontown Central (placeholder)",
            "Type": "Shopkeeper (placeholder)",
            "Random DNA": "False (placeholder)"
        }
        return info

    @app_commands.command(name = "suit")
    async def render_suit(
            self, interaction: discord.Interaction,
            random_dna: SuitDNAType = SuitDNAType.Random,
            suit_name: Optional[str] = None, nametag: Optional[bool] = True,
            frame_type: Optional[FrameType] = FrameType.Bodyshot,
            chatbubble_type: Optional[ChatBubbleType] = ChatBubbleType.Normal,
            say: Optional[str] = None
    ):
        renderConfig = RenderSettings.RenderSettings().renderConfig
        renderConfig["RENDER_TYPE"] = RenderType.Suit
        renderConfig["DNA_RANDOM"] = random_dna == SuitDNAType.Random
        renderConfig["DNA_HAPHAZARD"] = random_dna == SuitDNAType.Haphazard
        renderConfig["WANT_NAMETAG"] = nametag
        renderConfig["CUSTOM_PHRASE"] = say
        renderConfig["FRAME_TYPE"] = frame_type
        renderConfig["NAME"] = suit_name
        renderConfig["CHAT_BUBBLE_TYPE"] = chatbubble_type

        file, embed = self.render_image(renderConfig)
        await interaction.response.send_message(file = file, embed = embed)



if guild == -1:
    bot.tree.add_command(RenderGroup(bot))
else:
    bot.tree.add_command(RenderGroup(bot), guild = discord.Object(id = DISCORD_GUILD))

bot.run(DISCORD_TOKEN)
