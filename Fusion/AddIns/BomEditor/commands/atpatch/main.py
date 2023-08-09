import adsk.core
import os
from ...lib import fusion360utils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface
local_handlers = []

cmd:adsk.core.CommandDefinition=None
control:adsk.core.CommandControl=None

def start(panel:adsk.core.ToolbarPanel):
    ui.messageBox('hello world')
    resfolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')
    global cmd
    global control
    if not ui.commandDefinitions.itemById('atpatchcmd'):
        cmd = ui.commandDefinitions.addButtonDefinition('atpatchcmd','Patch',resfolder)
        control = panel.controls.addCommand(cmd)
        control.isPromoted=True
        
    pass


def stop():
    # cmd = ui.commandDefinitions.itemById('atpatchcmd')
    global cmd
    if cmd:
        cmd.deleteMe()
    global control
    if control:
        control.deleteMe()
    pass


def command_created(args: adsk.core.CommandCreatedEventArgs):
    pass


def command_execute(args: adsk.core.CommandEventArgs):
    pass


def command_preview(args: adsk.core.CommandEventArgs):
    pass


def command_input_changed(args: adsk.core.InputChangedEventArgs):
    pass


def command_destroy(args: adsk.core.CommandEventArgs):
    pass
