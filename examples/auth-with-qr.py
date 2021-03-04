from pymessages.client import MessagesClient
import json
import base64
import re

client = MessagesClient(headless=False)

@client.on('qr-code')
async def on_qr_code(base64Image):
    print("Generating qr code.")
    with open("qr.jpg", "wb") as f:
        f.write(base64.b64decode(re.sub(r'^data:image\/png;base64,','',base64Image)))

@client.on('browser-launched')
async def on_browser_launched():
    print("--------------------------------------\nBROWSER LAUNCHED\n-------------------------------------")

@client.on('authenticated')
async def on_authenticated(service):
    print("Authenticated")
    creds = await client.getCredentials()
    with open("credentials.json", 'w') as f:
        json.dump(creds, f, indent=4)

client.launch()
client.idle()
