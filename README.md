# ToonSnapshotBot
*Powered by the [modtools](https://github.com/loonaticx/modtools) library!*

# Installation
This library serves as an *extension* module of the modtools library. Keep in mind that this is currently only supported in sources using Python 3+.

While the bot can be configured to run on other Toontown sources, the development of the bot has been based off [this](https://github.com/loonaticx/open-toontown/tree/custom/custom) custom fork of open-toontown.

If you're unsure where to install the bot, feel free to clone the fork with:
```commandline
git clone https://github.com/loonaticx/open-toontown --branch custom/custom
cd open-toontown
```
---
First, clone the base ``modtools`` into the root of your Toontown source:
```commandline
git clone https://github.com/loonaticx/modtools
```

By the end, your file structure should look similar to something like:
```
- src
    - astron
    - modtools
        - toon_snapshot
    - otp
    - toontown
    - win32
    - resources
    ...
```

## Configuring Services
### Linux
``cp -r etc /etc``

## Debugging
Of course, it's not going to be pretty straightforward for a module like this to work on *any* Toontown source.
That being said, you may need to edit your source files a bit:

```commandline
  File "F:\toontown\modtools\modbase\ModularBase.py", line 37, in __init__
    ToonBase.ToonBase.__init__(self, self.selectedPipe)
TypeError: __init__() takes 1 positional argument but 2 were given
```
If you get an error similar to this, we just need to add an extra argument to pass on to ToonBase (then passed to OTPBase)

Go into ``toontown/toonbase/ToonBase`` and edit the following:
```python
class ToonBase(OTPBase.OTPBase):
    # ...

    def __init__(self):
        # ...
        pass
```
Change ``def __init__(self):`` to ``def __init__(self, pipe='pandagl'):``

In the ``__init__`` method of ToonBase, change ``OTPBase.OTPBase.__init__(self)`` to ``OTPBase.OTPBase.__init__(self, pipe)``

## "Improper Login Token"
```python
    raise LoginFailure('Improper token has been passed.') from exc
discord.errors.LoginFailure: Improper token has been passed.
```
Make sure you don't have any quotations around your discord token and/or guild id.





# Ignore below

```commandline


/ : command or subcommand


/render
    /toon
        - dnastring: optional>None
            > dictates if randomDNA will be used or not; None=randomDNA
        - muzzle: optional>default
            > autocomplete
        - eyes: optional>default
            > autocomplete
        - nametag: optional>True
            > if False, code should not consider setName
        - name: optional>None
            > if None, generate random name
        - pose: optional>random ** random may include more if over limit?
            > autocomplete: neutral, pose names
        - cheesyeffect: optional>None
        - picture_type: optional>fullbody
            > autocomplete: toptoons, fullbody, headshot
        
    /npc
        - npcid: optional>None
            > if not None, take in a string and convert it to its npc id equivalent
            > have an autocomplete list for notable NPC toons
            > maybe have a check to see if input is just ints to skip name check
        - nametag: optional>true
        - pose: optional>random
        - info: optional>False
            > print extra info about the npc, including the shop name (street and pg too), if toon is random dna'd, npc type, etc
        
    /doodle
    /cog
    /custom
        - selection menu using discord.ui.View
        - possibly as subcommands too? `/custom toon head` can return client sided preview pictures
        - ephermal / client sided input
        - once a cog/toon/doodle is selected and a preset is generated, 
        - use the same message, maybe arrows to go back and forth?
        - use reference images for showing options, can we do that with local image storage
        - variation options can always have a "random" tag at the end
        - should be fun to have an absolute true random generation
        ** do not know how this will work with paralell unless we can GET A RENDER QUEUE
        ** idk how im gonna generate clothing since there's so many, accessories too
        Choose Between:
        | Cog
        | Toon
            | Species
                > possible to include image of all species?
                | cat, dog, etc., random
            | Gender
                > possibly buttons instead of a dropdown
                | male, female, random
            | Head Type
                > possible to show a picture of all the different head styles?
            | Head Color
                > show color list
            | Eyes
                | normal, normal closed, angry, etc.
            | Muzzle Type
                | yeah
            | Torso Type
                > ditto, should we pre-render a template toon with applied changes? (ephermal)
                > image should keep editing itself until user is complete
            | Torso Color
            | Leg Type
                > ditto
            | Leg Color
            | Pose
                > buttons
                | Preset
                    > preset ids in a friendly name
                | Custom
                    | Animation
                        > show text list of all possible toon anims
                    | Frame
                        > get it with anim entered
                    | Offset: optional>(0, 0, 0, 0, 0, 0, 0, 0, 0)
                        > xyz hpr SxSySz
                        > i dont think im gonna do this anytime soon lol
            | Cheesy Effect
            | Name
        | Doodle 

```
