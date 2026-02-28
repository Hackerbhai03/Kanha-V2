# -----------------------------------------------
# 🔸 KanhaMusic Project
# 🔹 Developed & Maintained by: Kanha Bots (https://github.com/TEAM-Kanha-OP)
# 📅 Copyright © 2025 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by TEAM-Kanha-OP
# -----------------------------------------------


import os
import shutil
from pyrogram import filters
from KanhaMusic import app
from KanhaMusic.misc import SUDOERS

@app.on_message(filters.command("clean") & SUDOERS)
async def clean(_, message):
    status_msg = await message.reply_text("🧹 **ᴄʟᴇᴀɴɪɴɢ ᴛᴇᴍᴘ ᴅɪʀᴇᴄᴛᴏʀɪᴇs...**")

    folders = ["downloads", "cache"]

    for folder in folders:
        # Agar folder exist kare to delete aur create kare
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)

    await status_msg.edit("✅ **ᴛᴇᴍᴘ ᴅɪʀᴇᴄᴛᴏʀɪᴇs ᴀʀᴇ ᴄʟᴇᴀɴᴇᴅ**")
