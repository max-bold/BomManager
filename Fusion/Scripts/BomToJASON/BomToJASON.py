# Author- BM
# Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import json


def getallcomponents(root: adsk.fusion.Component) -> list[adsk.fusion.Component]:
    components = [root]
    ids = [root.id]
    for occ in root.allOccurrences:
        if occ.component.id not in ids:
            components.append(occ.component)
            ids.append(occ.component.id)
    return components


def getcomponents(root: adsk.fusion.Component) -> list[adsk.fusion.Component]:
    components = []
    for occ in root.occurrences:
        if occ.component not in components:
            components.append(occ.component)
    return components


def getbom(root: adsk.fusion.Component):
    components = getallcomponents(root)
    occurences = []
    compdicts = []
    for component in components:
        compdicts.append(
            {
                "id": component.id,
                "PartNumber": component.partNumber,
                "Description": component.description,
            }
        )
        for child in getcomponents(component):
            occurences.append(
                {
                    "InComp": component.id,
                    "OfComp": child.id,
                    "Count": component.allOccurrencesByComponent(child).count,
                }
            )
    return {"Components": compdicts, "Occurences": occurences}


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        root = design.rootComponent
        bom = getbom(root)
        with open(
            "F:/CODE/BomManager/Fusion/Scripts/BomToJASON/bom.json",
            "w",
            encoding="utf16",
        ) as out:
            _as_json = json.dumps(bom, indent=4, ensure_ascii=False)
            out.write(_as_json)
        print("Done")
    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
