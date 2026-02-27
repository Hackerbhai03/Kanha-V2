import asyncio
from KanhaMusic.misc import SUDOERS
from KanhaMusic import app
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from KanhaMusic.utils.Kanha_BAN import admin_filter
from KanhaMusic.utils.database import get_assistant

# Active join tracking
active_joins = {}


@app.on_message(
    filters.group
    & filters.command(["userbotjoin", f"userbotjoin@{app.username}"])
    & ~filters.private
)
async def join_group(client, message):
    chat_id = message.chat.id
    userbot = await get_assistant(chat_id)
    done_msg = await message.reply("⏳ <b>ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ, ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ...</b>")
    await asyncio.sleep(1)

    bot_member = await app.get_chat_member(chat_id, app.id)

    userbot_member = None
    try:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
    except:
        pass

    # 1️⃣ Public group, bot not admin
    if message.chat.username and bot_member.status != ChatMemberStatus.ADMINISTRATOR:
        try:
            await userbot.join_chat(message.chat.username)
            await done_msg.edit_text("✅ <b>ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!</b>")
        except:
            await done_msg.edit_text("⚠ <b>ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ!</b>")
        return

    # 2️⃣ Public group, bot is admin
    if message.chat.username and bot_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            await userbot.join_chat(message.chat.username)
            await done_msg.edit_text("✅ <b>ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!</b>")
        except Exception as e:
            await done_msg.edit_text(f"⚠ <b>ᴇʀʀᴏʀ: {e}</b>")
        return

    # 3️⃣ Private group, bot admin, userbot banned
    if not message.chat.username and bot_member.status == ChatMemberStatus.ADMINISTRATOR:
        if userbot_member and userbot_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await done_msg.edit_text("🔓 <b>ᴀssɪsᴛᴀɴᴛ ɪs ᴜɴʙᴀɴɴᴇᴅ...</b>")
                invite_link = await app.create_chat_invite_link(chat_id)
                await asyncio.sleep(1)
                await userbot.join_chat(invite_link.invite_link)
                await done_msg.edit_text("✅ <b>ᴀssɪsᴛᴀɴᴛ ɴᴏᴡ ᴊᴏɪɴᴇᴅ ᴄʜᴀᴛ!</b>")
            except:
                await done_msg.edit_text("⚠ <b>ᴄᴀɴ'ᴛ ᴊᴏɪɴ. ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ʙᴀɴ ᴘᴏᴡᴇʀ ᴛᴏ ᴜɴʙᴀɴ ᴀssɪsᴛᴀɴᴛ ᴍᴀɴᴜᴀʟʟʏ.</b>")
        return

    # 4️⃣ Private group, bot not admin
    if not message.chat.username and bot_member.status != ChatMemberStatus.ADMINISTRATOR:
        await done_msg.edit_text("⚠ <b>ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ!</b>")
        return

    # 5️⃣ Private group, bot admin, userbot not banned
    if not message.chat.username and bot_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            invite_link = await app.create_chat_invite_link(chat_id)
            await asyncio.sleep(1)
            await userbot.join_chat(invite_link.invite_link)
            await done_msg.edit_text("✅ <b>ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!</b>")
        except Exception as e:
            await done_msg.edit_text(f"⚠ <b>ᴇʀʀᴏʀ: {e}</b>")


@app.on_message(filters.command("userbotleave") & filters.group & admin_filter)
async def leave_group(client, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await app.send_message(message.chat.id, "✅ <b>ᴜsᴇʀʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ ᴛʜɪs ᴄʜᴀᴛ.</b>")
    except Exception as e:
        await app.send_message(message.chat.id, f"⚠ <b>ᴇʀʀᴏʀ: {e}</b>")


@app.on_message(filters.command(["leaveall", f"leaveall@{app.username}"]) & SUDOERS)
async def leave_all_chats(client, message):
    left, failed = 0, 0
    await message.reply("🔄 <b>ᴜsᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ ᴀʟʟ ᴄʜᴀᴛs...</b>")
    userbot = await get_assistant(message.chat.id)

    async for dialog in userbot.get_dialogs():
        if dialog.chat.id == -1002141133985:  # Skip special group
            continue
        try:
            await userbot.leave_chat(dialog.chat.id)
            left += 1
        except:
            failed += 1
        await asyncio.sleep(2)
        await message.edit_text(
            f"🔄 <b>ᴜsᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ...</b>\n<b>✅ ʟᴇғᴛ:</b> {left}\n<b>❌ ғᴀɪʟᴇᴅ:</b> {failed}"
        )

    await app.send_message(
        message.chat.id,
        f"✅ <b>ʟᴇғᴛ ғʀᴏᴍ:</b> {left} chats.\n❌ <b>ғᴀɪʟᴇᴅ ɪɴ:</b> {failed} chats."
    )
