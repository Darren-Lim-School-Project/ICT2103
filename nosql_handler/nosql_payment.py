import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from firestoredb import db, firestore

nosqlbackToMainMenu = [
    [
        InlineKeyboardButton("Main Menu", callback_data='nosqlmainmenu'),
    ],
]

# /help command 
def nosql_payment(update, context, totalAmount):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(nosqlbackToMainMenu)
    query.edit_message_text("<b>NoSQL Payment</b>" + "\n\n" +
                            "Please make your payment of <b>$" + str('{:.2f}'.format(totalAmount)) + "</b>" + " to UEN Number: 1234567890" + "\n\n" +
                            "Thank you for your purchase!\n" +
                            "Use /start to start another transaction.", parse_mode="html", reply_markup=reply_markup)