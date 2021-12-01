import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext, commandhandler
import telegram
from datetime import datetime
from firestoredb import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode


nosqlstartkeyboard = [
    [
        InlineKeyboardButton("Profile", callback_data='nosqlprofile'),
        InlineKeyboardButton("Product", callback_data='nosqlproduct'),
    ],
    [
        InlineKeyboardButton("Cart", callback_data='nosqlcart'),
        InlineKeyboardButton("Checkout", callback_data='nosqlcheckout'),
    ], [
        InlineKeyboardButton("Promo", callback_data='nosqlpromo'),
        InlineKeyboardButton("Help", callback_data='nosqlhelp'),
    ],
]
# End of variable declaration

# /start command
def nosql_telebot(update, context):
    global chatid, username
    does_user_exist_result = 0
    reply_markup = InlineKeyboardMarkup(nosqlstartkeyboard)
    datetime_now = datetime.now()
    dt_string = "'" + str(datetime_now.strftime('%d/%m/%Y %H:%M:%S')) + "'"
    username = update.message.chat.username
    chatid = "'" + str(update.message.chat.id) + "'"
    fname = "'" + str(update.message.chat.first_name) + "'"
    lname = "'" + str(update.message.chat.last_name) + "'"
    counter = 0
    docs = db.collection(u'Customers').stream()
    for doc in docs:
        if (str(doc.id) == str(update.message.chat.id)):
            does_user_exist_result = 1
        counter += 1

    if (does_user_exist_result == 0):
        doc_ref = db.collection(u'Customers').document(f'{update.message.chat.id}')
        doc_ref.set({
            u'CustomerID' : counter,
            u'ChatID' : update.message.chat.id,
            u'fname': fname,
            u'lname':lname,
            u'email': None,
            u'loyaltyType': 0,
            u'firstAccessedDate': dt_string,
        })
        doc_ref = db.collection(u'Customers').document(f'{update.message.chat.id}').collection("accessDate").document()
        doc_ref.set({
            u'accessDate' : dt_string,
        })
        update.message.reply_text("Hello " + fname +
                              " , nice to meet you and welcome to ABC shop!", reply_markup=reply_markup)
    else:
        doc_ref = db.collection(u'Customers').document(f'{update.message.chat.id}').collection("accessDate").document()
        doc_ref.set({
            u'accessDate' : dt_string,
        })
        update.message.reply_text("Welcome back " + fname +
                              " , nice to meet you and welcome to ABC shop!", reply_markup=reply_markup)


# Main Menu
def nosql_mainmenu(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(nosqlstartkeyboard)
    # fname = "'" + str(update.message.chat.first_name) + "'"
    query.edit_message_text("Hello " + fname +
                              " , nice to meet you and welcome to ABC shop!", reply_markup=reply_markup)