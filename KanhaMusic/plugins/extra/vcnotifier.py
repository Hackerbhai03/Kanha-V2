from typing import List, Optional, Union

from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import ChatPrivileges, Message

from KanhaMusic import app
from KanhaMusic.utils.database import get_assistant


# ---------------------------------------------------------
# 🔥 Command Helper
# ---------------------------------------------------------
def command(commands: Union[str, List[str]]):
    return filters.command(commands, prefixes=["/", "!"])


# ---------------------------------------------------------
# 🎧 Get Active Voice Chat
# ---------------------------------------------------------
async def get_group_call(
    assistant: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:

    chat_peer = await assistant.resolve_peer(message.chat.id)

    full_chat = None
    if isinstance(chat_peer, InputPeerChannel):
        full_chat = (await assistant.invoke(GetFullChannel(channel=chat_peer))).full_chat
    elif isinstance(chat_peer, InputPeerChat):
        full_chat = (await assistant.invoke(GetFullChat(chat_id=chat_peer.chat_id))).full_chat

    if full_chat and full_chat.call:
        return full_chat.call

    await app.send_message(
        message.chat.id,
        f"❌ 𝐍𝐎 𝐀𝐂𝐓𝐈𝐕𝐄 𝐕𝐎𝐈𝐂𝐄 𝐂𝐇𝐀𝐓 {err_msg}"
    )
    return None


# ---------------------------------------------------------
# 🚀 START VOICE CHAT
# ---------------------------------------------------------
@app.on_message(command(["vcstart", "startvc"]) & filters.group)
async def start_group_call(c: Client, m: Message):
    chat_id = m.chat.id
    assistant = await get_assistant(chat_id)
    if not assistant:
        return await app.send_message(chat_id, "❌ 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐍𝐨𝐭 𝐅𝐨𝐮𝐧𝐝")

    ass = await assistant.get_me()
    assid = ass.id

    msg = await app.send_message(chat_id, "🎙 𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭...\n━━━━━━━━━━━━━━")

    try:
        peer = await assistant.resolve_peer(chat_id)
        await assistant.invoke(
            CreateGroupCall(
                peer=InputPeerChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
                random_id=assistant.rnd_id() // 9000000000,
            )
        )
        await msg.edit_text("✅ 𝐕𝐎𝐈𝐂𝐄 𝐂𝐇𝐀𝐓 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 👑")

    except ChatAdminRequired:
        try:
            # Temporary Promote
            await app.promote_chat_member(
                chat_id,
                assid,
                privileges=ChatPrivileges(can_manage_video_chats=True),
            )

            peer = await assistant.resolve_peer(chat_id)
            await assistant.invoke(
                CreateGroupCall(
                    peer=InputPeerChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
                    random_id=assistant.rnd_id() // 9000000000,
                )
            )

            # Remove permission
            await app.promote_chat_member(
                chat_id,
                assid,
                privileges=ChatPrivileges(can_manage_video_chats=False),
            )

            await msg.edit_text("✅ 𝐕𝐎𝐈𝐂𝐄 𝐂𝐇𝐀𝐓 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 👑")

        except:
            await msg.edit_text("❌ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐆𝐢𝐯𝐞 𝐕𝐢𝐝𝐞𝐨 𝐂𝐡𝐚𝐭 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐓𝐨 𝐁𝐨𝐭")


# ---------------------------------------------------------
# 🛑 END VOICE CHAT
# ---------------------------------------------------------
@app.on_message(command(["vcend", "endvc"]) & filters.group)
async def stop_group_call(c: Client, m: Message):
    chat_id = m.chat.id
    assistant = await get_assistant(chat_id)
    if not assistant:
        return await app.send_message(chat_id, "❌ 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐍𝐨𝐭 𝐅𝐨𝐮𝐧𝐝")

    ass = await assistant.get_me()
    assid = ass.id

    msg = await app.send_message(chat_id, "🔻 𝐄𝐧𝐝𝐢𝐧𝐠 𝐕𝐨𝐢𝐜𝐞 𝐂𝐡𝐚𝐭...\n━━━━━━━━━━━━━━")

    try:
        group_call = await get_group_call(assistant, m, err_msg="• Already Ended")
        if not group_call:
            return

        await assistant.invoke(DiscardGroupCall(call=group_call))
        await msg.edit_text("🛑 𝐕𝐎𝐈𝐂𝐄 𝐂𝐇𝐀𝐓 𝐄𝐍𝐃𝐄𝐃 👑")

    except Exception as e:
        if "GROUPCALL_FORBIDDEN" in str(e):
            try:
                # Temporary Promote
                await app.promote_chat_member(
                    chat_id,
                    assid,
                    privileges=ChatPrivileges(can_manage_video_chats=True),
                )

                group_call = await get_group_call(assistant, m, err_msg="• Already Ended")
                if not group_call:
                    return

                await assistant.invoke(DiscardGroupCall(call=group_call))

                # Remove permission
                await app.promote_chat_member(
                    chat_id,
                    assid,
                    privileges=ChatPrivileges(can_manage_video_chats=False),
                )

                await msg.edit_text("🛑 𝐕𝐎𝐈𝐂𝐄 𝐂𝐇𝐀𝐓 𝐄𝐍𝐃𝐄𝐃 👑")
            except:
                await msg.edit_text("❌ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐆𝐢𝐯𝐞 𝐕𝐢𝐝𝐞𝐨 𝐂𝐡𝐚𝐭 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐓𝐨 𝐁𝐨𝐭")


# ---------------------------------------------------------
# 🎥 AUTO DETECT - VC STARTED
# ---------------------------------------------------------
@app.on_message(filters.video_chat_started & filters.group)
async def auto_vc_started(client: Client, message: Message):
    await message.reply_text(
      
        f"> 🎥 𝐕𝐎𝐈𝐂𝐄 𝐂𝐇𝐀𝐓 𝐈𝐒 𝐍𝐎𝐖 𝐋𝐈𝐕𝐄 👑\n"
        f"> 🏷 {message.chat.title}\n"
        f"> ⚡ Join Now & Enjoy The Session!"
    )


# ---------------------------------------------------------
# 🚫 AUTO DETECT - VC ENDED
# ---------------------------------------------------------
@app.on_message(filters.video_chat_ended & filters.group)
async def auto_vc_ended(client: Client, message: Message):
    await message.reply_text(
        
        f"> 🛑 𝐕𝐎𝐈𝐂𝐄 𝐂𝐇𝐀𝐓 𝐇𝐀𝐒 𝐄𝐍𝐃𝐄𝐃 👋\n"
        f"> 🏷 {message.chat.title}\n"
        f"> 🔥 See You In Next Session!"
    )
