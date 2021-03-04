from pymessages.client import MessagesClient

creds = MessagesClient.loadCredentialFile('credentials.json')
client = MessagesClient(creds)

TO = "+919876543210"
MSG = "Test message sent using PyMessages wrapper."

@client.on('authenticated')
async def onAuthenticated(service):
    print("Sending Messages.")
    await service.sendMessage(TO, MSG)
    print("Done.")

client.launch()
client.idle()