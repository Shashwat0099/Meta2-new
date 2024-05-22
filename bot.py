import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_login import TelegramLogin

# Replace with your bot's API token
API_TOKEN = 'YOUR_API_TOKEN'

# Replace with your GitHub repository URL
GITHUB_REPO_URL = 'https://github.com/ShashwatMishra0099/Members.run.git'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter your phone number to log in.')

def login(update, context):
    phone_number = update.message.text
    # Send OTP request to Telegram API
    otp_sent = TelegramLogin.send_otp(phone_number)
    if otp_sent:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter the OTP sent to your phone.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Failed to send OTP.')

def otp_input(update, context):
    otp = update.message.text
    # Verify OTP with Telegram API
    login_success = TelegramLogin.verify_otp(otp)
    if login_success:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Login successful!')
        # Store the logged-in user's credentials securely
        # ...
        add_members(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid OTP.')

def add_members(update, context):
    # Read the "members.txt" file from your GitHub repository
    members_file = os.path.join(GITHUB_REPO_URL, 'members.txt')
    with open(members_file, 'r') as f:
        members = [line.strip() for line in f.readlines()]
    
    # Use the logged-in user's credentials to add members to the group
    bot = telegram.Bot(token=API_TOKEN)
    group_id = 'YOUR_GROUP_ID'
    for member in members:
        bot.add_chat_member(group_id, member)

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), login))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), otp_input))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
