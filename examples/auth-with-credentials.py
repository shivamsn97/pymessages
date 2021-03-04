from pymessages.client import MessagesClient
import json

creds = MessagesClient.loadCredentialFile('credentials.json')
client = MessagesClient(creds)

@client.on('authenticated')
async def onAuthenticated(service):
    inbox = await service.getInbox()
    print(json.dumps(inbox, indent=4))

client.launch()
client.idle()