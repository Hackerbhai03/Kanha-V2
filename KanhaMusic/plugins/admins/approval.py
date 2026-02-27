import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from KanhaMusic import app

# Track active join requests to avoid duplicate buttons
active_requests = {}


@app.on_chat_join_request()
async def handle_join_request(client, join_req):
    chat = join_req.chat
    user = join_req.from_user
    key = f"{chat.id}_{user.id}"

    if key in active_requests:
        return
    active_requests[key] = True

    # Stylish formatted message
    message_text = (
        "**🚨 ᴀ ɴᴇᴡ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ!**\n\n"
        f"**👤 ᴜsᴇʀ:** {user.mention}\n"
        f"**🆔 ɪᴅ:** `{user.id}`\n"
        f"**🔗 ᴜsᴇʀɴᴀᴍᴇ:** @{user.username if user.username else 'ɴᴏɴᴇ'}\n\n"
        "<i>📝 ɴᴏᴛᴇ: ᴍᴇssᴀɢᴇ ᴡɪʟʟ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ɪɴ 10 ᴍɪɴᴜᴛᴇs</i>"
    )

    # Inline approve/dismiss buttons
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ ᴀᴘᴘʀᴏᴠᴇ", callback_data=f"approve:{chat.id}:{user.id}"),
                InlineKeyboardButton("❌ ᴅɪsᴍɪss", callback_data=f"dismiss:{chat.id}:{user.id}")
            ]
        ]
    )

    sent_message = await client.send_message(chat.id, message_text, reply_markup=buttons)

    # Auto-delete after 10 minutes
    async def auto_delete():
        await asyncio.sleep(600)
        try:
            await client.delete_messages(chat.id, sent_message.id)
        except:
            pass
        active_requests.pop(key, None)

    asyncio.create_task(auto_delete())


@app.on_callback_query(filters.regex("^(approve|dismiss):"))
async def handle_callback(client: Client, query: CallbackQuery):
    action, chat_id, user_id = query.data.split(":")
    chat_id, user_id = int(chat_id), int(user_id)
    key = f"{chat_id}_{user_id}"

    # Only allow admins to approve/dismiss
    try:
        member = await client.get_chat_member(chat_id, query.from_user.id)
        if member.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            return await query.answer("⚠️ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ 😎", show_alert=True)
    except:
        return await query.answer("⚠️ ᴀᴅᴍɪɴ ᴄʜᴇᴄᴋ ғᴀɪʟᴇᴅ", show_alert=True)

    try:
        user_obj = await client.get_users(user_id)
        chat_obj = await client.get_chat(chat_id)

        if action == "approve":
            await client.approve_chat_join_request(chat_id, user_id)
            await query.edit_message_text(
                f"**🎉 ʜᴇʏ {user_obj.mention}! ʏᴏᴜ ᴀʀᴇ ɴᴏᴡ ᴀᴘᴘʀᴏᴠᴇᴅ ɪɴ:** `{chat_obj.title}` ✅"
            )
        else:
            await client.decline_chat_join_request(chat_id, user_id)
            await query.edit_message_text(
                f"**❌ {user_obj.mention}, ʏᴏᴜʀ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴅɪsᴍɪssᴇᴅ ɪɴ:** `{chat_obj.title}`"
            )

    except Exception as e:
        msg = str(e)
        if "already handled" in msg.lower():
            await query.edit_message_text("⚠️ ʀᴇǫᴜᴇsᴛ ᴀʟʀᴇᴀᴅʏ ʜᴀɴᴅʟᴇᴅ")
        else:
            await query.answer(f"⚠️ ᴇʀʀᴏʀ: {msg}", show_alert=True)

    active_requests.pop(key, None)
