import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from KanhaMusic import app
from KanhaMusic.misc import SUDOERS


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚪 LEAVE GROUP COMMAND
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("leave") & SUDOERS)
async def leave_group_handler(client: Client, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "❖ ᴜsᴀɢᴇ:\n"
            "➤ `/leave -100xxxxxxxxxx`",
            quote=True
        )

    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("❖ ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ❌")

    status = await message.reply_text(
        f"❖ ʟᴇᴀᴠɪɴɢ ɢʀᴏᴜᴘ...\n"
        f"➤ {client.me.mention}"
    )

    try:
        await client.send_message(chat_id, "❖ ʙᴏᴛ ɪs ʟᴇᴀᴠɪɴɢ ᴛʜɪs ɢʀᴏᴜᴘ 👋")
        await client.leave_chat(chat_id)

        await status.edit(
            f"❖ ʟᴇғᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ✅\n"
            f"➤ `{chat_id}`"
        )

    except Exception as e:
        await status.edit(f"❖ ғᴀɪʟᴇᴅ ❌\n`{str(e)}`")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔗 CURRENT CHAT INVITE LINK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("givelink"))
async def give_current_link(client: Client, message: Message):

    try:
        link = await client.export_chat_invite_link(message.chat.id)

        await message.reply_text(
            "❖ ɪɴᴠɪᴛᴇ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ 🔗\n\n"
            f"{link}"
        )

    except FloodWait as fw:
        await asyncio.sleep(fw.value)
        await message.reply_text("❖ ᴛʀʏ ᴀɢᴀɪɴ ⚠️")

    except Exception as e:
        await message.reply_text(f"❖ ᴇʀʀᴏʀ ❌\n`{str(e)}`")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📜 GROUP INFO + INVITE LINK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(
    filters.command(["link", "invitelink"], prefixes=["/", "!", ".", "#"]) & SUDOERS
)
async def group_info_handler(client: Client, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "❖ ᴜsᴀɢᴇ:\n"
            "➤ `/link -100xxxxxxxxxx`"
        )

    group_id = message.command[1]
    file_name = f"group_info_{group_id}.txt"

    try:
        chat = await client.get_chat(int(group_id))

        try:
            invite_link = await client.export_chat_invite_link(chat.id)
        except FloodWait as fw:
            await message.reply_text(
                f"❖ ғʟᴏᴏᴅᴡᴀɪᴛ ⚠️\n"
                f"➤ ᴡᴀɪᴛ {fw.value} sᴇᴄ"
            )
            return

        group_info_text = f"""
❖ ɢʀᴏᴜᴘ ᴅᴇᴛᴀɪʟs

➤ ɪᴅ: {chat.id}
➤ ᴛɪᴛʟᴇ: {chat.title}
➤ ᴛʏᴘᴇ: {chat.type}
➤ ᴍᴇᴍʙᴇʀs: {chat.members_count}
➤ ᴠᴇʀɪғɪᴇᴅ: {chat.is_verified}
➤ sᴄᴀᴍ: {chat.is_scam}
➤ ғᴀᴋᴇ: {chat.is_fake}
➤ ᴘʀᴏᴛᴇᴄᴛᴇᴅ: {chat.has_protected_content}

❖ ɪɴᴠɪᴛᴇ ʟɪɴᴋ:
{invite_link}
"""

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(group_info_text.strip())

        await client.send_document(
            chat_id=message.chat.id,
            document=file_name,
            caption=(
                f"❖ ɢʀᴏᴜᴘ ɪɴғᴏ ᴇxᴘᴏʀᴛᴇᴅ 📄\n"
                f"➤ {chat.title}\n"
                f"➤ ʙʏ @{client.me.username}"
            )
        )

    except Exception as e:
        await message.reply_text(f"❖ ᴇʀʀᴏʀ ❌\n`{str(e)}`")

    finally:
        if os.path.exists(file_name):
            os.remove(file_name)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📚 MODULE INFO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

__MODULE__ = "❖ Gʀᴏᴜᴘ Lɪɴᴋs"

__HELP__ = """
❖ /givelink
   ➤ ᴄᴜʀʀᴇɴᴛ ᴄʜᴀᴛ ɪɴᴠɪᴛᴇ ʟɪɴᴋ

❖ /link -100xxxx
   ➤ ғᴜʟʟ ɢʀᴏᴜᴘ ɪɴғᴏ + ɪɴᴠɪᴛᴇ ʟɪɴᴋ

❖ /leave -100xxxx
   ➤ ʟᴇᴀᴠᴇ sᴘᴇᴄɪғɪᴇᴅ ɢʀᴏᴜᴘ
"""
