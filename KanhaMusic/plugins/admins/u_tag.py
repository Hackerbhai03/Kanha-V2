import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import Message

from KanhaMusic import app

spam_chats = set()

@app.on_message(filters.command(["utag", "all", "mention"], prefixes=["/", "@"]))
async def tag_all_users(client: Client, message: Message):

    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("⬤ **ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.**")


    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply("⬤ **ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ.**")


    try:
        await message.delete()
    except Exception:
        pass

    replied = message.reply_to_message
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else ""

    if not replied and not text:
        return await message.reply("**» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ/ɢɪᴠᴇ ᴛᴇxᴛ ᴛᴏ ᴛᴀɢ ᴀʟʟ ʟɪᴋᴇ »** `/all Hi Friends`")

    spam_chats.add(message.chat.id)
    usernum, usertxt, total_tagged = 0, "", 0


    try:
        async for member in client.get_chat_members(message.chat.id):
            if message.chat.id not in spam_chats:
                break

            if not member.user or member.user.is_bot:
                continue

            usernum += 1
            total_tagged += 1
            usertxt += f"⊚ [{member.user.first_name}](tg://user?id={member.user.id})\n"

            if usernum == 5:
                try:
                    if replied:
                        await replied.reply_text(
                            f"{text}\n\n{usertxt}\n**🏆 ᴛᴏᴛᴀʟ** `{total_tagged}` **ᴜsᴇʀs ᴛᴀɢs ᴅᴏɴᴇ...**"
                        )
                    else:
                        await message.reply_text(
                            f"{text}\n\n{usertxt}\n**🏆 ᴛᴏᴛᴀʟ** `{total_tagged}` **ᴜsᴇʀs ᴛᴀɢs ᴅᴏɴᴇ...**"
                        )
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception:
                    pass

                await asyncio.sleep(3)
                usernum, usertxt = 0, ""

        if usertxt:
            try:
                if replied:
                    await replied.reply_text(
                        f"{text}\n\n{usertxt}\n**🏆 ᴛᴏᴛᴀʟ** `{total_tagged}` **ᴜsᴇʀs ᴛᴀɢs ᴅᴏɴᴇ...**"
                    )
                else:
                    await message.reply_text(
                        f"{text}\n\n{usertxt}\n**🏆 ᴛᴏᴛᴀʟ** `{total_tagged}` **ᴜsᴇʀs ᴛᴀɢs ᴅᴏɴᴇ...**"
                    )
            except Exception:
                pass

        await message.reply(f"✅ **ᴛᴀɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ. ᴛᴏᴛᴀʟ :-** `{total_tagged}` **ᴜsᴇʀs.**")

    finally:
        spam_chats.discard(message.chat.id)


@app.on_message(filters.command(["cancel", "ustop"], prefixes=["/", "@"]))
async def cancel_spam(client: Client, message: Message):
    # Private chat check
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("⬤ **ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.**")

    chat_id = message.chat.id

    if chat_id not in spam_chats:
        return await message.reply("**» ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ᴀɴʏᴏɴᴇ ʀɪɢʜᴛ ɴᴏᴡ.**")

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
            return await message.reply("⬤ **ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ.**")
    except UserNotParticipant:
        return await message.reply("**» ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ᴏғ ᴛʜɪs ᴄʜᴀᴛ.**")
    except Exception:
        return await message.reply("**» ᴇʀʀᴏʀ ᴄʜᴇᴄᴋɪɴɢ ᴀᴅᴍɪɴ sᴛᴀᴛᴜs.**")

    spam_chats.discard(chat_id)
    return await message.reply("**🚫 ᴛᴀɢɢɪɴɢ ᴄᴀɴᴄᴇʟʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**")
