"""
prob just wnanna rename this to DoodleGroup
"""

import discord
from discord import app_commands
from discord.ext import commands

from modtools.extensions.toon_snapshot.pets.PetDNAContext import PetDNAContext
from modtools.extensions.toon_snapshot.pets.PetEnums import EarType
from toontown.pets import PetDNA




class CreateDoodleView(discord.ui.View):
    def __init__(self, user: discord.User):
        """
        :param user: user reserved for this interaction
        """
        super().__init__()
        self.user = user.id

        self.context = PetDNAContext()

        # for convenience of db updates, we give the context object a pointer to the userid.
        self.context.disid = self.user

        # now that everything's ready to go, we can show the user their next options.
        self.ear_options()

    def disable_buttons(self):
        for button in self.children:
            button.disabled = True

    def is_host(self, user):
        return self.user == user

    def configure_footer(self, embed):
        embed.set_footer(
            text = str(self.context.getDNA())
        )

    # def main_menu(self):
    #     self.add_item(MainMenuButton(GameMode.FREE_PLAY, label = "Free Play"))

    def ear_options(self):
        """
        given an area, display possible paths using LocationButtons dict.
        """
        self.add_item(DoodleEarPartsDropdown())


class DoodleEarPartsDropdown(discord.ui.Select['CreateDoodleView']):
    name2id = {
        'horns': 0,
        'antennae': 1,
        'dogEars': 2,
        'catEars': 3,
        'rabbitEars': 4
    }

    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = []
        for entry in self.name2id.keys():
            options.append(
                discord.SelectOption(label = entry, value = self.name2id[entry], description = 'abcd', emoji = '🟥'),
            )

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder = 'Select Ear Type', min_values = 1, max_values = 1, options = options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.

        assert self.view is not None
        view: CreateDoodleView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not yours!.", ephemeral = True)
            return
        view.clear_items()

        view.context.EAR_TYPE = int(self.values[0])  # todo: convert to enum

        if view.context.EAR_TYPE is not EarType.Empty:
            print(view.context.EAR_TYPE)
            earName = PetDNA.EarParts[view.context.EAR_TYPE]
        else:
            earName = "None Selected"


        em = discord.Embed(
            title = "Doodle Ear Type",
            description = f"Selected Ear Type: **{earName}**",
        )

        view.configure_footer(em)

        # em.add_field(name="Rod Rarity Chance", value=f"+{abs((chance - 100)):.2f}%")
        # em.add_field(name="Rod Price", value=RodPriceDict[view.context.ROD_ID])
        #
        # rodinfo = rodDict[view.context.ROD_ID]
        # em.add_field(name="Fish Weight", value=f"Min: {rodinfo[0]}, Max: {rodinfo[1]}")
        # em.add_field(name="Rod Cast Cost", value=rodinfo[2])
        # em.add_field(name="Fish Caught w/ Rod", value=str(0))

        # rodpicture = f"rod_{view.context.ROD_ID}.png"
        # thumbnail = discord.File(f"img/{rodpicture}", filename = rodpicture)
        # em.set_thumbnail(url = f"attachment://{rodpicture}")

        view.ear_options()
        # Re-load the inventory view to show our changes.
        await interaction.response.edit_message(view = view, embed = em)

