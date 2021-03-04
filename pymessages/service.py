import asyncio
import pyppeteer

class Conversation:
    unread: bool 
    id: int
    timestamp: str 
    fromNumber: str
    latestMsgText: str

    def __init__(self, unread, id, timestamp, fromNumber, latestMsgText) -> None:
        self.unread = unread
        self.id = id
        self.timestamp = timestamp
        self.fromNumber = fromNumber
        self.latestMsgText = latestMsgText

    

class MessageService: 
    page = pyppeteer.page.Page

    def __init__(self, page: pyppeteer.page.Page):
        self.page = page

    async def getInbox(self):
        # TODO: add pagination
        await self.page.waitForNavigation({"waitUntil": 'load'})
        await self.page.waitForSelector('body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > mws-conversations-list > nav > div.conv-container.ng-star-inserted > mws-conversation-list-item')

        inbox = await self.page.evaluate("""() => {
        
            function evalConvoElement (conversation) {
                const props = {
                    unread: false, // querySelector find .unread class
                    id: 0, // href of a tag
                    timestamp: '', // mws-relative-timestamp .innerText || > ..ng-star-inserted').getAttribute('aria-label') if latest message
                    from: '', // querySelector('h3').innerText
                    latestMsgText: '' // querySelector('mws-conversation-snippet').innerText
                }
                props.unread = conversation.querySelector('.unread') ? true : false
                
                const regex = /conversations\/(\d{1,})/g
                const chatUrl = conversation.querySelector('a').href
                props.id = parseInt(chatUrl.match(regex)[0].split('conversations/')[1])
                
                if (conversation.querySelector('mws-relative-timestamp').childElementCount > 0) {
                    props.timestamp = conversation.querySelector('mws-relative-timestamp > .ng-star-inserted').getAttribute('aria-label')
                } else {
                    props.timestamp = (conversation.querySelector('mws-relative-timestamp')).innerText
                }

                props.from = conversation.querySelector('h3').innerText
                props.latestMsgText = (conversation.querySelector('mws-conversation-snippet')).innerText
                if (props.latestMsgText.startsWith('You:')) {
                    props.latestMsgText = props.latestMsgText.slice('You:'.length).trim()
                }
                return props
            }

            const conversations = document.querySelectorAll("body > mw-app > mw-bootstrap > div > main > mw-main-container > div > mw-main-nav > mws-conversations-list > nav > div.conv-container.ng-star-inserted > mws-conversation-list-item")
            const msgs = []
            for (const conversation of conversations) {
                if (conversation) {
                    msgs.push(evalConvoElement(conversation))
                }
            }
            return msgs
        }
        """)
        return inbox

    async def sendMessage(self,to:str, text:str):
        pass


