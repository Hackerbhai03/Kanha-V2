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

from pyrogram import filters
from pyrogram.types import Message
from KanhaMusic import app
from KanhaMusic.core.call import Kanha

welcome = 20
close = 30


@app.on_message(filters.video_chat_started, group=welcome)
@app.on_message(filters.video_chat_ended, group=close)
async def welcome(_, message: Message):
    await Kanha.stop_stream_force(message.chat.id)
