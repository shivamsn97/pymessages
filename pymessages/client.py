import asyncio
import json
import signal
from typing import Callable

import pyppeteer
from pyee import AsyncIOEventEmitter

from pymessages.service import MessageService


class ClientOptions: 
    headless:bool
    credentials: object

    def __init__(self,headless=False, credentials={"cookies":[], "localStorage": {}}):
        self.headless = headless
        self.credentials = credentials


class MessagesClient(AsyncIOEventEmitter):
    page: pyppeteer.page.Page
    browser: pyppeteer.browser.Browser
    groups = []
    listeners = {}
    options: ClientOptions
    is_authenticated: bool = False

    def __init__(self, credentials={"cookies":[], "localStorage": {}}, headless=True):
        super(MessagesClient, self).__init__()
        self.loop = asyncio.get_event_loop()
        try:
            self.loop.add_signal_handler(signal.SIGTERM, self.stop)
        except NotImplementedError:
            pass
        self.options = ClientOptions(headless, credentials)

    def stop(self):
        print('Pymessages stopping.')
        self.loop.stop()
        
    def launch(self):
        self.loop.run_until_complete(self._launch(self.options))

    def idle(self, close=True):
        self.loop.run_forever()


    @staticmethod
    def loadCredentialFile(path):
        with open(path) as f:
            cred = json.load(f)
        return cred

    async def _attachReqTracer(self):
        @self.page.on('request')
        def on_request(request):
            url = request.url
            # print("Check ------")
            if "Pairing/GetWebEncryptionKey" in url:
                # print("YESSSSS")
                service = MessageService(self.page)
                if not self.is_authenticated:
                    self.emit('authenticated', service) #TODO: pass credentials as well
                    self.is_authenticated = True

    
    async def _attachQrReader(self):
        await self.page.waitForSelector("body > mw-app > mw-bootstrap > div > main > mw-authentication-container > div > div.content-container > div > div.qr-code-container > div.qr-code-wrapper > mw-qr-code")
        async def _func_to_expose():
            img = await self.page.J('body > mw-app > mw-bootstrap > div > main > mw-authentication-container > div > div.content-container > div > div.qr-code-container > div.qr-code-wrapper > mw-qr-code > img')
            if img:
                src = await img.getProperty('src')
                if src:
                    self.emit('qr-code', await src.jsonValue())  # qrData = base64 qr image
        await self.page.exposeFunction('onQrChange', _func_to_expose)
        await self.page.evaluate(""" () => {
            const observer = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    if (mutation.attributeName === 'data-qr-code') {
                        // @ts-ignore
                        window.onQrChange(mutation)
                    }
                }
            })
            const img = document.querySelector("body > mw-app > mw-bootstrap > div > main > mw-authentication-container > div > div.content-container > div > div.qr-code-container > div.qr-code-wrapper > mw-qr-code")
            if (img) {
                observer.observe(img, { attributes: true, childList: true, characterData: true })
            }
            return observer
        }
        """)
        await self.page.waitForSelector('body > mw-app > mw-bootstrap > div > main > mw-authentication-container > div > div.content-container > div > div.qr-code-container > div.qr-code-wrapper > mw-qr-code > img')
        img = await self.page.J('body > mw-app > mw-bootstrap > div > main > mw-authentication-container > div > div.content-container > div > div.qr-code-container > div.qr-code-wrapper > mw-qr-code > img')
        if img:
            src = await img.getProperty("src")
            if src:
                self.emit('qr-code', await src.jsonValue())

    async def _launch(self, options: ClientOptions):
        browser = await pyppeteer.launch({"headless": options.headless})
        self.browser = browser
        page = await browser.newPage()
        self.page = page
        await self.page.goto('https://messages.android.com', { "waitUntil": 'load' })
        await self.page.waitForSelector('#mat-slide-toggle-1-input')
        await self.page.evaluate("""() => {
            const checkbox = document.querySelector('#mat-slide-toggle-1-input')
            checkbox.click() 
        }
        """) #remember me button
        self.emit('browser-launched')
        if len(options.credentials["localStorage"]) == 0:
            await self._attachQrReader()
            await self._attachReqTracer()
            return
        else:
            await self.setCredentials(options.credentials)
            service = MessageService(self.page)
            self.emit('authenticated', service)
            self.is_authenticated = True

    async def getCredentials(self):
        await self.page.waitForFunction('!!localStorage.getItem("pr_backend_type")')
        localStorageData = await self.page.evaluate("""() => {
            let data = {}
            Object.assign(data, window.localStorage)
            return data
        }
        """)
        cookiz = await self.page.cookies()
        creds = {
            "cookies": cookiz,
            "localStorage": localStorageData
        }
        return creds

    async def setCredentials(self, credentials: dict):
        await self.page.setCookie(*credentials["cookies"])
        await self.page.evaluate("""(localStorageData) => {  
            try {
                localStorageData = JSON.parse(localStorageData)
            } catch (err) {}
            for (const key of Object.keys(localStorageData)) {
                localStorage.setItem(key, localStorageData[key])
            }
        }""", json.dumps(credentials["localStorage"]))
        await self.page.reload()
        return


    async def quit(self):
        await self.browser.close()


    def __del__(self):
        self.loop.run_until_complete(self.quit())

