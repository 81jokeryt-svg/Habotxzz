import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os, time, asyncio, requests
from threading import Thread
from pyrogram import types, Client, StopPropagation
from pyrogram.handlers import MessageHandler

# Flask import
from web import run_server 
from info import LOG_CHANNEL, API_ID, API_HASH, BOT_TOKEN, PORT
from utils import temp, check_premium
from database.users_chats_db import db

class Bot(Client):
    def __init__(self):
        super().__init__(
            name='Auto_Filter_Bot',
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"}
        )
        self.listeners = {}
        self.add_handler(MessageHandler(self._listener_handler), group=-1)

    async def _listener_handler(self, client: Client, message: types.Message):
        if not message.chat or not message.from_user: return
        listener_id = (message.chat.id, message.from_user.id)
        if listener_id in self.listeners:
            future = self.listeners[listener_id]
            if not future.done(): future.set_result(message)
            raise StopPropagation

    # --- Self Ping (Cron Job) logic ---
    async def keep_alive(self):
        while True:
            await asyncio.sleep(600) # Har 10 minute mein ping karega
            try:
                # Render URL ko ping karein taaki bot active rahe
                requests.get(f"http://0.0.0.0:{PORT}")
                logger.info("Self-ping: Keep-Alive sent!")
            except:
                pass

    async def start(self, **kwargs):
        await super().start()
        temp.START_TIME = time.time()
        
        # Flask Server Start (In background thread)
        Thread(target=run_server, daemon=True).start()
        
        # Self Ping Start
        asyncio.create_task(self.keep_alive())

        me = await self.get_me()
        temp.ME, temp.U_NAME = me.id, me.username
        
        asyncio.create_task(check_premium(self))
        try:
            await self.send_message(chat_id=LOG_CHANNEL, text=f"<b>{me.mention} Started with Flask!</b>")
        except:
            pass
        logger.info(f"@{me.username} is running on Port {PORT}")

app = Bot()
app.run()
