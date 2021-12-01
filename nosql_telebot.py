import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext, commandhandler
import telegram
import firebase_admin
from datetime import datetime
from firebase_admin import db
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
    global chatid, username, fname
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    datetime_now = datetime.now()
    dt_string = "'" + str(datetime_now.strftime('%d/%m/%Y %H:%M:%S')) + "'"
    username = update.message.chat.username
    chatid = "'" + str(update.message.chat.id) + "'"
    fname = "'" + str(update.message.chat.first_name) + "'"
    lname = "'" + str(update.message.chat.last_name) + "'"
    reply_markup = InlineKeyboardMarkup(nosqlstartkeyboard)
    does_user_exist = cur.execute(f"SELECT EXISTS(SELECT * FROM Customers WHERE chatID = {chatid})")
    for i in does_user_exist:
        does_user_exist_result = i[0]
    if (does_user_exist_result == 0):
        cur.execute(f"INSERT INTO Customers ('chatID', 'fname','lname','loyaltyType','firstAccessedDate') VALUES ({chatid},{fname},{lname},0,{dt_string})")
        con.commit()
        cur.execute(f"INSERT INTO Customers_Access_Records ('customerID', 'accessDate') VALUES ((SELECT customerID FROM Customers WHERE chatID = {chatid}),{dt_string})")
        con.commit()
        update.message.reply_text("Hello " + fname +
                              " , nice to meet you and welcome to ABC shop!", reply_markup=reply_markup)
    else:
        cur.execute(f"INSERT INTO Customers_Access_Records ('customerID', 'accessDate') VALUES ((SELECT customerID FROM Customers WHERE chatID = {chatid}),{dt_string})")
        con.commit()
        update.message.reply_text("Welcome back " + fname +
                              " , nice to meet you and welcome to ABC shop!", reply_markup=reply_markup)


    # Inserting info into DB
    con.close()

# Main Menu
def nosql_mainmenu(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(nosqlstartkeyboard)
    # fname = "'" + str(update.message.chat.first_name) + "'"
    query.edit_message_text("Hello " + fname +
                              " , nice to meet you and welcome to ABC shop!", reply_markup=reply_markup)