import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

backToMainMenu = [
    [
        InlineKeyboardButton("Main Menu", callback_data='mainmenu'),
    ],
]

# /help command 
def payment(update, context, totalAmount):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(backToMainMenu)
    query.edit_message_text("<b>Payment</b>" + "\n\n" +
                            "Please make your payment of <b>$" + str('{:.2f}'.format(totalAmount)) + "</b>" + " to UEN Number: 1234567890" + "\n\n" +
                            "Thank you for your purchase!\n" +
                            "Use /start to start another transaction.", parse_mode="html", reply_markup=reply_markup)