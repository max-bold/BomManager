import json

with open("Tries&Failures\FurgeClient1\creds.json", "r") as file:
    data:dict = json.load(file)
    for key, value in data.items():
        print(f'{key}: {value}')