import asyncio
import os
import time
from pyrogram import Client, filters
from pyrogram.errors import UserChannelsTooMuch, UserAlreadyParticipant, UserIsBlocked
from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup

from funcs import *

ch1_link = os.environ.get('CH1_LINK', 'https://t.me/VIP_membership_200')
ch2_link = os.environ.get('CH2_LINK', 'https://t.me/Adult_files46')

ch1_title = os.environ.get('CH1_TITLE', 'VIP Membership only 149₹ 👈')
ch2_title = os.environ.get('CH2_TITLE', "🍿Join BackUp Channel 🍿")

BOT_TOKEN = os.environ.get(
    'BOT_TOKEN', '6645936369:AAEqeVXD9gFh3NCNi6ioRKnIJBk4UI9qMHw')

API_ID = 16514976
API_HASH = '40bd8634b3836468bb2fb7eafe39d81a'
app = Client("KingReqBot", api_id=API_ID,
             api_hash=API_HASH, bot_token=BOT_TOKEN)

sudo_users = [1953040213, 5144980226, 874964742,
              839221827, 5294965763, 1195182155]


@app.on_message(filters.command('start'))
async def start_cmd(_, M):
    text = f"Hello {M.from_user.mention} 👋\n\nI'm an auto approve Admin Join Requests Bot.\n\n<b>I can approve users in Groups/Channels.</b>Add me to your chat and promote me to admin with add members permission."
    await app.send_photo(M.chat.id, 'https://te.legra.ph/file/9ccb06149e194ba2f38d7.jpg', text)


@app.on_message(filters.command(['user', 'users']) & filters.user(sudo_users))
async def user_cmd(_, M):
    total_docs = await users_collection.count_documents({})
    await M.reply_text(f"Total Users: {total_docs}")


@app.on_message(
    filters.command(['broadcast', 'bcast']) & filters.user(sudo_users))
async def broadcast(_, M):
    if not M.reply_to_message_id:
        await M.reply_text("No Message Found")
        return

    ids = await getid()
    success = 0
    failed = 0
    total = len(ids)
    msG = await M.reply_text(f"Started Broadcast\n\nTotal users: {str(total)}")
    for userid in ids:
        if success % 200 == 0:
            try:
                await msG.edit_text(
                    f"In Progress\n\n**Total:** {str(total)}\n**Success:** {str(success)}\n**Failed:** {str(failed)}"
                )

            except:
                pass

        try:
            await M.reply_to_message.copy(userid, disable_notification=True)
            await asyncio.sleep(0.3)
            success += 1
        except:
            failed += 1

            pass
    await M.reply_text(
        f"**Total:** {str(total)}\n**Success:** {str(success)}\n**Failed:** {str(failed)}"
    )


# promotion photo
PHOTO_URL = "https://telegra.ph/file/bd3f2968f4b0eef1d60fc.jpg"
CAPTION = """<b>8000+ 𝘚𝘌𝘟 𝘝𝘐𝘋𝘌𝘖𝘚 🔞🔞 
❌ 🔗 NO LINK  ❌
🤤 DIRECT VIDEO 🤤 
✅ VIP MEMEBERSHIP✅
😎 LIFETIME 😎
😲 ONLY 149₹ 💋
  
DM 👉 @VIP_membership_200
DM 👉 @VIP_membership_200</b>"""


button = [[InlineKeyboardButton(f"{ch1_title}", url=f"{ch1_link}")],
          [InlineKeyboardButton(f"{ch2_title}", url=f"{ch2_link}")]]


@app.on_chat_join_request()
async def reqs_handler(client: app, message: ChatJoinRequest):
    CHAT = message.chat
    USER = message.from_user

    try:
        await app.approve_chat_join_request(CHAT.id, USER.id)
        await app.send_photo(USER.id, PHOTO_URL, CAPTION, reply_markup=InlineKeyboardMarkup(button))
        # await app.send_message(USER.id, f'<b>Hello</b> {USER.mention}\n\nYour Request To Join <b>{CHAT.title}</b> has been approved!', reply_markup=InlineKeyboardMarkup(button))
        await add_user(USER)

    except UserChannelsTooMuch:
        pass
    except UserAlreadyParticipant:
        pass

    except Exception as ex:
        pass

print("Bot started :)")
app.run()
