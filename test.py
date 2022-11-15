import requests
import json

a = requests.post('https://geoloc.jne.co.id/jne-public/publik/get_pos',headers={"posName":"jakarta"}).json()

with open("initest.txt",'w') as file:
    file.write(json.dumps(a))