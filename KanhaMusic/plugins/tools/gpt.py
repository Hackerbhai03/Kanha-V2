import aiohttp
import urllib.parse
from pyrogram import filters
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from KanhaMusic import app

API_URL = "https://chatgpt.apinepdev.workers.dev/?question="

@app.on_message(filters.command(
    ["chatgpt", "ai", "ask", "gpt", "solve"],
    prefixes=["/", ".", "!", "$", "#", "&"]
))
async def ultra_ai(bot, message):

    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            return await message.reply_text(
                "✨ **𝗘𝘅𝗮𝗺𝗽𝗹𝗲 :**\n\n`/ai Who built Taj Mahal?`",
                parse_mode=ParseMode.MARKDOWN
            )

        question = message.text.split(" ", 1)[1]
        encoded_question = urllib.parse.quote(question)

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}{encoded_question}", timeout=20) as response:

                if response.status != 200:
                    return await message.reply_text(
                        f"⚠️ **𝗔𝗣𝗜 𝗘𝗿𝗿𝗼𝗿 :** `{response.status}`",
                        parse_mode=ParseMode.MARKDOWN
                    )

                data = await response.json()

        if "answer" not in data:
            return await message.reply_text("⚠️ 𝗡𝗼 𝗩𝗮𝗹𝗶𝗱 𝗔𝗻𝘀𝘄𝗲𝗿 𝗙𝗼𝘂𝗻𝗱.")

        answer = data["answer"]

        # Remove unwanted promo text
        unwanted = ["Join", "t.me/", "Telegram"]
        for word in unwanted:
            if word.lower() in answer.lower():
                answer = answer.split(word)[0].strip()

        # Telegram limit protection
        if len(answer) > 4000:
            answer = answer[:4000] + "\n\n⚠️ 𝗔𝗻𝘀𝘄𝗲𝗿 𝗧𝗿𝘂𝗻𝗰𝗮𝘁𝗲𝗱..."

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🚀 𝗔𝗗𝗗 𝗠𝗘 𝗜𝗡 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣 🚀",
                    url=f"https://t.me/{app.username}?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔥 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 𝗨𝗟𝗧𝗥𝗔 𝗔𝗜 🔥",
                    url="https://t.me"
                )
            ]
        ])

        await message.reply_text(
            f"""
╔═══〔 🤖 𝗨𝗟𝗧𝗥𝗔 𝗔𝗜 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 〕═══╗

💬 **𝗤𝘂𝗲𝘀𝘁𝗶𝗼𝗻 :**
`{question}`

🧠 **𝗔𝗻𝘀𝘄𝗲𝗿 :**
{answer}

╚═══════════════════════╝
""",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=buttons,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply_text(
            f"⚠️ **𝗘𝗿𝗿𝗼𝗿 :** `{str(e)}`",
            parse_mode=ParseMode.MARKDOWN
        )
