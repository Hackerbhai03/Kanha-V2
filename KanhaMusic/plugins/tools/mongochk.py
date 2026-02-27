from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
import re
from KanhaMusic import app as Kanha

# ✦ Mongo URL Pattern
MONGO_URL_PATTERN = re.compile(r"^mongodb(\+srv)?:\/\/[^\s]+$")


@Sona.on_message(filters.command("mongochk"))
async def mongo_command(client, message: Message):

    ADD_ME_BUTTON = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "✧ ᴀᴅᴅ ϻє ᴛᴏ ʏσυʀ ɢʀσυᴘ ✧",
                url=f"https://t.me/{Kanha.username}?startgroup=true"
            )
        ]]
    )

    # ❌ No URL
    if len(message.command) < 2:
        return await message.reply_text(
            "╭━━━〔 💾 ᴍᴏɴɢᴏ ᴄʜᴇᴄᴋᴇʀ 💾 〕━━━╮\n"
            "┃ ✘ ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴍᴏɴɢᴏ ᴜʀʟ\n"
            "┃ \n"
            "┃ ✎ ᴇxᴀᴍᴘʟᴇ :\n"
            "┃ `/mongochk mongodb+srv://user:pass@cluster.mongodb.net/`\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=ADD_ME_BUTTON
        )

    mongo_url = message.command[1].strip()

    # ❌ Invalid Format
    if not re.match(MONGO_URL_PATTERN, mongo_url):
        return await message.reply_text(
            "╭━━━〔 ⚠ ᴇʀʀᴏʀ ⚠ 〕━━━╮\n"
            "┃ 💔 ɪɴᴠᴀʟɪᴅ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ꜰᴏʀᴍᴀᴛ\n"
            "┃ \n"
            "┃ ✔ ꜱᴛᴀʀᴛ ᴡɪᴛʜ : mongodb://\n"
            "┃ ✔ ᴏʀ : mongodb+srv://\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=ADD_ME_BUTTON
        )

    checking_msg = await message.reply_text(
        "╭━━━〔 🔄 ᴘʀᴏᴄᴇssɪɴɢ 🔄 〕━━━╮\n"
        "┃ ⏳ ᴄʜᴇᴄᴋɪɴɢ ᴍᴏɴɢᴏᴅʙ ᴄᴏɴɴᴇᴄᴛɪᴏɴ...\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯"
    )

    try:
        mongo_client = MongoClient(
            mongo_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )

        mongo_client.server_info()

        await checking_msg.edit_text(
            "╭━━━〔 ✅ sᴜᴄᴄᴇss ✅ 〕━━━╮\n"
            "┃ 🎉 ᴍᴏɴɢᴏᴅʙ ᴄᴏɴɴᴇᴄᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ\n"
            "┃ \n"
            f"┃ ✦ ᴄʜᴇᴄᴋᴇᴅ ʙʏ : {Sona.mention}\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=ADD_ME_BUTTON
        )

    except ServerSelectionTimeoutError:
        await checking_msg.edit_text(
            "╭━━━〔 ⏰ ᴛɪᴍᴇᴏᴜᴛ ⏰ 〕━━━╮\n"
            "┃ ❌ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛɪᴍᴇᴅ ᴏᴜᴛ\n"
            "┃ 🌐 ᴄʜᴇᴄᴋ ɴᴇᴛᴡᴏʀᴋ / ᴄʟᴜsᴛᴇʀ\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=ADD_ME_BUTTON
        )

    except ConfigurationError:
        await checking_msg.edit_text(
            "╭━━━〔 ⚙ ᴄᴏɴғɪɢ ᴇʀʀᴏʀ ⚙ 〕━━━╮\n"
            "┃ ❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ / ᴘᴀssᴡᴏʀᴅ\n"
            "┃ 🔐 ᴄʜᴇᴄᴋ ᴄʟᴜsᴛᴇʀ sᴇᴛᴛɪɴɢs\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=ADD_ME_BUTTON
        )

    except Exception as e:
        await checking_msg.edit_text(
            "╭━━━〔 💥 ғᴀɪʟᴇᴅ 💥 〕━━━╮\n"
            f"┃ ❌ {str(e)}\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=ADD_ME_BUTTON
        )
