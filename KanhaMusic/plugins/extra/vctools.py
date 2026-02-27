from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.enums import ChatType, ChatMemberStatus

from KanhaMusic import app
from strings import get_string
from KanhaMusic.utils.database import get_assistant, get_lang
from KanhaMusic.utils import KanhaBin


# ─────────────────────────────────────────────
# ✦ ADMIN CHECK SYSTEM ✦
# ─────────────────────────────────────────────

async def is_admin(_, __, message: Message):
    try:
        member = await message.chat.get_member(message.from_user.id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )
    except Exception:
        return False


# ─────────────────────────────────────────────
# 🎙️ VIDEO CHAT STARTED
# ─────────────────────────────────────────────

@app.on_message(filters.video_chat_started)
async def vc_started(_, msg: Message):
    add_link = f"https://t.me/{app.username}?startgroup=true"

    await msg.reply(
        "**✨ 𝑽𝑶𝑰𝑪𝑬 𝑪𝑯𝑨𝑻 𝑯𝑨𝑺 𝑺𝑻𝑨𝑹𝑻𝑬𝑫 ✨**\n\n"
        "➥ 𝐋𝐞𝐭’𝐬 𝐑𝐨𝐜𝐤 𝐓𝐡𝐞 𝐕𝐂 🎧🔥",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="💎 𝐉𝐎𝐈𝐍 𝐕𝐂 💎",
                        url=add_link
                    )
                ]
            ]
        ),
    )


# ─────────────────────────────────────────────
# 🛑 VIDEO CHAT ENDED
# ─────────────────────────────────────────────

@app.on_message(filters.video_chat_ended)
async def vc_ended(_, msg: Message):
    add_link = f"https://t.me/{app.username}?startgroup=true"

    await msg.reply(
        "**⚡ 𝑽𝑶𝑰𝑪𝑬 𝑪𝑯𝑨𝑻 𝑬𝑵𝑫𝑬𝑫 ⚡**\n\n"
        "➥ 𝐒𝐞𝐞 𝐘𝐨𝐮 𝐀𝐠𝐚𝐢𝐧 𝐂𝐡𝐚𝐦𝐩 😎",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🚀 𝐀𝐃𝐃 𝐌𝐄 𝐀𝐆𝐀𝐈𝐍 🚀",
                        url=add_link
                    )
                ]
            ]
        ),
    )


# ─────────────────────────────────────────────
# 👥 MEMBERS INVITED IN VC
# ─────────────────────────────────────────────

@app.on_message(filters.video_chat_members_invited)
async def vc_invited(client, message: Message):
    text = (
        f"👑 {message.from_user.mention}\n\n"
        "✨ 𝐈𝐍𝐕𝐈𝐓𝐄𝐃 𝐈𝐍 𝐕𝐎𝐈𝐂𝐄 𝐂𝐇𝐀𝐓 ✨\n\n"
    )

    for user in message.video_chat_members_invited.users:
        try:
            text += f"➥ [{user.first_name}](tg://user?id={user.id})\n"
        except Exception:
            continue

    add_link = f"https://t.me/{app.username}?startgroup=true"

    await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🎧 𝐉𝐎𝐈𝐍 𝐍𝐎𝐖 🎧",
                        url=add_link
                    )
                ]
            ]
        ),
    )


# ─────────────────────────────────────────────
# 📊 VC MEMBERS LIST COMMAND
# ─────────────────────────────────────────────

@app.on_message(
    filters.command(
        ["vcuser", "vcusers", "vcmember", "vcmembers", "cu", "cm"],
        prefixes=["/", "!", ".", "v", "V"]
    ) & filters.create(is_admin)
)
async def vc_members(client, message: Message):

    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except Exception:
        _ = get_string("en")

    msg = await message.reply_text("⏳ 𝐅𝐞𝐭𝐜𝐡𝐢𝐧𝐠 𝐕𝐂 𝐌𝐞𝐦𝐛𝐞𝐫𝐬...")

    assistant = await get_assistant(message.chat.id)
    TEXT = "🎙️ **𝐕𝐂 𝐌𝐄𝐌𝐁𝐄𝐑 𝐋𝐈𝐒𝐓** 🎙️\n\n"

    try:
        async for member in assistant.get_call_members(message.chat.id):

            chat_id = member.chat.id
            username = member.chat.username or "N/A"
            is_video = member.is_video_enabled
            is_screen = member.is_screen_sharing_enabled
            is_hand = member.is_hand_raised
            is_left = member.is_left
            is_muted = bool(member.is_muted and not member.can_self_unmute)
            is_speaking = not member.is_muted

            if member.chat.type != ChatType.PRIVATE:
                title = member.chat.title
            else:
                try:
                    user = await client.get_users(chat_id)
                    title = user.mention
                except Exception:
                    title = member.chat.first_name

            TEXT += (
                f"👤 𝐍𝐚𝐦𝐞: {title}\n"
                f"🆔 𝐈𝐃: `{chat_id}`\n"
                f"🔊 𝐒𝐩𝐞𝐚𝐤𝐢𝐧𝐠: `{is_speaking}`\n"
                f"🔇 𝐌𝐮𝐭𝐞𝐝: `{is_muted}`\n"
                f"🎥 𝐕𝐢𝐝𝐞𝐨: `{is_video}`\n"
                f"🖥️ 𝐒𝐜𝐫𝐞𝐞𝐧: `{is_screen}`\n"
                f"✋ 𝐇𝐚𝐧𝐝 𝐑𝐚𝐢𝐬𝐞𝐝: `{is_hand}`\n"
                f"🚪 𝐋𝐞𝐟𝐭: `{is_left}`\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
            )

        if len(TEXT) < 4000:
            await msg.edit(TEXT)
        else:
            link = await KanhaBin(TEXT)
            await msg.edit(
                f"📜 𝐋𝐢𝐬𝐭 𝐓𝐨𝐨 𝐋𝐨𝐧𝐠...\n\n🔗 {link}",
                disable_web_page_preview=True
            )

    except ValueError:
        await msg.edit("❌ 𝐍𝐨 𝐀𝐜𝐭𝐢𝐯𝐞 𝐕𝐂 𝐅𝐨𝐮𝐧𝐝")
    except Exception as e:
        await msg.edit(f"⚠️ 𝐄𝐫𝐫𝐨𝐫: {e}")
