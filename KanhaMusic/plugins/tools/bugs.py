from datetime import datetime
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery
)
from config import OWNER_ID
from KanhaMusic import app

SUPPORT_CHAT_ID = -1002274422022  # Change if needed


# ============================= #
# ✨ Extract Command Content
# ============================= #

def extract_bug_text(msg: Message):
    if not msg.text:
        return None
    parts = msg.text.split(None, 1)
    return parts[1] if len(parts) > 1 else None


# ============================= #
# 🐞 Bug Command
# ============================= #

@app.on_message(filters.command("bug"))
async def bug_report_handler(_, msg: Message):

    if msg.chat.type == "private":
        return await msg.reply_text(
            "❌ 𝐓ʜɪs 𝐂ᴏᴍᴍᴀɴᴅ 𝐈s 𝐎ɴʟʏ 𝐅ᴏʀ 𝐆ʀᴏᴜᴘs."
        )

    bug_text = extract_bug_text(msg)
    user = msg.from_user
    user_id = user.id
    mention = user.mention

    if user_id == OWNER_ID:
        return await msg.reply_text(
            "🤣 𝐀ʀᴇ 𝐘ᴏᴜ 𝐒ᴇʀɪᴏᴜs? 𝐘ᴏᴜ 𝐀ʀᴇ 𝐓ʜᴇ 𝐎ᴡɴᴇʀ!"
        )

    if not bug_text:
        return await msg.reply_text(
            "⚠️ 𝐍ᴏ 𝐁ᴜɢ 𝐌ᴇssᴀɢᴇ 𝐅ᴏᴜɴᴅ.\n\n"
            "👉 𝐔sᴇ: `/bug Your problem here`"
        )

    # Chat Info
    chat_info = (
        f"@{msg.chat.username} / `{msg.chat.id}`"
        if msg.chat.username
        else f"𝐏ʀɪᴠᴀᴛᴇ 𝐆ʀᴏᴜᴘ / `{msg.chat.id}`"
    )

    # Date
    date_now = datetime.utcnow().strftime("%d-%m-%Y")

    # Owner Info
    owner = await app.get_users(OWNER_ID)
    owner_mention = owner.mention

    # Bug Report Format
    bug_report_text = f"""
🐞 **#𝐍ᴇᴡ_𝐁ᴜɢ_𝐑ᴇᴘᴏʀᴛ**

👑 𝐇ᴇʟʟᴏ {owner_mention}

👤 **𝐑ᴇᴘᴏʀᴛᴇᴅ 𝐁ʏ:** {mention}
🆔 **𝐔sᴇʀ 𝐈𝐃:** `{user_id}`
💬 **𝐂ʜᴀᴛ:** {chat_info}

📝 **𝐁ᴜɢ:** `{bug_text}`

📅 **𝐃ᴀᴛᴇ:** {date_now}
"""

    # Confirmation to User
    await msg.reply_text(
        f"✅ **𝐁ᴜɢ 𝐑ᴇᴘᴏʀᴛᴇᴅ 𝐒ᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
        f"📝 `{bug_text}`",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("❌ 𝐂ʟᴏsᴇ", callback_data="close_user_msg")]]
        ),
    )

    # Send to Support Chat
    await app.send_photo(
        SUPPORT_CHAT_ID,
        photo="https://files.catbox.moe/1b1wap.jpg",
        caption=bug_report_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔎 𝐕ɪᴇᴡ 𝐁ᴜɢ", url=msg.link),
                    InlineKeyboardButton("❌ 𝐂ʟᴏsᴇ", callback_data="close_support_msg"),
                ]
            ]
        ),
    )


# ============================= #
# ❌ Close Buttons
# ============================= #

@app.on_callback_query(filters.regex("close_user_msg"))
async def close_user_message(_, query: CallbackQuery):
    await query.message.delete()


@app.on_callback_query(filters.regex("close_support_msg"))
async def close_support_message(_, query: CallbackQuery):
    member = await app.get_chat_member(
        query.message.chat.id, query.from_user.id
    )

    if member.privileges and member.privileges.can_delete_messages:
        await query.message.delete()
    else:
        await query.answer(
            "🚫 𝐘ᴏᴜ 𝐃ᴏɴ'ᴛ 𝐇ᴀᴠᴇ 𝐏ᴇʀᴍɪssɪᴏɴ!",
            show_alert=True
        )
