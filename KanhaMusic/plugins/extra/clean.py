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
    # Step 1: Status message in Open Telegraph style
    status_msg = await message.reply_text("🧹 **𝐂ʟᴇᴀɴɪɴɢ 𝐓ᴇᴍᴘ 𝐃ɪʀᴇᴄᴛᴏʀɪᴇs...**")

    folders = ["downloads", "cache"]

    # Step 2: Safely delete and recreate folders
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

    # Step 3: Done message in Open Telegraph style
    await status_msg.edit("✅ **𝐓ᴇᴍᴘ 𝐃ɪʀᴇᴄᴛᴏʀɪᴇs 𝐀ʀᴇ 𝐂ʟᴇᴀɴᴇᴅ!**")
