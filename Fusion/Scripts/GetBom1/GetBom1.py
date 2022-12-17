# Author-
# Description-
# import sys
# sys.path.append()

from __future__ import annotations
from typing import Tuple
import traceback
import requests
import adsk.cam
import adsk.fusion
import adsk.core
import sys
import os
import json
libpath = os.path.dirname(os.path.realpath(__file__))+'\\lib'
sys.path.append(libpath)
# for path in sys.path:
#     print(path)


class Occurrence(object):
    def __init__(self, ofcomponent: adsk.fusion.Component, incomponent: adsk.fusion.Component, count: int = 0) -> None:
        self.ofc = ofcomponent
        self.inc = incomponent
        self.count = count

    def __eq__(self, other: Occurrence) -> bool:
        return other.ofc.id == self.ofc.id and other.inc.id == self.inc.id


def getallcomponents(root: adsk.fusion.Component) -> list[adsk.fusion.Component]:
    components = []
    for occ in root.allOccurrences:
        if occ.component not in components:
            components.append(occ.component)
    return components


def getcomponents(root: adsk.fusion.Component) -> list[adsk.fusion.Component]:
    components = []
    for occ in root.occurrences:
        if occ.component not in components:
            components.append(occ.component)
    return components


def getalloccs(root: adsk.fusion.Component) -> list[Occurrence]:
    occlist: list[Occurrence] = []
    components = getallcomponents(root)
    components.append(root)
    for parent in components:
        for child in getcomponents(parent):
            newocc = Occurrence(child,
                                parent,
                                parent.occurrencesByComponent(child).count)
            occlist.append(newocc)
    return occlist


def getoccs(root: adsk.fusion.Component) -> list[Occurrence]:
    occlist: list[Occurrence] = []
    for child in getcomponents(root):
        newocc = Occurrence(child,
                            root,
                            root.occurrencesByComponent(child).count)
        occlist.append(newocc)
    return occlist


def getflatoccs(root: adsk.fusion.Component) -> list[Occurrence]:
    occlist: list[Occurrence] = []
    for comp in getallcomponents(root):
        newocc = Occurrence(comp,
                            root,
                            root.allOccurrencesByComponent(comp).count)
        occlist.append(newocc)
    return occlist


def comptocsv(components: list[adsk.fusion.Component]) -> str:
    out = 'ID,Part_number,Name,Description\n'
    for comp in components:
        out += ','.join([comp.id, comp.partNumber,
                        comp.name, comp.description])+'\n'
    return out


def occstocsv(occs: list[Occurrence]) -> str:
    out = 'ID,of_id,in_id,count\n'
    for occ in occs:
        id = f'{occ.ofc.id}-{occ.inc.id}'
        out += ','.join([id, occ.ofc.id, occ.inc.id, str(occ.count)])+'\n'
    return out


token = "pat2QOIhhU65h1xZx.ab0f75c773fafb9c5b2d301e68810d198bc127e2403cd87a110a7a419ff5421e"
baseId = 'appWxxU0dgHGJgHGZ'


def atpush(baseId: str, tableIdOrName: str, apiEndpointSyncId: str, data: str, token: str):

    url = f'https://api.airtable.com/v0/{baseId}/{tableIdOrName}/sync/{apiEndpointSyncId}'
    headers = {'Authorization': f'Bearer {token}',
               'Content-Type': 'text/csv'}
    r = requests.post(url, headers=headers, data=data)
    return r.status_code


def atpatchcomps(baseId: str, tableIdOrName: str, comps: list[adsk.fusion.Component], token: str) -> requests.Response:
    url = f"https://api.airtable.com/v0/{baseId}/{tableIdOrName}"
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    data = {
        "performUpsert": {
            "fieldsToMergeOn": [
                "ID"
            ]
        },
        "records": []
    }
    for comp in comps:
        rec = {
            "fields": {
                "ID": comp.id,
                "fldyDundYFql6ReRf": comp.partNumber,
                "fldri55UTvgd3t39n": comp.name,
                "fldTLteA9WZESMxuU": comp.description
            }
        }
        data["records"].append(rec)
    data = json.dumps(data)
    print(data)
    r = requests.patch(url, headers=headers, data=data)
    return r


def atfindcompbyid(baseId: str, tableIdOrName: str, compid: str, token: str) -> list[str]:
    url = f'https://api.airtable.com/v0/{baseId}/{tableIdOrName}'
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        'filterByFormula': f'{{ID}}="{compid}"'
    }
    r = requests.get(url, params, headers=headers)
    if r.status_code == 200:
        data = r.json()
        recs = []
        for rec in data['records']:
            recs.append(rec['id'])
    # print(r.request.url)
    return recs


def atpatchoccs(baseId: str, tableIdOrName: str, occs: list[Occurrence], token: str, comptable: str) -> requests.Response:
    url = f"https://api.airtable.com/v0/{baseId}/{tableIdOrName}"
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    data = {
        "performUpsert": {
            "fieldsToMergeOn": [
                "fldCbJRbZR9vLumPR",
                "fldMzBNkOmQJp79RK"
            ]
        },
        "records": []
    }
    for occ in occs:
        ofrecids = atfindcompbyid(baseId, comptable, occ.ofc.id, token)
        inrecids = atfindcompbyid(baseId, comptable, occ.inc.id, token)
        if ofrecids and inrecids:
            rec = {
                "fields": {
                    "fldCbJRbZR9vLumPR": ofrecids[0],
                    "fldMzBNkOmQJp79RK": inrecids[0],
                    "fldLzjR1TVjprJEyC": str(occ.count)
                }
            }
            data["records"].append(rec)
    data = json.dumps(data)
    print(data)
    r = requests.patch(url, headers=headers, data=data)
    return r


# curl -X POST https://api.airtable.com/v0/appWxxU0dgHGJgHGZ/tblCyjuFbzWfv87hE/sync/S37lqFJ2 \
# -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
# -H "Content-Type: text/csv" \
# --data "${CSV_DATA}"

# curl -X POST https://api.airtable.com/v0/appWxxU0dgHGJgHGZ/tblDVobcZyLq24mCW/sync/rhE1polT \
# -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
# -H "Content-Type: text/csv" \
# --data "${CSV_DATA}"

# curl -X POST https://api.airtable.com/v0/appWxxU0dgHGJgHGZ/tblsxOLCYtnpeEbqs/sync/khX2A1ds \
# -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
# -H "Content-Type: text/csv" \
# --data "${CSV_DATA}"


def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    root = design.rootComponent
    # print('Components:')
    # # for comp in getallcomponents(root):
    # #     print(f'{comp.name} ({comp.id})')
    # comps = getallcomponents(root)
    # print(atpush('appWxxU0dgHGJgHGZ',
    #              'tblCyjuFbzWfv87hE',
    #              'S37lqFJ2',
    #              comptocsv(comps)))

    # print(comptocsv(comps))
    # print('Occurrences:')
    # # for occ in getalloccs(root):
    # #     print(f'of {occ.ofc.name} in {occ.inc.name} count: {occ.count}')
    # occs = getalloccs(root)
    # print(atpush('appWxxU0dgHGJgHGZ',
    #              'tblsxOLCYtnpeEbqs',
    #              'khX2A1ds',
    #              occstocsv(occs)))
    # print(occstocsv(occs))
    # comps = getallcomponents(root)
    # print('Patch components:', atpatchcomps(
    #     baseId='appWxxU0dgHGJgHGZ',
    #     tableIdOrName='tblM2xme4TrV4xkAN',
    #     comps=comps,
    #     token=token
    # ).status_code)
# https://airtable.com/appWxxU0dgHGJgHGZ/tblM2xme4TrV4xkAN/viwxkQ9BfX8nKHA9Z/rec2eBRrZFx6x7Ldk/fldQNW2q1PsQp5SSq?copyLinkToCellOrRecordOrigin=gridView
    occs = getalloccs(root)
    print('Patch occs:', atpatchoccs(
        baseId=baseId,
        tableIdOrName='tbl4JFd3AdUPZtW9Z',
        comptable='tblM2xme4TrV4xkAN',
        occs=occs,
        token=token
    ).json())

    # print(atfindcompbyid(baseId,
    #                      tableIdOrName='tblM2xme4TrV4xkAN',
    #                      compid='7610b7b7-0afc-4565-b4fb-a298b413071f',
    #                      token=token).json())
