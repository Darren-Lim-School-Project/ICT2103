from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext, commandhandler
import telegram
import firebase_admin
from datetime import datetime
from firebase_admin import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode

from handler.product import product, mickeymouse
from handler.tocart import tocart
from handler.cart import cart
from handler.help import help
from handler.checkout import checkout
from handler.promo import promo

# Variable Declaration
STATE = None
# STATEs for Drawing Keys
KEY_ID_DRAW = 1
DRAWER_NAME = 2
# STATEs for Returning Keys
KEY_ID_RETURN = 3
RETURN_NAME = 4
# Storage system for key
# keys_dict = {'key':'Name + ',' + Date'}
# Future implementation to store this information in cloud
keys_dict = {0: None, 1: "Keypress", 2: "Keypress",
             3: "Keypress", 4: "Keypress", 5: "Keypress"}

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

profilekeyboard = [
    [
        InlineKeyboardButton("Update Email Address", callback_data='email'),
        InlineKeyboardButton("Cart", callback_data='cart'),
    ], [
        InlineKeyboardButton("Checkout", callback_data='checkout'),
        InlineKeyboardButton("Promo", callback_data='promo'),
    ], [
        InlineKeyboardButton("Help", callback_data='help')
    ],
]
# End of variable declaration

# /start command
def start(update, context):
    first_name = update.message.chat.username

    reply_markup = InlineKeyboardMarkup(startkeyboard)
    update.message.reply_text("Hello " + str(first_name) +
                              " , nice to meet you and welcome to ABC shop!", reply_markup=reply_markup)

# Buttoon for callbackquery on inline button
def button(update: Update, context: CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data == "profile":
        profile(update, context)
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
        query.edit_message_text(text=f"Selected option: Update email")
    elif query.data == "mickeymouse":
        mickeymouse(update, context)

# /profile command
def profile(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(profilekeyboard)  # to change keyboard

    query.edit_message_text("*Profile:*" + "\n" +
                            "Some profile description thingyyyyyyyyyyyyyyyyyyyyyyyyyyy", parse_mode='MarkdownV2', reply_markup=reply_markup)

# Error message displayed to user
def error(update, context):
    update.message.reply_text('An error has occured')
    print("Error: " + str(error()))

# function to handle normal text
# Add the different STATE here as response are received through text
def text(update, context):
    global STATE

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
