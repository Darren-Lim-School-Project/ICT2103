import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# Import of SQLite 3
import sqlite3
from datetime import datetime

sqlbackToMainMenu = [
    [
        InlineKeyboardButton("Main Menu", callback_data='sqlmainmenu'),
    ],
]

# /help command 
def sql_payment(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(sqlbackToMainMenu)
    cartID = str(context.args[0])
    address = str(context.args[1]) + " " + str(context.args[2])
    print("address", address)
    datetime_now = datetime.now()
    dt_string = "'" + str(datetime_now.strftime('%d/%m/%Y %H:%M:%S')) + "'"
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    cur.execute("INSERT INTO Transaction_Info (cartID, shippingAddress) VALUES (" + str(cartID) + ", '" + str(address) + "')")
    cur.execute("SELECT transactionID FROM Transaction_Info WHERE cartID = " +str(cartID))
    transactionIDResult = cur.fetchone()[0]
    cur.execute("INSERT INTO Completed_Cart (transactionID, cartID, checkoutDate) VALUES (" + str(transactionIDResult) + ", " + str(cartID) + "," + str(dt_string) + ")")
    statement = ("SELECT completedCartID FROM Completed_Cart WHERE cartID = " + str(cartID))
    print("statmente ; ", statement)
    cur.execute("SELECT completedCartID FROM Completed_Cart WHERE cartID = " + str(cartID))
    completedCartIDResult = cur.fetchone()[0]
    cur.execute("INSERT INTO Cart_Transaction (completedCartID, transactionID) VALUES (" + str(completedCartIDResult) + ", " + str(transactionIDResult) + ")")
    cur.execute("DELETE FROM Shopping_Cart WHERE cartID =" + str(cartID))
    con.commit()
    con.close()

    # query.edit_message_text("<b>Payment</b>" + "\n\n" +
    #                         "Please make your payment of <b>$" + str('{:.2f}'.format(totalAmount)) + "</b>" + " to UEN Number: 1234567890" + "\n\n" +
    #                         "Thank you for your purchase!\n" +
    #                         "Use /start to start another transaction.", parse_mode="html", reply_markup=reply_markup)