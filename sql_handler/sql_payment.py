import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# Import of SQLite 3
import sqlite3

sqlbackToMainMenu = [
    [
        InlineKeyboardButton("Main Menu", callback_data='sqlmainmenu'),
    ],
]

# /help command 
def sql_payment(update, context, totalAmount):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(sqlbackToMainMenu)
    query.edit_message_text("<b>Payment</b>" + "\n\n" +
                            "Please make your payment of <b>$" + str('{:.2f}'.format(totalAmount)) + "</b>" + " to UEN Number: 1234567890" + "\n\n" +
                            "Thank you for your purchase!\n" +
                            "Use /start to start another transaction.", parse_mode="html", reply_markup=reply_markup)

    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()

    cur.execute("SELECT p.instock, cc.quantity, p.productName from Products P, Cart_Contents cc WHERE cc.productID = p.productID")