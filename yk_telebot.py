from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext, commandhandler
import telegram
import firebase_admin
import sqlite3
from datetime import datetime
from firebase_admin import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode

from handler.product import product, mickeymouse
from handler.tocart import tocart
from handler.cart import cart
from handler.help import help
from handler.checkout import checkout
from handler.promo import promo

from handler.profile import profile, received_email


# Variable Declaration
STATE = 0
# STATEs for Drawing Keys
GET_EMAIL = 1

startkeyboard = [
    [
        InlineKeyboardButton("Profile", callback_data='profile'),
        InlineKeyboardButton("Product", callback_data='product'),
    ],
    [
        InlineKeyboardButton("Cart", callback_data='cart'),
        InlineKeyboardButton("Checkout", callback_data='checkout'),
    ], [
        InlineKeyboardButton("Promo", callback_data='promo'),
        InlineKeyboardButton("Help", callback_data='help'),
    ],
]


# End of variable declaration

# /start command
def start(update, context):
    global chatid, username
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    datetime_now = datetime.now()
    dt_string = "'" + str(datetime_now.strftime('%d/%m/%Y %H:%M:%S')) + "'"
    username = update.message.chat.username
    chatid = "'" + str(update.message.chat.id) + "'"
    fname = "'" + str(update.message.chat.first_name) + "'"
    lname = "'" + str(update.message.chat.last_name) + "'"
    reply_markup = InlineKeyboardMarkup(startkeyboard)
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

# Buttoon for callbackquery on inline button


def button(update: Update, context: CallbackContext):
    global STATE
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data == "profile":
        profile(update, context, chatid, username)
    elif query.data == "cart":
        query.edit_message_text(text=f"Selected option: Cart")
    elif query.data == "checkout":
        query.edit_message_text(text=f"Selected option: Checkout")
    elif query.data == "product":
        #query.edit_message_text(text=f"Selected option: Product")
        product(update, context)
    elif query.data == "promo":
        promo(update, context)
    elif query.data == "help":
        help(update, context)
    elif query.data == "email":
        STATE = GET_EMAIL
        query.edit_message_text(text=f"Enter your email address")
    elif query.data == "mickeymouse":
        mickeymouse(update, context)

# Error message displayed to user


def error(update, context):
    update.message.reply_text('An error has occured')
    print("Error: " + str(error()))

# function to handle normal text
# Add the different STATE here as response are received through text


def text(update, context):
    global STATE

    if STATE == GET_EMAIL:
        received_email(update, context, chatid)
# Main function
# THIS IS THE PART THAT LINK THE COMMANDS TO THE FUNCTION


def main():
    # Change TOKEN here
    TOKEN = "1509494665:AAGBFYwXPxGEeIkogksR7CEZlVyqYf9kNBM"

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    # CommandHandler(Command User Type, function to call)
    # Add commands here
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("product", product))
    dispatcher.add_handler(CommandHandler("cart", cart))
    dispatcher.add_handler(CommandHandler("checkout", checkout))
    dispatcher.add_handler(CommandHandler("profile", profile))
    dispatcher.add_handler(CommandHandler("promo", promo))
    dispatcher.add_handler(CommandHandler("tocart", tocart, pass_args=True))
    dispatcher.add_handler(CommandHandler("mickeymouse", mickeymouse))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
