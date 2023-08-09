# Here you define the commands that will be added to your add-in.

# TODO Import the modules corresponding to the commands you created.
# If you want to add an additional command, duplicate one of the existing directories and import it here.
# You need to use aliases (import "entry" as "my_module") assuming you have the default module named "entry".
from .commandDialog import entry as commandDialog
from .paletteShow import entry as paletteShow
from .paletteSend import entry as paletteSend
from .atpatch import main as atpatch
import adsk.core

app = adsk.core.Application.get()
ui = app.userInterface

# TODO add your imported modules to this list.
# Fusion will automatically call the start() and stop() functions.
commands = [
    # commandDialog,
    # paletteShow,
    # paletteSend
    atpatch
]


# Assumes you defined a "start" function in each of your modules.
# The start function will be run when the add-in is started.
def start():
    ws = ui.workspaces.itemById('FusionSolidEnvironment')
    tb = ws.toolbarTabs.itemById('BMtab')
    if not tb:
        tb = ws.toolbarTabs.add('BMtab','BOM Manager')
    tb.activate()
    atpanel = tb.toolbarPanels.itemById('ATtab')
    if not atpanel:
        atpanel = tb.toolbarPanels.add('ATtab','AirTable')
    # for command in commands:
    #     command.start()
    atpatch.start(atpanel)


# Assumes you defined a "stop" function in each of your modules.
# The stop function will be run when the add-in is stopped.
def stop():
    for command in commands:
        command.stop()
    ws = ui.workspaces.itemById('FusionSolidEnvironment')
    tb = ws.toolbarTabs.itemById('BMtab')
    atpanel = tb.toolbarPanels.itemById('ATtab')
    # if atpanel:
    #     atpanel.deleteMe()
    if tb:
        tb.deleteMe()

    