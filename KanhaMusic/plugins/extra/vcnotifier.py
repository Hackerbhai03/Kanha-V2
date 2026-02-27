# -----------------------------------------------
# 💎 𝐊𝐀𝐍𝐇𝐀 𝐌𝐔𝐒𝐈𝐂 - 𝐕𝐈𝐃𝐄𝐎 𝐂𝐇𝐀𝐓 𝐀𝐍𝐍𝐎𝐔𝐍𝐂𝐄𝐑 💎
# 🚀 Developed & Maintained by: TEAM-Kanha-OP
# 👑 Royal Edition • Boom Boom Style • Clean & Powerful
# 📅 Copyright © 2025 – All Rights Reserved
#
# ⚠️ License:
# This source code is open for educational and non-commercial use ONLY.
# Removing credits is strictly prohibited.
#
# ❤️ Made with dedication, passion & power
# -----------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import Message
import logging
from KanhaMusic import app

logging.basicConfig(level=logging.INFO)


# 🎥 VIDEO CHAT STARTED HANDLER
@app.on_message(filters.video_chat_started)
async def video_chat_started(client: Client, message: Message):
    chat = message.chat

    await message.reply_text(
        f"💎 𝐕𝐈𝐃𝐄𝐎 𝐂𝐇𝐀𝐓 𝐀𝐋𝐄𝐑𝐓 💎\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🎥 𝐒𝐓𝐀𝐓𝐔𝐒: 𝐋𝐈𝐕𝐄 𝐍𝐎𝐖\n"
        f"🏷 𝐂𝐇𝐀𝐓: {chat.title}\n\n"
        f"⚡ ᴛʜᴇ sᴛᴀɢᴇ ɪs sᴇᴛ!\n"
        f"👑 ᴊᴏɪɴ ɴᴏᴡ ᴀɴᴅ ᴇɴᴊᴏʏ ᴛʜᴇ ᴠɪʙᴇ!\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🚀 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲 𝐊𝐚𝐧𝐡𝐚 𝐌𝐮𝐬𝐢𝐜"
    )


# 🚫 VIDEO CHAT ENDED HANDLER
@app.on_message(filters.video_chat_ended)
async def video_chat_ended(client: Client, message: Message):
    chat = message.chat

    await message.reply_text(
        f"💎 𝐕𝐈𝐃𝐄𝐎 𝐂𝐇𝐀𝐓 𝐔𝐏𝐃𝐀𝐓𝐄 💎\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🚫 𝐒𝐓𝐀𝐓𝐔𝐒: 𝐄𝐍𝐃𝐄𝐃\n"
        f"🏷 𝐂𝐇𝐀𝐓: {chat.title}\n\n"
        f"👋 ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴊᴏɪɴɪɴɢ!\n"
        f"🔥 sᴇᴇ ʏᴏᴜ ɪɴ ᴛʜᴇ ɴᴇxᴛ sᴇssɪᴏɴ.\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👑 𝐊𝐚𝐧𝐡𝐚 𝐌𝐮𝐬𝐢𝐜 𝐒𝐲𝐬𝐭𝐞𝐦"
    )
