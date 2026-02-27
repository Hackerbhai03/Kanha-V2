import requests
from pyrogram import filters
from pyrogram.types import Message
from KanhaMusic import app


# 🎮 Game Emoji Mapping
GAME_EMOJIS = {
    "dice": "🎲",
    "ludo": "🎲",
    "dart": "🎯",
    "basket": "🏀",
    "basketball": "🏀",
    "football": "⚽",
    "slot": "🎰",
    "jackpot": "🎰",
    "bowling": "🎳",
}


# ─────────────────────────────
# 🎲 FUN GAMES HANDLER
# ─────────────────────────────
@app.on_message(filters.command(list(GAME_EMOJIS.keys())))
async def fun_games(client, message: Message):
    cmd = message.command[0].lower()
    emoji = GAME_EMOJIS.get(cmd, "🎲")

    dice_msg = await client.send_dice(
        chat_id=message.chat.id,
        emoji=emoji,
        reply_to_message_id=message.id
    )

    score = dice_msg.dice.value

    await dice_msg.reply_text(
        f"""
╔═══━─━─━─━─━─━─━═══╗
      🎮 𝗙𝗨𝗡 𝗚𝗔𝗠𝗘 𝗥𝗘𝗦𝗨𝗟𝗧 🎮
╚═══━─━─━─━─━─━─━═══╝

🎯 𝗚𝗮𝗺𝗲   ➜  {cmd.upper()}
🏆 𝗦𝗰𝗼𝗿𝗲  ➜  {score}

✨ 𝗣𝗹𝗮𝘆 𝗔𝗴𝗮𝗶𝗻 & 𝗕𝗲𝗮𝘁 𝗬𝗼𝘂𝗿 𝗦𝗰𝗼𝗿𝗲!
"""
    )


# ─────────────────────────────
# 🌈 BORED COMMAND
# ─────────────────────────────
BORED_API = "https://apis.scrimba.com/bored/api/activity"


@app.on_message(filters.command("bored"))
async def bored(client, message: Message):
    try:
        res = requests.get(BORED_API, timeout=5)

        if res.status_code == 200:
            data = res.json()
            activity = data.get("activity")

            if activity:
                await message.reply_text(
                    f"""
╔═══━─━─━─━─━─━─━═══╗
      🌈 𝗕𝗢𝗥𝗘𝗗 𝗠𝗢𝗗𝗘 🌈
╚═══━─━─━─━─━─━─━═══╝

💡 𝗧𝗿𝘆 𝗧𝗵𝗶𝘀 𝗔𝗰𝘁𝗶𝘃𝗶𝘁𝘆:

➜  {activity}

🔥 𝗠𝗮𝗸𝗲 𝗬𝗼𝘂𝗿 𝗗𝗮𝘆 𝗔𝘄𝗲𝘀𝗼𝗺𝗲!
"""
                )
            else:
                await message.reply_text("⚠️ 𝗡𝗼 𝗮𝗰𝘁𝗶𝘃𝗶𝘁𝘆 𝗳𝗼𝘂𝗻𝗱.")
        else:
            await message.reply_text("❌ 𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝗳𝗲𝘁𝗰𝗵 𝗮𝗰𝘁𝗶𝘃𝗶𝘁𝘆.")

    except Exception:
        await message.reply_text("🚨 𝗦𝗼𝗺𝗲𝘁𝗵𝗶𝗻𝗴 𝗪𝗲𝗻𝘁 𝗪𝗿𝗼𝗻𝗴.")


# ─────────────────────────────
# 📚 MODULE INFO
# ─────────────────────────────
__MODULE__ = "🎉 𝗙𝗨𝗡 𝗭𝗢𝗡𝗘"

__HELP__ = """
╔═══━─━─━─━─━─━─━═══╗
        🎮 𝗙𝗨𝗡 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦
╚═══━─━─━─━─━─━─━═══╝

🎲 `/dice`        ➜ Roll Dice  
🎯 `/dart`        ➜ Throw Dart  
🏀 `/basket`      ➜ Play Basketball  
⚽ `/football`    ➜ Play Football  
🎰 `/slot`        ➜ Try Jackpot  
🎳 `/bowling`     ➜ Play Bowling  
🎲 `/ludo`        ➜ Play Ludo  
🌈 `/bored`       ➜ Random Activity  

━━━━━━━━━━━━━━━━━━━
🔥 𝗘𝗻𝗷𝗼𝘆 & 𝗞𝗲𝗲𝗽 𝗦𝗺𝗶𝗹𝗶𝗻𝗴!
"""
