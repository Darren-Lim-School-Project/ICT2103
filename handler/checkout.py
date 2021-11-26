import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Import of SQLite 3
import sqlite3

checkoutkeyboard = [
    [
        InlineKeyboardButton("Back", callback_data='cart'),
    ],
]

checkoutkeyboard1 = [
    [
        InlineKeyboardButton("No", callback_data='cart'),
        InlineKeyboardButton("Yes", callback_data='checkoutimg'),
    ],
]

# Checkout Cart
def checkout(update, context, totalAmount):
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(checkoutkeyboard)
    reply_markup1 = InlineKeyboardMarkup(checkoutkeyboard1)

    if totalAmount == 0:
        # A shopping cart does not exist
        # Does not exist so technically need to prompt them to add products to create new cart
        # So technically cart is empty
        query.edit_message_text("*Checkout:*" + "\n" +
                            "You have no items in your cart\." + "\n" +
                            "There is no items to make payment\." + "\n" +
                            "You may want to view products using /products", parse_mode='MarkdownV2', reply_markup=reply_markup)
            
    else:
        # Print out the text needed including the products
        query.edit_message_text("<b>Checkout</b>" + "\n\n" +
                            "Total Payable: <b>" + str('{:.2f}'.format(totalAmount)) + "</b>\n\n" +
                            "Would you like to make payment?", parse_mode="html", reply_markup=reply_markup1)