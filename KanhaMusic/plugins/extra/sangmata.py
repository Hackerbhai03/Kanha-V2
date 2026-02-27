# -----------------------------------------------
# 💎 𝐊𝐀𝐍𝐇𝐀 𝐌𝐔𝐒𝐈𝐂 - 𝐒𝐔𝐏𝐄𝐑 𝐔𝐋𝐓𝐑𝐀 𝐒𝐆 𝐌𝐎𝐃𝐔𝐋𝐄 💎
# 🚀 Developed & Maintained by: TEAM-Kanha-OP
# 👑 Power Packed • Royal Styled • Haters Destroyer Edition
# 📅 Copyright © 2025 – All Rights Reserved
#
# ⚠️ License:
# This source code is for educational & non-commercial use ONLY.
# Removing credits = Direct disrespect.
# Commercial use without permission is strictly prohibited.
#
# ❤️ Made with Passion, Power & Royal Attitude
# -----------------------------------------------

import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from pyrogram.raw.functions.messages import DeleteHistory
from KanhaMusic import userbot as us, app
from KanhaMusic.core.userbot import assistants


# 🔥 SG COMMAND — ROYAL EDITION
@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):

    # ⚡ Argument Check
    if len(message.command) == 1 and not message.reply_to_message:
        return await message.reply_text(
            "💎 𝐊𝐀𝐍𝐇𝐀 𝐒𝐆 𝐒𝐘𝐒𝐓𝐄𝐌 💎\n\n"
            "➤ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴜsᴇʀ ɪᴅ / ᴜsᴇʀɴᴀᴍᴇ\n"
            "➤ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ\n\n"
            "⚡ ᴅᴏɴ’ᴛ ᴛᴇsᴛ ᴍᴇ ᴡɪᴛʜᴏᴜᴛ ɪɴᴘᴜᴛ 😉"
        )

    # 🎯 Get Target User
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.text.split()[1]

    loading = await message.reply_text(
        "🔎 𝐊𝐀𝐍𝐇𝐀 𝐒𝐂𝐀𝐍𝐍𝐈𝐍𝐆...\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "⚡ ᴄᴏʟʟᴇᴄᴛɪɴɢ ʜɪsᴛᴏʀʏ..."
    )

    try:
        user = await client.get_users(user_id)
    except Exception:
        return await loading.edit_text(
            "❌ 𝐈𝐍𝐕𝐀𝐋𝐈𝐃 𝐔𝐒𝐄𝐑 ❌\n\n"
            "➤ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɪᴅ / ᴜsᴇʀɴᴀᴍᴇ."
        )

    # 🎲 Random Sangmata Bot
    sangmata_bots = ["sangmata_bot", "sangmata_beta_bot"]
    target_bot = random.choice(sangmata_bots)

    # 🤖 Assistant Check
    if 1 in assistants:
        ubot = us.one
    else:
        return await loading.edit_text(
            "❌ 𝐍𝐎 𝐀𝐒𝐒𝐈𝐒𝐓𝐀𝐍𝐓 𝐔𝐒𝐄𝐑𝐁𝐎𝐓 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 ❌"
        )

    # 🚀 Send ID to Sangmata
    try:
        sent = await ubot.send_message(target_bot, str(user.id))
        await sent.delete()
    except Exception as e:
        return await loading.edit_text(
            f"❌ 𝐄𝐑𝐑𝐎𝐑 ❌\n\n{e}"
        )

    await asyncio.sleep(2)

    found = False

    # 🔍 Search Response
    async for msg in ubot.search_messages(target_bot):
        if not msg.text:
            continue

        await message.reply_text(
            f"💎 𝐊𝐀𝐍𝐇𝐀 𝐒𝐆 𝐑𝐄𝐒𝐔𝐋𝐓 💎\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 𝐓𝐚𝐫𝐠𝐞𝐭: {user.mention}\n"
            f"🆔 𝐈𝐃: <code>{user.id}</code>\n\n"
            f"📜 𝐇𝐢𝐬𝐭𝐨𝐫𝐲:\n"
            f"{msg.text}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⚡ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲 𝐊𝐚𝐧𝐡𝐚 𝐌𝐮𝐬𝐢𝐜",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("❌ 𝐂𝐋𝐎𝐒𝐄", callback_data="close_sg")]]
            ),
        )

        found = True
        break

    if not found:
        await message.reply_text(
            "❌ 𝐍𝐎 𝐑𝐄𝐒𝐏𝐎𝐍𝐒𝐄 ❌\n\n"
            "sᴀɴɢᴍᴀᴛᴀ ʙᴏᴛ ᴅɪᴅ ɴᴏᴛ ʀᴇᴘʟʏ.\n"
            "ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
        )

    # 🧹 Clear History (Stealth Mode)
    try:
        peer = await ubot.resolve_peer(target_bot)
        await ubot.send(DeleteHistory(peer=peer, max_id=0, revoke=True))
    except Exception:
        pass

    await loading.delete()


# ❌ Close Button Handler
@app.on_callback_query(filters.regex("close_sg"))
async def close_sg_callback(client: Client, query: CallbackQuery):
    await query.message.delete()
    await query.answer("💎 𝐊𝐀𝐍𝐇𝐀 𝐒𝐘𝐒𝐓𝐄𝐌 𝐂𝐋𝐎𝐒𝐄𝐃 💎", show_alert=False)
