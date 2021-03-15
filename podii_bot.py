# importing packages
import sys
import os
import logging

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext,MessageHandler, Filters, CallbackQueryHandler,ConversationHandler
# creating a user dictionaries
data = {}
# saving the dictionary as csv
import csv  
field_names = ['name', 'age', 'gender', 'attending']
with open('Names.csv', 'w') as podii_csv: 
    writer = csv.DictWriter(podii_csv, fieldnames = field_names) 
    writer.writeheader() 
    writer.writerow(data) 
# --- states use in conversation ---

NAME = 1
AGE = 2
GENDER = 3
ATTENDING = 4
# getting my token from env file
load_dotenv("D:/Purity/Podii_bot/.env")
Token = os.getenv('TOKEN')
# This function replies with 'Hello <user.first_name>'
def start(update: Update, context: CallbackContext) -> int:
    global data # to assign new dictionary to external/global variable
     # create new empty dictionary
    data = {}
    update.message.reply_text(f'Hello {update.effective_user.first_name} I am a bot. \n'
                              'It is nice to meet you.\n'
                              'Please write your full names or send /cancel to end this conversion.')
     # next state in conversation 
    return NAME                          
def get_name(update: Update, context: CallbackContext) -> int:
    data['name'] = update.message.text 
    update.message.reply_text('Please write your age')
    # next state in conversation 
    return AGE
def get_age(update: Update, context: CallbackContext) -> int:
    data['age'] = update.message.text
    reply_keyboard = [['Male', 'Female']]
    update.message.reply_text(
        'What is your gender?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return GENDER 
def get_gender(update: Update, context: CallbackContext) -> int:
    data['gender'] = update.message.text
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text(
        'Will you be attending our event?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return ATTENDING
def get_attending(update: Update, context: CallbackContext) -> int:
    data['attending'] = update.message.text
    update.message.reply_text(
        'Perfect. Thank you for your time. \n'
        'Type /info to view your data.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
def cancel(update: Update, context: CallbackContext) -> int:
    data['attending'] = update.message.text
    update.message.reply_text(
        'Bye! Thank you so much for your time.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
# creating coversation
my_conversation_handler = ConversationHandler(
   entry_points=[CommandHandler('start', start)],
   states={
       NAME: [
           CommandHandler('cancel', cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `name`
           MessageHandler(Filters.text, get_name)
       ],
       AGE: [
           CommandHandler('cancel', cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `age`
           MessageHandler(Filters.text, get_age)
       ],
       GENDER: [
           CommandHandler('cancel', cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `gender`
           MessageHandler(Filters.regex('^(Male|Female)$'), get_gender)
       ],
       ATTENDING: [
           CommandHandler('cancel', cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `attending`
           MessageHandler(Filters.regex('^(Yes|No)$') & ~Filters.command, get_attending)
       ],
   },
   fallbacks=[CommandHandler('cancel', cancel)]
)                

# this function replies to text sent to the bot that are not commands
def reply(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please type /start to begin or /end to end the conversation.')
reply_handler = MessageHandler(Filters.text & (~Filters.command), reply)
# this function handles any unknown command
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Sorry, I didn't understand that command. \n"
                             'Please type the correct one.')

unknown_handler = MessageHandler(Filters.command, unknown)
# this function prints data
def print_data():
    get_data = print(data)
    return get_data
# this function shows the printed data
def info(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(print_data())
data_handler = MessageHandler(Filters.command, info)
# this function ends the conversion
def end(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Bye! Thank you so much for your time.'
    )
end_handler = MessageHandler(Filters.command, end)

updater = Updater(Token)
# run the start function
updater.dispatcher.add_handler(my_conversation_handler)
# run the relpy function
updater.dispatcher.add_handler(reply_handler)
# run the data handler
updater.dispatcher.add_handler(data_handler)
# run the end function
updater.dispatcher.add_handler(end_handler)
# run the unknown function
updater.dispatcher.add_handler(unknown_handler)
# Connect to Telegram and wait for messages
updater.start_polling()
# Keep the program running until interrupted
updater.idle()