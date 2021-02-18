# importing packages
import sys
import os
import logging

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext,MessageHandler, Filters, CallbackQueryHandler,ConversationHandler
# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)
# getting my token from env file
load_dotenv("D:/Purity/Podii_bot/.env")
Token = os.getenv('TOKEN')
# This function replies with 'Hello <user.first_name>'
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name} I am a bot. \n'
                              'It is nice to meet you.\n'
                              'Send /rsvp to proceed otherwise send /cancel to end this conversation')
start_handler = CommandHandler('start', start)   
# This function asks whether you'll attend the event or not
def rsvp(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text(f' {update.effective_user.first_name} will you come to the event?',
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                             )
rsvp_handler = CommandHandler('rsvp', rsvp)
# this function replies to text sent to the bot that are not commands
def reply(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Okay thank you. Type /start to begin or /cancel when you are done.')
reply_handler = MessageHandler(Filters.text & (~Filters.command), reply)
# this function handles the cancel command
def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.'
    )
cancel_handler = CommandHandler('cancel', cancel)
# this function handles any unknown command
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Sorry, I didn't understand that command. \n"
                             'Please type the correct one.')

unknown_handler = MessageHandler(Filters.command, unknown)
updater = Updater(Token)
# run the start function
updater.dispatcher.add_handler(start_handler)
# run the rsvp function
updater.dispatcher.add_handler(rsvp_handler)
# run the relpy function
updater.dispatcher.add_handler(reply_handler)
# run the cancel function
updater.dispatcher.add_handler(cancel_handler)
# run the unknown function
updater.dispatcher.add_handler(unknown_handler)
# Connect to Telegram and wait for messages
updater.start_polling()
# Keep the program running until interrupted
updater.idle()