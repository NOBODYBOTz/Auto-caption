#testing mode
from pyrogram import Client, filters
import aiohttp
import asyncio
import requests
import time

restart_channel_id = -1001955617973
bot_tokens = ["7416279313:AAGZiCpxa_J6Zzu3jEE91nZeF0M1jp5NrzA"]

app = Client("caption_bot")

def get_bot_info(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url)
    data = response.json()
    return data["result"]["name"], data["result"]["username"]

async def check_bot_status(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return True
            else:
                return False

@app.on_message(filters.command("botstatus"))
async def bot_status(client, message):
    bots_to_check = []
    for token in bot_tokens:
        name, username = get_bot_info(token)
        bots_to_check.append({"token": token, "username": username, "name": name})
    
    msg = await message.reply_text("Checking bot status...")
    
    while True:
        for bot in bots_to_check:
            is_alive = await check_bot_status(bot["token"])
            if is_alive:
                status = f"{bot['name']} (@{bot['username']}) is alive 💖"
            else:
                status = f"{bot['name']} (@{bot['username']}) is dead 💀"
            await msg.edit_text("\n".join([status for bot in bots_to_check]))
        await asyncio.sleep(3600)

@app.on_message(filters.photo)
async def caption_photo(client, message):
    # Your existing caption bot code here

app.run()
```
