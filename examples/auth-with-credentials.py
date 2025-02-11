from pymessages.client import MessagesClient
import json

creds = MessagesClient.loadCredentialFile('credentials.json')
client = MessagesClient(creds, False)

@client.on('authenticated')
async def onAuthenticated(service):
    inbox = await service.getInbox(0,10)
    print(json.dumps(inbox, indent=4))

client.launch()
client.idle()