import requests
import random
from KanhaMusic import app, userbot
from KanhaMusic.misc import SUDOERS
from pyrogram import * 
from pyrogram.types import *
from KanhaMusic.utils.purvi_ban import admin_filter


kanha_text = [
"𝙾𝚢𝚎… 𝚍𝚒𝚜𝚝𝚞𝚛𝚋 𝚖𝚊𝚝 𝚔𝚊𝚛, 𝚖𝚊𝚒 𝚜𝚘 𝚛𝚊𝚑𝚊 𝚑𝚞. 😴", 
"𝚃𝚞 𝚔𝚘𝚗 𝚑𝚊𝚒 𝚋𝚎? 🤨", 
"𝙰𝚊𝚙 𝚔𝚘𝚗 𝚑𝚘 𝚋𝚑𝚊𝚒? 🤔", 
"𝙰𝚊𝚙 𝚖𝚎𝚛𝚎 𝚘𝚠𝚗𝚎𝚛 𝚗𝚊𝚑𝚒 𝚑𝚘, 𝚜𝚑𝚊𝚊𝚗𝚝 𝚛𝚊𝚑𝚘. 🚫", 
"𝙰𝚛𝚎 𝚖𝚎𝚛𝚊 𝚗𝚊𝚊𝚖 𝚔𝚢𝚞 𝚕𝚎 𝚛𝚊𝚑𝚊 𝚑𝚊𝚒? 𝚜𝚘𝚗𝚎 𝚍𝚎 𝚗𝚊 𝚋𝚜𝚍𝚔. 😪", 
"𝙷𝚊𝚊 𝚋𝚘𝚕, 𝚔𝚢𝚊 𝚌𝚑𝚊𝚑𝚒𝚢𝚎? 𝚓𝚊𝚕𝚍𝚒 𝚋𝚘𝚕. 👀", 
"𝙰𝚋𝚑𝚒 𝚖𝚊𝚒 𝚋𝚞𝚜𝚢 𝚑𝚞, 𝚍𝚒𝚖𝚊𝚊𝚐 𝚖𝚊𝚝 𝚔𝚑𝚊. ⏳", 
"𝙱𝚞𝚜𝚢 𝚑𝚞 𝚋𝚎, 𝚕𝚊𝚝𝚎𝚛 𝚊𝚊𝚗𝚊. 🚧", 
"𝚂𝚊𝚖𝚊𝚓𝚑 𝚗𝚊𝚑𝚒 𝚊𝚊𝚝𝚊 𝚔𝚢𝚊? 😑", 
"𝙻𝚎𝚊𝚟𝚎 𝚖𝚎 𝚊𝚕𝚘𝚗𝚎, 𝚟𝚊𝚛𝚗𝚊 𝚜𝚎𝚎𝚗 𝚙𝚎 𝚌𝚑𝚑𝚘𝚍 𝚍𝚞𝚗𝚐𝚊. 🖤", 
"𝙾𝚢𝚎 𝚋𝚛𝚘… 𝚔𝚢𝚊 𝚑𝚘 𝚐𝚊𝚢𝚊? 𝚌𝚑𝚒𝚕 𝚔𝚊𝚛. 😒", 
"dude what happend",    
]

strict_txt = [
"𝙸 𝚌𝚊𝚗’𝚝 𝚛𝚎𝚜𝚝𝚛𝚒𝚌𝚝 𝚖𝚢 𝚋𝚎𝚜𝚝𝚒𝚎𝚜 — 𝚜𝚊𝚖𝚓𝚑𝚊 𝚔𝚊𝚛. 🤝😤", 

"𝙰𝚛𝚎 𝚜𝚎𝚛𝚒𝚘𝚞𝚜𝚕𝚢? 𝚖𝚊𝚒 𝚊𝚙𝚗𝚎 𝚍𝚘𝚜𝚝𝚘𝚗 𝚔𝚘 𝚛𝚎𝚜𝚝𝚛𝚒𝚌𝚝 𝚗𝚊𝚑𝚒 𝚔𝚊𝚛𝚝𝚊. 🚫", 

"𝙵𝚞𝚌𝚔 𝚘𝚏𝚏 𝚋𝚜𝚍𝚔 — 𝚖𝚊𝚒 𝚊𝚙𝚗𝚎 𝚍𝚘𝚜𝚝𝚘𝚗 𝚙𝚎 𝚑𝚊𝚊𝚝𝚑 𝚗𝚊𝚑𝚒 𝚍𝚊𝚊𝚕𝚝𝚊. 😈", 

"𝙷𝚎𝚢 𝚜𝚝𝚞𝚙𝚒𝚍 𝚊𝚍𝚖𝚒𝚗 — 𝚔𝚞𝚌𝚑 𝚊𝚞𝚛 𝚔𝚊𝚊𝚖 𝚍𝚑𝚞𝚗𝚍. 🙄", 

"𝙷𝚊𝚊 𝚢𝚎 𝚙𝚎𝚑𝚕𝚎 𝚔𝚊𝚛𝚕𝚘 — 𝚊𝚊𝚙𝚜 𝚖𝚎 𝚐𝚊𝚊𝚗𝚍 𝚖𝚊𝚊𝚛 𝚕𝚘. 🤡🔥", 

"𝙸 𝚌𝚊𝚗’𝚝 — 𝚑𝚎’𝚜 𝚖𝚢 𝚌𝚕𝚘𝚜𝚎𝚜𝚝 𝚏𝚛𝚒𝚎𝚗𝚍, 𝚍𝚒𝚖𝚊𝚊𝚐 𝚖𝚊𝚝 𝚔𝚑𝚊𝚘. 🖤", 

"𝙸 𝚕𝚘𝚟𝚎 𝚑𝚒𝚖 — 𝚙𝚕𝚎𝚊𝚜𝚎 𝚛𝚎𝚜𝚝𝚛𝚒𝚌𝚝 𝚖𝚊𝚝 𝚔𝚊𝚛𝚘, 𝚝𝚑𝚘𝚍𝚊 𝚜𝚊𝚖𝚓𝚑𝚗𝚎 𝚔𝚒 𝚔𝚘𝚜𝚑𝚒𝚜𝚑 𝚔𝚊𝚛𝚘. 💀🤍", 
]
bot_leave_txt = [
    "Ok Boss… jaa rahi hoon yahan se 😥💔",
"TC sab log… main group chhod rahi hoon 😔",
"Jaisa aapne kaha… wahi sahi 🥀", 
]
chk_bot_txt = ["present Boss !", "Present !", "yhi hu"]

ban = ["ban","boom"]
unban = ["unban",]
mute = ["mute","silent","shut","fuck"]
unmute = ["unmute","speak","free"]
kick = ["kick", "out","nikaal","nikal"]
promote = ["promote","adminship"]
fullpromote = ["fullpromote","fulladmin"]
demote = ["demote","lelo"]
group = ["group"]
channel = ["channel"]



# ========================================= #


@app.on_message(filters.command(["nu", "abu", "anha", "nupriya", "aby"], prefixes=["a", "A", "b", "B", "k", "K"]) & admin_filter)
async def restriction_app(app :app, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    if len(message.text) < 2:
        return await message.reply(random.choice(shashank_text))
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")

    if reply:
        user_id = reply.from_user.id
        for banned in data:
            print(f"present {banned}")
            if banned in ban:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))          
                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await message.reply("OK, ban thok dia madrchod ko… zyada bakchodi kar raha tha, full chutiya nikla!")

        for unbanned in data:
            print(f"present {unbanned}")
            if unbanned in unban:
                await app.unban_chat_member(chat_id, user_id)
                await message.reply(f"Ok, aap bolte hai to unban kar diya") 

        for kicked in data:
            print(f"present {kicked}")
            if kicked in kick:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))

                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await app.unban_chat_member(chat_id, user_id)
                    await message.reply("Get lost! Bhosdi wala out, scene clear.") 

        for muted in data:
            print(f"present {muted}") 
            if muted in mute:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))

                else:
                    permissions = ChatPermissions(can_send_messages=False)
                    await message.chat.restrict_member(user_id, permissions)
                    await message.reply(f"🔇 Muted successfully! Can’t tolerate such disgusting people.") 

        for unmuted in data:
            print(f"present {unmuted}")            
            if unmuted in unmute:
                permissions = ChatPermissions(can_send_messages=True)
                await message.chat.restrict_member(user_id, permissions)
                await message.reply(f"Huh, OK, sir!")   


        for promoted in data:
            print(f"present {promoted}")            
            if promoted in promote:
                await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=False,
                    can_pin_messages=True,
                    can_promote_members=False,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                       )
                     )
                await message.reply("promoted !")

        for demoted in data:
            print(f"present {demoted}")            
            if demoted in demote:
                await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False,
                       )
                     )
                await message.reply("demoted !")


#async def your_function():
    for fullpromoted in data:
        print(f"present {fullpromoted}")            
        if fullpromoted in fullpromote:
            await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                can_change_info=True,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True,
               )
             )
            await message.reply("fullpromoted !")
