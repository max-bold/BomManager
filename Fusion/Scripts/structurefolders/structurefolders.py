# Author-
# Description-

import adsk.core
import adsk.fusion
import adsk.cam
import traceback
from os import mkdir, path


def getchildcomp(root: adsk.fusion.Component) -> list[adsk.fusion.Component]:
    childs: list[adsk.fusion.Component] = []
    for occ in root.occurrences:
        if occ.component not in childs:
            childs.append(occ.component)
    return childs

def getallchilds(root: adsk.fusion.Component)->dict:
    res = {}
    childs: list[adsk.fusion.Component] = []
    for occ in root.occurrences:
        if occ.component not in childs:
            childs.append(occ.component)
    for child in childs:
        res[child.name]=getallchilds(child)
    return res

def createfolder(parent:str, name:str)->str:
    try:
        p = f'{parent}/{name}'
        mkdir(p)
        return p
    except:
        # app = adsk.core.Application.get()
        # ui = app.userInterface
        # ui.messageBox(f'Failed to create folder {p}')
        print(f'Failed to create folder {p}')
        return None

def createfolders(structure:dict, rootpath:str)->None:
    for key, value in structure.items():
        newroot = createfolder(rootpath, key)
        createfolders(value, newroot)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        root = design.rootComponent
        res = getallchilds(root)
        fd = ui.createFolderDialog()
        if fd.showDialog() == adsk.core.DialogResults.DialogOK:
            createfolders(res, fd.folder)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
