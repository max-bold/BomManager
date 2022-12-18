# BoldM
# Basic tests on uploading Fusion360 bom to air table

# AirTable API docs: https://airtable.com/developers/web/api/introduction

from __future__ import annotations
from typing import Tuple
import traceback

import adsk.cam
import adsk.fusion
import adsk.core
import sys
import os
import json
# libpath = os.path.dirname(os.path.realpath(__file__))+'\\lib'
# sys.path.append(libpath)
# import requests
from .creds import token, baseId
from .lib import requests
from time import sleep
import logging
from urllib.parse import unquote
from .lib.progress.bar import ChargingBar

scriptdir = os.path.dirname(os.path.realpath(__file__))
comptableId = 'tblM2xme4TrV4xkAN'
occtableId = 'tbl4JFd3AdUPZtW9Z'

log = logging.Logger('GetBom1', level=logging.DEBUG)
fh = logging.FileHandler(f'{scriptdir}\\getbom.log', 'w')
hf = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
fh.setFormatter(hf)
log.addHandler(fh)
log.debug('Script loaded')


class Occurrence(object):
    def __init__(self, ofcomponent: adsk.fusion.Component, incomponent: adsk.fusion.Component, count: int = 0) -> None:
        self.ofc = ofcomponent
        self.inc = incomponent
        self.count = count

    def __eq__(self, other: Occurrence) -> bool:
        return other.ofc.id == self.ofc.id and other.inc.id == self.inc.id


def getallcomponents(root: adsk.fusion.Component) -> list[adsk.fusion.Component]:
    components = [root]
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


def atpush(baseId: str, tableIdOrName: str, apiEndpointSyncId: str, data: str, token: str):

    url = f'https://api.airtable.com/v0/{baseId}/{tableIdOrName}/sync/{apiEndpointSyncId}'
    headers = {'Authorization': f'Bearer {token}',
               'Content-Type': 'text/csv'}
    r = requests.post(url, headers=headers, data=data)
    return r.status_code


def atrequest(method: str,
              url: str,
              headers: dict = None,
              params: dict = None,
              data: dict = None) -> requests.Response:
    r: requests.Response = requests.request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        json=data)
    if r.status_code == 439:
        log.info('To much requests, waiting 30s')
        sleep(30)
        return atrequest(method, url, headers, params, data)
    else:
        return r


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
    r = requests.patch(url, headers=headers, data=data)
    return r

# https://airtable.com/appWxxU0dgHGJgHGZ/tblM2xme4TrV4xkAN/viwxkQ9BfX8nKHA9Z/fldQNW2q1PsQp5SSq


def atfindcompbyid(compid: str) -> list[str]:
    url = f'https://api.airtable.com/v0/{baseId}/{comptableId}'
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        'filterByFormula': f'{{ID}}="{compid}"'
    }
    r = requests.get(url, params, headers=headers)
    if r.status_code == 200:
        data = r.json()
        if len(data['records']) == 1:
            return data['records'][0]['id']
        else:
            log.warning(
                f'Found {len(data["records"])} records for component {compid}')
            return None
    else:
        log.warning(f'Server returned: {r.json()}')
        return None


# def atgetoccsincomp(compid: str):
#     comprecids = atfindcompbyid(compid)
#     if len(comprecids) == 1:
#         comprecid = comprecids[0]
#     else:
#         logging.warning(f'Found {len(comprecids)} records for {compid}')


def atfindcomp(comp: adsk.fusion.Component) -> str:
    r = atrequest(
        'GET',
        url=f'https://api.airtable.com/v0/{baseId}/{comptableId}',
        headers={"Authorization": f"Bearer {token}"},
        params={'filterByFormula': f'{{ID}}="{comp.id}"'})
    if r.status_code == 200:
        if len(r.json()['records']) == 1:
            return r.json()['records'][0]['id']
        else:
            log.info(
                f'Found {len(r.json()["records"])} records for component {comp.id}')
            return None
    else:
        log.warning(f'Server returned {r.json()}')


def atcreatecomp(comp: adsk.fusion.Component) -> str:
    r = atrequest(
        'POST',
        url=f'https://api.airtable.com/v0/{baseId}/{comptableId}',
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"},
        data={
            "records": [
                {
                    "fields": {
                        "fldQNW2q1PsQp5SSq": comp.id,
                        "fldyDundYFql6ReRf": comp.partNumber,
                        "fldri55UTvgd3t39n": comp.name,
                        "fldTLteA9WZESMxuU": comp.description
                    }
                }
            ]
        }
    )
    if r.status_code == 200:
        return r.json()['records'][0]['id']
    else:
        log.warning(f'Server returned {r.json()}')


def atfindcomporadd(comp: adsk.fusion.Component) -> str:
    comprecid = atfindcomp(comp)
    if not comprecid:
        comprecid = atcreatecomp(comp)
    return comprecid


def atgetoccsincomp(compid: str) -> list[dict]:
    r = atrequest(
        'GET',
        url=f'https://api.airtable.com/v0/{baseId}/{occtableId}',
        headers={
            "Authorization": f"Bearer {token}"
        },
        params={
            "filterByFormula": f'{{in_component}} = "{compid}"',
            "cellFormat": "string",
            "userLocale": "ru",
            "timeZone": "Asia/Tbilisi"
        }
    )
    # print(unquote(r.url))
    if r.status_code == 200:
        return r.json()['records']
    else:
        log.warning(f'Server returned {r.json()}')


def atcreateocc(ofcompid: str, incompid: str, count: int) -> requests.Response:
    return atrequest(
        'POST',
        url=f'https://api.airtable.com/v0/{baseId}/{occtableId}',
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        data={
            "records": [
                {
                    "fields": {
                        "fldCbJRbZR9vLumPR": [ofcompid],
                        "fldMzBNkOmQJp79RK": [incompid],
                        "fldLzjR1TVjprJEyC": count
                    }
                }
            ]
        }
    )


def atdeloccs(recidlist: list[str]) -> None:
    if len(recidlist) > 1:
        r = atrequest(
            'DELETE',
            url=f'https://api.airtable.com/v0/{baseId}/{occtableId}',
            params={
                "records": recidlist
            },
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
    else:
        r = atrequest(
            'DELETE',
            url=f'https://api.airtable.com/v0/{baseId}/{occtableId}/{recidlist[0]}',
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
    if not r.status_code == 200:
        log.warning(f'Server returned {r.json()}')


def atpatchoccs(root: adsk.fusion.Component) -> requests.Response:
    
    data = {
        "performUpsert": {
            "fieldsToMergeOn": [
                "ID-ID"
            ]
        },
        "records": []
    }
    dellist = []
    ocscount = len(getalloccs(root))
    i=0
    for comp in getallcomponents(root):
        incomprec = atfindcomporadd(comp)
        atoccs = atgetoccsincomp(comp.id)
        occs = getoccs(comp)
        if not occs:
            print(f'Done: {i}/{ocscount}')
            i+=1
        ofcids = []
        for occ in occs:
            ofcids.append(occ.ofc.id)
            ofcomprec = atfindcomporadd(occ.ofc)
            data['records'].append({
                "fields": {
                    "ID-ID": f'{occ.ofc.id}-{occ.inc.id}',
                    "of_component": [ofcomprec],
                    "in_component": [incomprec],
                    "Count": occ.count
                }
            }
            )
            print(f'Done: {i}/{ocscount}')
            i+=1
        
        for atocc in atoccs:
            if atocc['fields']['of_component'] not in ofcids:
                dellist.append(atocc['id'])
    if dellist:
        atdeloccs(dellist)
    if data['records']:
        r = atrequest(
            'PATCH',
            url=f'https://api.airtable.com/v0/{baseId}/{occtableId}',
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            data=data
        )
        # print(r.json())

            # if occ.ofc.id
            # pass
            # def atgetallocs() -> list[Occurrence]:
            #     url = f'https://api.airtable.com/v0/{baseId}/{occtableId}'
            #     headers = {
            #         "Authorization": f"Bearer {token}"
            #     }
            #     r = atrequest('GET', url)
            #     print(r.json())
            # occs:list[Occurrence] = []
            # if r.status_code == 200:
            #     for record in r.json()['records']:
            #         pass


def run(context):
    log.debug('Started')
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
    #     baseId=baseId,
    #     tableIdOrName='tblM2xme4TrV4xkAN',
    #     comps=comps,
    #     token=token
    # ).status_code)
# https://airtable.com/appWxxU0dgHGJgHGZ/tblM2xme4TrV4xkAN/viwxkQ9BfX8nKHA9Z/rec2eBRrZFx6x7Ldk/fldQNW2q1PsQp5SSq?copyLinkToCellOrRecordOrigin=gridView
    # occs = getalloccs(root)
    # print('Patch occs:', atpatchoccs(
    #     baseId=baseId,
    #     tableIdOrName='tbl4JFd3AdUPZtW9Z',
    #     comptable='tblM2xme4TrV4xkAN',
    #     occs=occs,
    #     token=token
    # ).json())

    # print(atfindcompbyid(baseId,
    #                      tableIdOrName='tblM2xme4TrV4xkAN',
    #                      compid='7610b7b7-0afc-4565-b4fb-a298b413071f',
    #                      token=token).json())
    # for i in range(100):
    # atgetallocs()
    # print(atfindcomp2('7610b7b7-0afc-4565-b4fb-a297b413071f'))
    # # log.debug('Finished')
    # for comp in getallcomponents(root):
    #     print(atcreatecomp(comp))
    # rec = atfindcompbyid('dd1ab7d6-c85c-4ae2-b9a8-6a9a675a9e55')
    # print(rec)
    # occs = atgetoccsincomp('dd1ab7d6-c85c-4ae2-b9a8-6a9a675a9e55')
    # dellist = []
    # for occ in occs:
    #     dellist.append(occ['id'])
    # print(atdeloccs(dellist).json())
    # r=  atcreateocc(
    #     ofcompid=atfindcompbyid('dd1ab7d6-c85c-4ae2-b9a8-6a9a675a9e55'),
    #     incompid=atfindcompbyid('fe4556af-d61c-4173-b9ac-c247e641194b'),
    #     count=10
    # )
    # print(r.request.body)
    # print(r.status_code)
    # print(r.json())
    atpatchoccs(root)
    log.debug('Finished')
