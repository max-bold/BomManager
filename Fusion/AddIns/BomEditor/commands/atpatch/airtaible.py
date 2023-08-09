# BoldM
# Basic tests on uploading Fusion360 bom to air table

# AirTable API docs: https://airtable.com/developers/web/api/introduction

from __future__ import annotations
import requests
from urllib.parse import unquote
import logging
from time import sleep
from .creds import token, baseId

from typing import Tuple
import traceback

import adsk.cam
import adsk.fusion
import adsk.core
import sys
import os
import json
libpath = os.path.dirname(os.path.realpath(__file__))+'\\lib'
sys.path.append(libpath)

scriptdir = os.path.dirname(os.path.realpath(__file__))
comptableId = 'tblM2xme4TrV4xkAN'
occtableId = 'tbl4JFd3AdUPZtW9Z'

log = logging.Logger('GetBom1', level=logging.DEBUG)
fh = logging.FileHandler(f'{scriptdir}\\atpush.log', 'w', encoding='UTF-16')
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
              data: dict = None,
              session: requests.Session = None) -> requests.Response:
    if not session:
        session = requests.Session()
    r: requests.Response = session.request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        json=data)
    log.debug(f'{unquote(r.url)} | {r.status_code} | {r.json()}')
    if r.status_code == 439:
        log.info('To much requests, waiting 30s')
        sleep(30)
        return atrequest(method, url, headers, params, data)
    else:
        return r


def atpatchcomps(comps: list[adsk.fusion.Component]) -> dict:
    results = {}
    records = []
    ids = []
    for comp in comps:
        if comp.id not in ids:
            records.append(
                {
                    "fields": {
                        "fldQNW2q1PsQp5SSq": comp.id,
                        "fldyDundYFql6ReRf": comp.partNumber,
                        "fldri55UTvgd3t39n": comp.name,
                        "fldTLteA9WZESMxuU": comp.description
                    }
                }
            )
            ids.append(comp.id)
        else:
            log.warning(
                f'Seems that diffirent components have same IDs: {comp.id}')
    session = requests.Session()
    for i in range(0, len(records), 10):
        ii = min(i+10, len(records))
        r = atrequest(
            method='PATCH',
            url=f"https://api.airtable.com/v0/{baseId}/{comptableId}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            data={
                "performUpsert": {
                    "fieldsToMergeOn": [
                        "ID"
                    ]
                },
                "records": records[i:ii]
            },
            session=session
        )
        if r.status_code == 200:
            for rec in r.json()["records"]:
                results[rec['fields']['ID']] = rec['id']
        else:
            log.warning(f'Server returned: {r.json()}')
    return results


def atfindcompbyid(compid: str) -> list[str]:
    url = f'https://api.airtable.com/v0/{baseId}/{comptableId}'
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        'filterByFormula': f'{{ID}}="{compid}"'
    }
    r = atrequest('GET', url, params=params, headers=headers)
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


def atgetoccsincomp(compid: str, session: requests.Session = None) -> list[dict]:
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
            # "fields": ["fldCbJRbZR9vLumPR"]
        },
        session=session
    )
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


def atpatchoccs(root: adsk.fusion.Component, ui: adsk.core.UserInterface) -> requests.Response:
    comps = getallcomponents(root)
    compdict = atpatchcomps(comps)
    dellist = []
    records = []
    pd = ui.createProgressDialog()
    pd.show('GetBom', 'Updating Airtable', 0, len(comps))
    session = requests.Session()
    for comp in comps:
        incomprec = compdict[comp.id]
        atoccs = atgetoccsincomp(comp.id, session)
        occs = getoccs(comp)
        ofcids = []
        for occ in occs:
            ofcids.append(occ.ofc.id)
            ofcomprec = compdict[occ.ofc.id]
            records.append({
                "fields": {
                    "ID-ID": f'{occ.ofc.id}-{occ.inc.id}',
                    "of_component": [ofcomprec],
                    "in_component": [incomprec],
                    "Count": occ.count
                }
            }
            )
        for atocc in atoccs:
            if atocc['fields']['of_component'] not in ofcids:
                dellist.append(atocc['id'])
        pd.progressValue += 1
        if pd.wasCancelled:
            break
    if dellist:
        atdeloccs(dellist)
    for i in range(0, len(records), 10):
        ii = min(i+10, len(records))
        data = {
            "performUpsert": {
                "fieldsToMergeOn": [
                    "ID-ID"
                ]
            },
            "records": records[i:ii]
        }
        r = atrequest(
            'PATCH',
            url=f'https://api.airtable.com/v0/{baseId}/{occtableId}',
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            data=data
        )
        if not r.status_code == 200:
            log.warning(f'Server returned {r.json()}')


def run(context):
    log.debug('Started')
    app = adsk.core.Application.get()
    ui = app.userInterface
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    root = design.rootComponent

    atpatchoccs(root, ui)

    log.debug('Finished')
