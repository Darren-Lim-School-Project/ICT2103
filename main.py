import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext, commandhandler
import telegram
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from firestoredb import db
from functools import partial

# SQL
from sql_telebot import sql_telebot, sql_mainmenu
from sql_handler.sql_product import sql_product, sql_mickeymouse, sql_disneyAndPixar, sql_marvel, sql_frozen
from sql_handler.sql_tocart import sql_tocart
from sql_handler.sql_cart import sql_cart, sql_getTotalAmount
from sql_handler.sql_help import sql_help
from sql_handler.sql_checkout import sql_checkout
from sql_handler.sql_promo import sql_promo
from sql_handler.sql_delete import sql_delete
from sql_handler.sql_payment import sql_payment
from sql_handler.sql_profile import sql_profile, sql_received_email

# NoSQL
from nosql_telebot import nosql_telebot, nosql_mainmenu
from nosql_handler.nosql_product import nosql_product, nosql_mickeymouse, nosql_disneyAndPixar, nosql_marvel, nosql_frozen
from nosql_handler.nosql_tocart import nosql_tocart
from nosql_handler.nosql_cart import nosql_cart, nosql_getTotalAmount
from nosql_handler.nosql_help import nosql_help
from nosql_handler.nosql_checkout import nosql_checkout
from nosql_handler.nosql_promo import nosql_promo
from nosql_handler.nosql_delete import nosql_delete
from nosql_handler.nosql_payment import nosql_payment
from nosql_handler.nosql_profile import nosql_profile, nosql_received_email

# Variable Declaration
STATE = 0
global totalAmount
# STATEs for Drawing Keys
SQL_GET_EMAIL = 1
NOSQL_GET_EMAIL = 2
# End of variable declaration

# /start command
def start(update, context):
    global chatid, fname, username
    chatid = update.message.chat.id
    fname = update.message.chat.first_name
    username = update.message.chat.username
    update.message.reply_text("Hello " + username + " , nice to meet you and welcome to ABC shop!\n\nPlease select your choice of database:\n/sql_telebot for SQL Database structure\n/nosql_telebot for NoSQL Database Structure")

# Buttoon for callbackquery on inline button
def button(update: Update, context: CallbackContext):
    global STATE
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

# Add the different STATE here as response are received through text
def text(update, context):
    global STATE

    if STATE == SQL_GET_EMAIL:
        sql_received_email(update, context, chatid)
        STATE = 0
    elif STATE == NOSQL_GET_EMAIL:
        nosql_received_email(update, context, chatid)
        STATE = 0

# Error message displayed to user
def error(update, context):
    update.message.reply_text('An error has occured')
    print("Error: " + str(error()))

# Buttoon for callbackquery on inline button
def button(update: Update, context: CallbackContext):
    global STATE
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    # SQL
    if query.data == "sqlprofile":
        sql_profile(update, context, chatid, username)
    elif query.data == "sqlcart":
        sql_cart(update, context)
    elif query.data == "sqlcheckout":
        sql_checkout(update, context, sql_getTotalAmount())
    elif query.data == "sqlproduct":
        sql_product(update, context)
    elif query.data == "sqlpromo":
        sql_promo(update, context)
    elif query.data == "sqlhelp":
        sql_help(update, context)
    elif query.data == "sqlemail":
        STATE = SQL_GET_EMAIL
        query.edit_message_text(text=f"Enter your email address")
    elif query.data == "sqlmickeymouse":
        sql_mickeymouse(update, context)
    elif query.data == "sqlpixar":
        sql_disneyAndPixar(update, context)
    elif query.data == "sqlmarvel":
        sql_marvel(update, context)
    elif query.data == "sqlfrozen":
        sql_frozen(update, context)
    elif query.data == "sqlback":
        start(update, context)
    elif query.data == "sqlcheckoutimg":
        sql_payment(update, context, sql_getTotalAmount())
    elif query.data == "sqlmainmenu":
        sql_mainmenu(update, context)
    # NoSQL
    elif query.data == "nosqlprofile":
        nosql_profile(update, context, chatid,username)
    elif query.data == "nosqlcart":
        nosql_cart(update, context, chatid)
    elif query.data == "nosqlcheckout":
        nosql_checkout(update, context, nosql_getTotalAmount(), chatid)
    elif query.data == "nosqlproduct":
        nosql_product(update, context)
    elif query.data == "nosqlpromo":
        nosql_promo(update, context)
    elif query.data == "nosqlhelp":
        nosql_help(update, context)
    elif query.data == "nosqlemail":
        STATE = NOSQL_GET_EMAIL
        query.edit_message_text(text=f"Enter your email address")
    elif query.data == "nosqlmickeymouse":
        nosql_mickeymouse(update, context)
    elif query.data == "nosqlpixar":
        nosql_disneyAndPixar(update, context)
    elif query.data == "nosqlmarvel":
        nosql_marvel(update, context)
    elif query.data == "nosqlfrozen":
        nosql_frozen(update, context)
    elif query.data == "nosqlback":
        start(update, context)
    elif query.data == "nosqlcheckoutimg":
        nosql_payment(update, context, nosql_getTotalAmount())
    elif query.data == "nosqlmainmenu":
        nosql_mainmenu(update, context)

# Main function
# THIS IS THE PART THAT LINK THE COMMANDS TO THE FUNCTION
def main():
    # Change TOKEN here
    # YK
    #TOKEN = "1509494665:AAGBFYwXPxGEeIkogksR7CEZlVyqYf9kNBM"
    # Darren
    TOKEN = "2140713559:AAFunBF0TFdivjUeskd1TLNtKwwfhT_bnIE"
    # Ken
    #TOKEN = "2132985175:AAEMPGwqmVmki5okwnzoonFti0XN5NlT4UA"

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    # CommandHandler(Command User Type, function to call)
    # Add commands here
    # Some clean up done on 27 Nov, should probably need start, end, sql_tocart, and delete commands. the rest should be by button
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("sql_tocart", sql_tocart, pass_args=True))
    dispatcher.add_handler(CommandHandler("nosql_tocart", nosql_tocart, pass_args=True))
    dispatcher.add_handler(CommandHandler("sql_telebot", sql_telebot, pass_args=True))
    dispatcher.add_handler(CommandHandler("nosql_telebot", nosql_telebot, pass_args=True))
    dispatcher.add_handler(CommandHandler("sql_delete", sql_delete, pass_args=True))
    dispatcher.add_handler(CommandHandler("nosql_delete", nosql_delete, pass_args=True))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
