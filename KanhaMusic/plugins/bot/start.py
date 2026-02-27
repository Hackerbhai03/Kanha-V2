import random
import time
import asyncio

from youtubesearchpython.__future__ import VideosSearch
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from KanhaMusic import app
from KanhaMusic.misc import _boot_
from KanhaMusic.plugins.sudo.sudoers import sudoers_list
from KanhaMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from KanhaMusic.utils.decorators.language import LanguageStart
from KanhaMusic.utils.formatters import get_readable_time
from KanhaMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


EFFECT_ID = [
    5104841245755180586,
    5107584321108051014,
]

# 🔥 BOOM STYLE CAPTIONS
START_CAPTION_PM = """
💥 𝐁𝐎𝐎𝐌 💥

{0} 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗧𝗼 𝗧𝗵𝗲 𝗠𝗼𝘀𝘁 𝗗𝗮𝗻𝗴𝗲𝗿𝗼𝘂𝘀 𝗠𝘂𝘀𝗶𝗰 𝗕𝗼𝘁 ⚡

🎧 24x7 Non-Stop Music
🚀 Ultra Fast Streaming
🔥 Zero Lag Performance
👑 Powered By {1}

💣 Haters Watching... Legends Using.
"""

START_CAPTION_GROUP = """
💥 𝐁𝐎𝐎𝐌 𝐁𝐎𝐎𝐌 💥

{0} 𝗜𝘀 𝗡𝗼𝘄 𝗔𝗰𝘁𝗶𝘃𝗲 ⚡

⏳ Uptime : {1}
🎶 Ready To Rule This Chat
👑 Let’s Make This Group Legendary
"""


async def change_img():
    while True:
        await asyncio.sleep(5)
        if hasattr(config, "START_IMAGES"):
            random.shuffle(config.START_IMAGES)


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    await message.react("🔥")

    if len(message.text.split()) > 1:
        param = message.text.split(None, 1)[1]

        # HELP PANEL
        if param.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption="💥 𝐁𝐎𝐎𝐌 💥\n\nNeed Help? I Got You 😎",
                reply_markup=keyboard,
            )

        # SUDO LIST
        if param.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            return

        # TRACK INFO
        if param.startswith("inf"):
            m = await message.reply_text("🔍 Searching Boom Track...")
            query = param.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"

            results = VideosSearch(query, limit=1)
            data = (await results.next())["result"][0]

            caption = f"""
💥 𝐓𝐑𝐀𝐂𝐊 𝐈𝐍𝐅𝐎 💥

🎵 Title : {data['title']}
⏱ Duration : {data['duration']}
👁 Views : {data['viewCount']['short']}
📅 Uploaded : {data['publishedTime']}

🔥 Powered By {app.mention}
"""

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🎧 Watch Now", url=data["link"]),
                        InlineKeyboardButton("💬 Support", url=config.SUPPORT_CHAT),
                    ]
                ]
            )

            await m.delete()
            return await app.send_photo(
                chat_id=message.chat.id,
                photo=data["thumbnails"][0]["url"].split("?")[0],
                caption=caption,
                reply_markup=buttons,
            )

    # NORMAL START
    buttons = private_panel(_)

    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=START_CAPTION_PM.format(
            message.from_user.mention,
            app.mention,
        ),
        message_effect_id=random.choice(EFFECT_ID),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    uptime = int(time.time() - _boot_)
    buttons = start_panel(_)

    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=START_CAPTION_GROUP.format(
            app.mention,
            get_readable_time(uptime),
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                await message.chat.ban_member(member.id)
                continue

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text("❌ Supergroup Required Bro!")
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text("🚫 This Chat Is Blacklisted.")
                    return await app.leave_chat(message.chat.id)

                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=f"""
💥 𝐁𝐎𝐎𝐌 𝐄𝐍𝐓𝐑𝐘 💥

Thanks {message.from_user.first_name} For Adding Me 😎

🔥 Now Let’s Rock {message.chat.title}
👑 Powered By {app.mention}
""",
                )

                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as e:
            print(e)
