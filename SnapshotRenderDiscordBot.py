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
if guild.isdigit():
    MY_GUILD = discord.Object(id = DISCORD_GUILD)  # replace with your guild id
else:
    MY_GUILD = None

# Since the NPC Toon dict is unfathomably large, let's pregenerate a lookup dict.
NpcToonNames_name2id = {
    toonName.lower().replace(" ", "").replace(".", ""): toonID for toonID, toonName in NPCToonNames.items()
}


# asyncio.run(prepare_bot_tree(DISCORD_GUILD != -1))

class SnapshotRenderBot(commands.Bot):
    def __init__(self, intents, command_prefix, description):
        super().__init__(intents = intents, command_prefix = command_prefix, description = description)
        self.pfp = None

    async def prepare_bot_tree(self):
        print(f"Preparing bot tree (guild = {MY_GUILD})")
        # self.tree.clear_commands(guild = MY_GUILD)
        self.tree.add_command(RenderGroup(bot), guild = MY_GUILD)

        if MY_GUILD:
            # This copies the global commands over to your guild.
            self.tree.copy_global_to(guild = MY_GUILD)

        await self.tree.sync(guild = MY_GUILD)

    def setup_bot_pfp(self):
        renderArgs = {
            "RENDER_TYPE": RenderType.Toon,
            "WANT_NAMETAG": False,
            "FRAME_TYPE": FrameType.Headshot,

        }
        asyncio.get_event_loop().run_until_complete(SnapshotRenderClient.requestRender(renderArgs))
        response = json.loads(SnapshotRenderClient.response)

        pfp_path = response["RENDER_IMAGE"]
        fp = open(pfp_path, 'rb')
        self.pfp = fp.read()
        return self.pfp

    async def prepare_bot_presence(self):
        # Since we're calling this from on_ready, which may be called multiple times, let's ensure we haven't
        # setup a profile picture already.
        if self.pfp:
            return
        # do an initial toon render here and set the bots pfp to it
        # ( might be good to do a headshot/toptoons pic for it as well
        self.setup_bot_pfp()
        await self.user.edit(avatar = self.pfp)
        await self.change_presence(activity = discord.Activity(type = discord.ActivityType.competing, name = "toontow"))

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
        await self.prepare_bot_presence()


intents = discord.Intents.default()
intents.message_content = True  # required for dropdown

bot = SnapshotRenderBot(command_prefix = '/', description = 'blah', intents = intents)


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


# Define a simple View that gives us a confirmation menu
class ToggleRenderAttributesView(discord.ui.View):
    def __init__(self, embed):
        super().__init__()
        self.value = None
        self.embed = embed

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
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

    @discord.ui.button(label = 'Random ToonTask', style = discord.ButtonStyle.primary)
    async def regenerate_quest(self, interaction: discord.Interaction, button: discord.ui.Button):
        em, file = generateQuestEmbed(interaction.user.display_name)
        await interaction.response.edit_message(embed = em, view = self)


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

    tip = random.choice(tipChoices)

    """Sends the text into the current channel."""
    em = discord.Embed(
        title = "Toon Tip",
        description = tip
    )
    em.set_footer(text = f"Total Toon Tips loaded: {len(tipChoices)})")

    await interaction.response.send_message(embed = em)


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
        toon_name = "Name of Toon",
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
            say: Optional[str] = None, muzzle_type: MuzzleType = None
    ):
        renderConfig = RenderSettings.RenderSettings().renderConfig

        # ToonSnapshot will handle it from here ~
        renderConfig["NAME"] = toon_name
        renderConfig["WANT_NAMETAG"] = nametag
        renderConfig["FRAME_TYPE"] = frame_type
        renderConfig["CUSTOM_PHRASE"] = say
        renderConfig["CHAT_BUBBLE_TYPE"] = chatbubble_type
        renderConfig["EYE_TYPE"] = eye_type
        renderConfig["MUZZLE_TYPE"] = muzzle_type

        if not npc:
            renderConfig["RENDER_TYPE"] = RenderType.Toon
        else:
            renderConfig["RENDER_TYPE"] = RenderType.NPC
            # see if the user chose an autocomplete or manually typed in their selection
            # autocomplete will give us the npcid with an npc- prefix
            npcID = npc.replace('npc-', '')
            if npcID.isdigit():
                renderConfig["NPC_ID"] = int(npcID)
            else:
                # User tried passing in the name of an npc, most likely
                # get rid of spaces and period requirements
                npcName = npcID.replace(" ", "").replace(".", "")
                npcID = NpcToonNames_name2id.get(npcName)
                if not npcID:
                    await interaction.response.send_message("Sorry, I couldn't find that NPC Toon!", ephemeral = True)
                    return
                else:
                    renderConfig["NPC_ID"] = npcID
            # em, file = generateNPCRender(RenderArgs)
        file, embed = self.render_image(renderConfig)

        # Add on to the embed
        if npc:
            npcInfo = self.generateNpcInfo(renderConfig["NPC_ID"])
            for name, value in npcInfo.items():
                embed.add_field(name = name, value = value)
        await interaction.response.send_message(file = file, embed = embed)

    @app_commands.command(name = "doodle")
    @app_commands.describe(
        random_dna = 'unfinished',
        say = "Make Doodle say input phrase",
        doodle_name = "Name of Doodle (default random)",
        nametag = "Display nametag? (defualt True)"
    )
    async def render_doodle(
            self, interaction: discord.Interaction,
            random_dna: Optional[bool] = True,
            say: Optional[str] = None, doodle_name: Optional[str] = None, nametag: Optional[bool] = True,
            chatbubble_type: Optional[ChatBubbleType] = ChatBubbleType.Normal,

    ):
        renderConfig = RenderSettings.RenderSettings().renderConfig

        renderConfig["RENDER_TYPE"] = RenderType.Doodle
        # renderConfig["DNA_RANDOM"] = random_dna
        renderConfig["NAME"] = doodle_name
        renderConfig["WANT_NAMETAG"] = nametag
        renderConfig["CUSTOM_PHRASE"] = say
        renderConfig["CHAT_BUBBLE_TYPE"] = chatbubble_type

        file, embed = self.render_image(renderConfig)
        await interaction.response.send_message(file = file, embed = embed)

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


bot.run(DISCORD_TOKEN)
