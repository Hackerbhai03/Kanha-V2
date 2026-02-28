from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType, ChatMemberStatus
from KanhaMusic import app
from config import OWNER_ID
from strings import get_string
from KanhaMusic.utils import KanhaBin
from KanhaMusic.utils.database import get_assistant, get_lang
from KanhaMusic.core.call import Kanha

# ⚡ Check if user is admin
async def is_admin(_, __, message: Message):
    try:
        member = await message.chat.get_member(message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except:
        return False

# 🌟 VC STARTED
@app.on_message(filters.video_chat_started)
async def on_vc_start(_, msg: Message):
    text = "⏩ 𝗩𝗖 𝘀𝘁𝗮𝗿𝘁𝗲𝗱! 💥\n> 🎧 ᴊσɪη ᴠᴄ ʙʏ ᴄʟɪᴄᴋɪɴɢ ʜᴇʀᴇ!"
    add_link = f"https://t.me/{app.username}?startgroup=true"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="🎧 ᴊσɪη ᴠᴄ 🎶", url=add_link)]]
    )
    await msg.reply(text, reply_markup=reply_markup)

# 🔥 VC ENDED
@app.on_message(filters.video_chat_ended)
async def on_vc_end(_, msg: Message):
    text = "⏹️ 𝗩𝗖 𝗲𝗻𝗱𝗲𝗱 😢\n> ✨ ᴀᴅᴅ ᴍᴇ ʙᴀᴄᴋ ʙʏ ᴄʟɪᴄᴋɪɴɢ ʜᴇʀᴇ"
    add_link = f"https://t.me/{app.username}?startgroup=true"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="✨ ᴀᴅᴅ ᴍᴇ ʙᴀᴄᴋ 💫", url=add_link)]]
    )
    await msg.reply(text, reply_markup=reply_markup)

# 🫣 VC MEMBERS INVITED
@app.on_message(filters.video_chat_members_invited)
async def on_vc_invite(_, message: Message):
    text = f"> 👑 {message.from_user.mention} ɪɴᴠɪᴛᴇᴅ ᴍᴇᴍʙᴇʀs ᴛᴏ ᴠᴄ 🤩\n> "
    for user in message.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
        except Exception:
            continue

    try:
        add_link = f"https://t.me/{app.username}?startgroup=true"
        await message.reply(
            text + "\n> 🎶 ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴊᴏɪɴ 👇",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="🎧 ᴊσɪη ᴠᴄ 🎶", url=add_link)]]
            )
        )
    except Exception as e:
        print(f"Error sending VC invite message: {e}")

# 👥 VC MEMBERS LIST
@app.on_message(
    filters.command(
        ["vcuser", "vcusers", "vcmember", "vcmembers", "cu", "cm"],
        prefixes=["/", "!", ".", "V", "v"]
    ) & filters.create(is_admin)
)
async def vc_members(client: Client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")

    msg = await message.reply_text("> ⏳ ʟᴏᴀᴅɪɴɢ ᴠᴄ ᴍᴇᴍʙᴇʀs...")

    userbot = await get_assistant(message.chat.id)
    TEXT = ""

    try:
        async for m in userbot.get_call_members(message.chat.id):
            chat_id = m.chat.id
            username = m.chat.username or "❌ NoUsername"
            is_hand_raised = "✋" if m.is_hand_raised else "❌"
            is_video_enabled = "🎥" if m.is_video_enabled else "❌"
            is_left = "🚪" if m.is_left else "✅"
            is_screen_sharing_enabled = "🖥️" if m.is_screen_sharing_enabled else "❌"
            is_muted = "🔇" if (m.is_muted and not m.can_self_unmute) else "🔊"
            is_speaking = "🎤" if not m.is_muted else "❌"

            if m.chat.type != ChatType.PRIVATE:
                title = m.chat.title
            else:
                try:
                    title = (await client.get_users(chat_id)).mention
                except:
                    title = "Private"

            TEXT += f"> 💠 **{title}**\n"
            TEXT += f"> 🆔 `{chat_id}` | 🖋️ @{username}\n"
            TEXT += f"> {is_video_enabled} | {is_screen_sharing_enabled} | {is_hand_raised} | {is_muted} | {is_speaking} | {is_left}\n\n"

        if len(TEXT) < 4000:
            await msg.edit(TEXT or "> ❌ No members found in VC")
        else:
            link = await SonaBin(TEXT)
            await msg.edit(
                f"> 📜 ᴛᴏᴏ ᴍᴀɴʏ ᴍᴇᴍʙᴇʀs! ᴠɪᴇᴡ ʜᴇʀᴇ: {link}",
                disable_web_page_preview=True,
            )
    except ValueError:
        await msg.edit("> ❌ ᴇʀʀᴏʀ ʟᴏᴀᴅɪɴɢ ᴍᴇᴍʙᴇʀs")
