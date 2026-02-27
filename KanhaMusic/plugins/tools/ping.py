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

import random
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from KanhaMusic import app
from KanhaMusic.core.call import Kanha
from KanhaMusic.utils import bot_sys_stats
from KanhaMusic.utils.decorators.language import language
from KanhaMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL

Kanha_PIC = [

    "https://files.catbox.moe/vbdda6.jpg",
    "https://files.catbox.moe/3up9ky.jpg",
    "https://files.catbox.moe/jktiak.jpg",
    "https://files.catbox.moe/0n4439.jpg",
    "https://files.catbox.moe/l2id2z.jpg",
    "https://files.catbox.moe/l2id2z.jpg",
    "https://files.catbox.moe/8c6zfn.jpg",
    "https://files.catbox.moe/to3v10.jpg",
    "https://files.catbox.moe/mcqu0j.jpg",
    "https://files.catbox.moe/2803m5.jpg",
    "https://files.catbox.moe/gf3142.jpg",
    "https://files.catbox.moe/gcqh0j.jpg"

]

@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        photo=random.choice(Kanha_PIC),
        has_spoiler=True,
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Kanha.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
