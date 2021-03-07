# PYMESSAGES - Google Messages Client for Python

### What is this?
- This is a [Google Messages](https://messages.android.com) Client library to send message with a backend .eg. with flask to send otp messages. This module uses your own number to work as a sms gateway api and you can send message to other person with your own number. Ported from [messages-web by Swapnil Soni](https://github.com/SwapnilSoni1999/messages-web).

### How to use

1. install the package from [PyPI](https://pypi.org/project/pymessages/)

```sh
pip install pymessages
```

2. Use it

- Without credentials

```python
from pymessages.client import MessagesClient
import json
import base64
import re

client = MessagesClient()

@client.on('qr-code')
async def on_qr_code(base64Image):
    print("Generating qr code.")
    with open("qr.jpg", "wb") as f:
        f.write(base64.b64decode(re.sub(r'^data:image\/png;base64,','',base64Image)))

@client.on('authenticated')
async def on_authenticated(service):
    print("Authenticated")
    creds = await client.getCredentials()
    with open("credentials.json", 'w') as f:
        json.dump(creds, f, indent=4)

client.launch()
client.idle()
```
Then you can use `credentials.json` file to login .

- With credentials

```python
from pymessages.client import MessagesClient
import json

creds = MessagesClient.loadCredentialFile('credentials.json')
client = MessagesClient(creds)

@client.on('authenticated')
async def onAuthenticated(service):
    inbox = await service.getInbox(start=10, limit=20) #will return 20 elements starting from the 11th element. 
    # By default, start is 0 and limit is 50. You can set limit to -1 to return all elements after the starting point. 
    print(json.dumps(inbox, indent=4))

client.launch()
client.idle()
```

3. send message

```python
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
```

- Examples are given [here](https://github.com/shivamsn97/pymessages/tree/main/examples).

### Todos
- ~~add pagination in getInbox~~
- ~~add sendMessage in Service~~
- add public method in client to save credentials to a file
- sendMessage: parse to var to check if country code is included or not
- Rewrite docs with proper details
- detect if phone is not connected
- detect if web client is open in another browser or not
- Use logger module

# License 
ISC - Swapnil Soni &copy;