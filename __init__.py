import sys, os

# storing the directory in dir variable
OP_DIR = os.path.dirname(__file__)
sys.path.append(OP_DIR)

if __name__ == '__main__':
    from modtools.modbase import ModularStart
    from modtools.modbase.ModularBase import ModularBase

    base = ModularBase()

from panda3d.core import loadPrcFile, ConfigVariableManager, loadPrcFileData, ConfigVariableInt, ConfigVariableBool, \
    ConfigVariableString

"""
Modify config/config_snapshot.prc instead of this file!
DO NOT EDIT
"""
loadPrcFile('modtools/extensions/toon_snapshot/config/config_snapshot.prc')
SNAPSHOT_HOST = ConfigVariableString("snapshot-host", "localhost").getValue()
SNAPSHOT_PORT = ConfigVariableInt("snapshot-port", 20151).getValue()
SNAPSHOT_HEADLESS = ConfigVariableBool("snapshot-headless", 1).getValue()
SNAPSHOT_DEBUG = ConfigVariableBool("snapshot-debug", 0).getValue()

SNAPSHOT_RES = ConfigVariableInt("snapshot-res", 1024).getValue()
SNAPSHOT_EXTENSION = ConfigVariableString("snapshot-extension", ".png").getValue()
SNAPSHOT_DIR = ConfigVariableString("snapshot-dir", "out").getValue()
SNAPSHOT_PREFIX = ConfigVariableString("snapshot-prefix", "render_").getValue()
SNAPSHOT_KEEP_RENDERS = ConfigVariableBool("snapshot-keep-renders", 0)
SNAPSHOT_CLEANUP_TIME = ConfigVariableBool("snapshot-cleanup-time", 60)
SNAPSHOT_TRIM_WHITESPACE = ConfigVariableBool("snapshot-trim-whitespace", 1)

DISCORD_TOKEN = ConfigVariableString("snapshot-discord-token", "unknown").getValue()
DISCORD_GUILD = ConfigVariableString("snapshot-discord-guild", 'none').getValue()
DISCORD_BOT_OWNER = ConfigVariableString("snapshot-discord-owner", '141314236998615040').getValue()

# Graphics config
loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 4")
loadPrcFileData('', 'texture-anisotropic-degree %d' % 16)


if __name__ == '__main__':
    # ConfigVariableManager.getGlobalPtr().listVariables()
    # ConfigVariableManager.getGlobalPtr().listDynamicVariables()
    # print(base.config.GetString('snapshot-host', 'unknown'))
    # print(base.config.GetInt('snapshot-port', 1))
    # print(test)
    # c = Config().DISCORD_TOKEN
    print(SNAPSHOT_HOST)

    # print(c)
    base.run()
