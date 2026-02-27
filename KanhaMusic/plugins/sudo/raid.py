import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from KanhaMusic import app
from KanhaMusic.misc import SUDOERS

MAX_LIMIT = 10  # Safety Limit

@app.on_message(filters.command("mention", prefixes=".") & SUDOERS)
async def mention_notify(client, message: Message):

    try:
        await message.delete()
    except:
        pass

    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ **𝐔sᴀɢᴇ:** `.mention username count message`"
        )

    # 🎯 Get User
    try:
        user = await client.get_users(message.command[1])
        target = user.mention
    except Exception:
        return await message.reply_text(
            "❌ **𝐈ɴᴠᴀʟɪᴅ 𝐔sᴇʀɴᴀᴍᴇ / 𝐈𝐃**"
        )

    # 🔢 Count
    try:
        count = int(message.command[2])
        if count > MAX_LIMIT:
            count = MAX_LIMIT
    except:
        count = 3

    # 📝 Message
    text = " ".join(message.command[3:]) if len(message.command) > 3 else "👋 𝐇ᴇʟʟᴏ!"

    # 🚀 Send Mentions (Rate Limited)
    for _ in range(count):
        try:
            await message.reply_text(f"{target} **{text}**")
            await asyncio.sleep(2)
        except FloodWait as e:
            await asyncio.sleep(e.value)
