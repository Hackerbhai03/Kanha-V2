from pyrogram import filters, Client
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from unidecode import unidecode

from KanhaMusic import app
from KanhaMusic.misc import SUDOERS
from KanhaMusic.utils.database import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)

# ==============================
# 🔊 ACTIVE VOICE CHATS
# ==============================

@app.on_message(filters.command(["activevc", "activevoice", "vc"]) & SUDOERS)
async def active_voice(_, message: Message):
    mystic = await message.reply_text("🔥 ɢᴇᴛᴛɪɴɢ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs...")

    served_chats = await get_active_chats()
    text = ""
    count = 0

    for chat_id in served_chats:
        try:
            chat = await app.get_chat(chat_id)
            title = unidecode(chat.title).upper()
            username = chat.username
        except:
            await remove_active_chat(chat_id)
            continue

        count += 1

        if username:
            text += f"<b>{count}.</b> <a href='https://t.me/{username}'>{title}</a>\n"
        else:
            text += f"<b>{count}.</b> {title}\n"

    if count == 0:
        await mystic.edit_text("❌ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ʀɪɢʜᴛ ɴᴏᴡ.")
    else:
        await mystic.edit_text(
            f"<b>🔥 ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ({count}) :</b>\n\n{text}",
            disable_web_page_preview=True,
        )


# ==============================
# 🎥 ACTIVE VIDEO CHATS
# ==============================

@app.on_message(filters.command(["activevc", "activevideo", "vc"]) & SUDOERS)
async def active_video(_, message: Message):
    mystic = await message.reply_text("🔥 ɢᴇᴛᴛɪɴɢ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs...")

    served_chats = await get_active_video_chats()
    text = ""
    count = 0

    for chat_id in served_chats:
        try:
            chat = await app.get_chat(chat_id)
            title = unidecode(chat.title).upper()
            username = chat.username
        except:
            await remove_active_video_chat(chat_id)
            continue

        count += 1

        if username:
            text += f"<b>{count}.</b> <a href='https://t.me/{username}'>{title}</a> [<code>{chat_id}</code>]\n"
        else:
            text += f"<b>{count}.</b> {title} [<code>{chat_id}</code>]\n"

    if count == 0:
        await mystic.edit_text("❌ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs ʀɪɢʜᴛ ɴᴏᴡ.")
    else:
        await mystic.edit_text(
            f"<b>🔥 ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs ({count}) :</b>\n\n{text}",
            disable_web_page_preview=True,
        )


# ==============================
# 📊 ACTIVE COUNT INFO
# ==============================

@app.on_message(filters.command(["ac", "av"]) & SUDOERS)
async def active_count(_, message: Message):
    voice_count = len(await get_active_chats())
    video_count = len(await get_active_video_chats())

    await message.reply_text(
        f"✯ <b><u>🔥 ᴀᴄᴛɪᴠᴇ ᴄʜᴀᴛs ɪɴғᴏ 🔥</u></b>\n\n"
        f"🔊 ᴠᴏɪᴄᴇ : <code>{voice_count}</code>\n"
        f"🎥 ᴠɪᴅᴇᴏ  : <code>{video_count}</code>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✯ ᴄʟᴏsᴇ ✯", callback_data="close")]]
        ),
    )


# ==============================
# ❌ CLOSE BUTTON
# ==============================

@app.on_callback_query(filters.regex("^close$"))
async def close_handler(_, query: CallbackQuery):
    await query.message.delete()
