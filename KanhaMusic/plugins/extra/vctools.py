from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType, ChatMemberStatus
from KanhaMusic import app
from config import OWNER_ID
from strings import get_string
from KanhaMusic.utils import KanhaBin
from KanhaMusic.utils.database import get_assistant
from KanhaMusic.core.call import Kanha

# ─── 𝐀𝐝𝐦𝐢𝐧 𝐂𝐡𝐞𝐜𝐤𝐞𝐫 ─── #
async def is_admin(_, __, message):
    try:
        member = await message.chat.get_member(message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except:
        return False


# ─── 𝐕𝐂 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 ─── #
@app.on_message(filters.video_chat_started)
async def vc_started(_, msg: Message):
    text = "🫣 **𝐕𝐈𝐃𝐄𝐎 𝐂𝐇𝐀𝐓 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 😆**"
    add_link = f"https://t.me/{app.username}?startgroup=true"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="๏ 𝐉𝐎𝐈𝐍 𝐕𝐂 ๏", url=add_link)]]
    )
    await msg.reply(text, reply_markup=reply_markup)


# ─── 𝐕𝐂 𝐄𝐍𝐃𝐄𝐃 ─── #
@app.on_message(filters.video_chat_ended)
async def vc_ended(_, msg: Message):
    text = "😤 **𝐕𝐈𝐃𝐄𝐎 𝐂𝐇𝐀𝐓 𝐄𝐍𝐃𝐄𝐃 🙁**"
    add_link = f"https://t.me/{app.username}?startgroup=true"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="๏ 𝐀𝐃𝐃 𝐌𝐄 𝐁𝐀𝐁𝐘 ๏", url=add_link)]]
    )
    await msg.reply(text, reply_markup=reply_markup)


# ─── 𝐕𝐂 𝐌𝐄𝐌𝐁𝐄𝐑𝐒 𝐈𝐍𝐕𝐈𝐓𝐄𝐃 ─── #
@app.on_message(filters.video_chat_members_invited)
async def vc_invited(_, msg: Message):
    text = f"➠ {msg.from_user.mention}\n\n**๏ 𝐈𝐍𝐕𝐈𝐓𝐈𝐍𝐆 𝐓𝐎 𝐕𝐂 ๏**\n\n"
    for user in msg.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
        except:
            continue

    add_link = f"https://t.me/{app.username}?startgroup=true"
    await msg.reply(
        text + " 🤭🤭",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="๏ 𝐉𝐎𝐈𝐍 𝐕𝐂 ๏", url=add_link)]]
        ),
    )


# ─── 𝐋𝐈𝐒𝐓 𝐕𝐂 𝐌𝐄𝐌𝐁𝐄𝐑𝐒 ─── #
@app.on_message(
    filters.command(
        ["vcuser", "vcusers", "vcmember", "vcmembers", "cu", "cm"],
        prefixes=["/", "!", ".", "V", "v"]
    ) & filters.create(is_admin)
)
async def vc_members(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")

    msg = await message.reply("⏳ **𝐋𝐨𝐚𝐝𝐢𝐧𝐠 𝐕𝐂 𝐌𝐞𝐦𝐛𝐞𝐫𝐬...**")
    userbot = await get_assistant(message.chat.id)
    TEXT = ""

    try:
        async for m in userbot.get_call_members(message.chat.id):
            chat_id = m.chat.id
            username = m.chat.username
            is_video_enabled = m.is_video_enabled
            is_screen_sharing_enabled = m.is_screen_sharing_enabled
            is_hand_raised = m.is_hand_raised
            is_muted = bool(m.is_muted and not m.can_self_unmute)
            is_speaking = not m.is_muted
            is_left = m.is_left

            if m.chat.type != ChatType.PRIVATE:
                title = m.chat.title
            else:
                try:
                    title = (await client.get_users(chat_id)).mention
                except:
                    title = m.chat.first_name

            TEXT += _["V_C_2"].format(
                title,
                chat_id,
                username,
                is_video_enabled,
                is_screen_sharing_enabled,
                is_hand_raised,
                is_muted,
                is_speaking,
                is_left,
            )
            TEXT += "\n\n"

        if len(TEXT) < 4000:
            await msg.edit(TEXT or _["V_C_3"])
        else:
            link = await KanhaBin(TEXT)
            await msg.edit(
                _["V_C_4"].format(link),
                disable_web_page_preview=True
            )

    except ValueError:
        await msg.edit(_["V_C_5"])
