
from aiohttp import web
from pyrogram import Client, filters
from config import Rkn_Bots, Rkn_Bots as Rkn_Botz
from Rkn_Bots.web_support import web_server

class Rkn_AutoCaptionBot(Client):
    def __init__(self):
        super().__init__(
            name="Rkn-Advance-Caption-Bot",
            api_id=Rkn_Bots.API_ID,
            api_hash=Rkn_Bots.API_HASH,
            bot_token=Rkn_Bots.BOT_TOKEN,
            workers=200,
            plugins={"root": "Rkn_Bots"},
            sleep_threshold=15,
        )
        self.add_handler(self.bot_status, filters.command("botstatus"))

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.uptime = Rkn_Botz.BOT_UPTIME
        self.force_channel = Rkn_Bots.FORCE_SUB

        if Rkn_Bots.FORCE_SUB:
            try:
                link = await self.export_chat_invite_link(Rkn_Bots.FORCE_SUB)
                self.invitelink = link
            except Exception as e:
                print(e)
                print("Make Sure Bot admin in force sub channel")
                self.force_channel = None

        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Rkn_Bots.PORT).start()

        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")

        for id in Rkn_Bots.ADMIN:
            try:
                await self.send_message(id, f"**__{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
            except:
                pass

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped 🙄")

    @staticmethod
    def get_bot_info(token):
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url)
        data = response.json()
        return data["result"]["name"], data["result"]["username"]

    @staticmethod
    async def check_bot_status(token):
        url = f"https://api.telegram.org/bot{token}/getMe"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return True
                else:
                    return False

    async def bot_status(self, message):
        bots_to_check = []
        for token in ["7416279313:AAGZiCpxa_J6Zzu3jEE91nZeF0M1jp5NrzA"]:
            name, username = Rkn_AutoCaptionBot.get_bot_info(token)
            bots_to_check.append({"token": token, "username": username, "name": name})

        msg = await message.reply_text("Checking bot status...")
        while True:
            for bot in bots_to_check:
                is_alive = await Rkn_AutoCaptionBot.check_bot_status(bot["token"])
                if is_alive:
                    status = f"{bot['name']} (@{bot['username']}) is alive 💖"
                else:
                    status = f"{bot['name']} (@{bot['username']}) is dead 💀"

            await msg.edit_text("\n".join([status for bot in bots_to_check]))
            await asyncio.sleep(3600)

Rkn_AutoCaptionBot().run()
