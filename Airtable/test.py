import requests
import json
import urllib.parse as up

CSV_DATA = 'C1,C2,C3\n\
            1,2,3\n\
            4,5,25\n\
            7,8,73jkfshdjfh'
credfile = open('Airtable\creds.json', 'r')
PERSONAL_ACCESS_TOKEN = json.load(credfile)['token']
print(PERSONAL_ACCESS_TOKEN)
url = f'https://api.airtable.com/v0/applPm3xWS2CHRhkE/tblRs2T2Qdr9cvSdj/sync/exHn7ap9'
headers = {'Authorization': f'Bearer {PERSONAL_ACCESS_TOKEN}',
           'Content-Type': 'text/csv'}
r = requests.post(url, headers=headers, data=CSV_DATA)
print(r.status_code)
