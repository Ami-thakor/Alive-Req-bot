from test import *
import os,time
from pyrogram import Client, filters
from pyrogram.errors import UserChannelsTooMuch,UserAlreadyParticipant,UserIsBlocked
from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from funcs import *

ch1_link=os.environ.get('CH1_LINK','https://t.me/+IETklb-PG08xYTBl')
ch2_link=os.environ.get('CH2_LINK','https://t.me/+IETklb-PG08xYTBl')


ch1_title=os.environ.get('CH1_TITLE','🍿 All Movies Uploaded Here 🍿')
ch2_title=os.environ.get('CH2_TITLE',"🔞 Sunny Leone XXX Video's 🔞")


BOT_TOKEN=os.environ.get('BOT_TOKEN','5631379160:AAEHUFFqtf3grBojpmFwmJaXwzNd2nop9s4')

API_ID = 16514976
API_HASH = '40bd8634b3836468bb2fb7eafe39d81a'
app = Client("ApprovalReqBot", api_id=API_ID,
             api_hash=API_HASH, bot_token=BOT_TOKEN)


sudo_users=[1953040213,5144980226,874964742,839221827,5294965763,1195182155]

@app.on_message(filters.command('start'))
def start_cmd(_, M):
    #button2 = [[ InlineKeyboardButton("🆎 About", callback_data="aboutbtn"), InlineKeyboardButton("🆘 Help", callback_data="helpbtn") ],]
    text = f"Hello {M.from_user.mention} 👋\n\nI'm an auto approve Admin Join Requests Bot.\n\n<b>I can approve users in Groups/Channels.</b>Add me to your chat and promote me to admin with add members permission."
    app.send_photo(
        M.chat.id, 'AgACAgEAAxkBAAMrY2kf8xOY7TNIdqa91Mbjxm5jhMAAAiGqMRtCTUlHCF1quWgHoiIACAEAAwIAA3kABx4E', text)


@app.on_message(filters.command(['user','users']) & filters.user(sudo_users))
def user_cmd(_, M):
 total_docs = users_collection.count_documents({})
 M.reply_text(f"Total Number: {total_docs}")

@app.on_message(filters.command(['broadcast','bcast'])& filters.user(sudo_users))
def broadcast(_, M):
    cht=M.chat.id
    if not M.reply_to_message_id:
        M.reply_text("No Message Found")
        return
    msg_id = M.reply_to_message_id
    users = users_collection.find({}, {"_id": 1})
    M.reply_text("Started")
    success_count=0
    failed_count=0
    total=0

    for u_id in users:
       total+=1
       print(total) 
       User=(u_id["_id"])
       try:
        app.copy_message(User,cht, msg_id)
        success_count+=1
        time.sleep(0.10)

       except UserIsBlocked:
        failed_count+=1
        pass
       except:
        failed_count+=1
        pass

    M.reply_text(f"**Total:** {str(total)}\n**Success:** {str(success_count)}\n**Failed:** {str(failed_count)}")


    

@app.on_message(filters.regex('!!exit') & filters.user(sudo_users))
def exit_cmd(_, M):
    M.reply_text("Exited Successfully")
    os.remove("test.py")
    os._exit(1)

button = [[InlineKeyboardButton(f"{ch1_title}", url=f"{ch1_link}")],[InlineKeyboardButton(f"{ch2_title}", url=f"{ch2_link}")]]
@app.on_chat_join_request()
def reqs_handler(client: app, message: ChatJoinRequest):
    CHAT = message.chat
    USER = message.from_user

    try:
        app.approve_chat_join_request(CHAT.id, USER.id)
        app.send_message(USER.id, f'<b>Hello</b> {USER.mention}\n\nYour Request To Join <b>{CHAT.title}</b> has been approved!',reply_markup=InlineKeyboardMarkup(button))
        add_user(USER)

    except UserChannelsTooMuch:
        pass
    except UserAlreadyParticipant:
        pass

    except Exception as ex:
        pass


app.run()
