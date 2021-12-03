import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from firestoredb import db

# Import of SQLite 3
import sqlite3

sqlcartkeyboard = [
    [
        InlineKeyboardButton("Main Menu", callback_data='nosqlmainmenu'),
        InlineKeyboardButton("Checkout", callback_data='nosqlcheckout'),
    ],
    [
        InlineKeyboardButton("Products", callback_data='nosqlproduct'),
    ],
]

# Show Cart
def nosql_cart(update, context, chatid):
    global totalAmount
    totalAmount = 0
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    counter = 0

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(sqlcartkeyboard)
    docs = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').stream()
    for doc in docs:
        toDict = doc.to_dict()
        counter = counter + 1
    # Check if got cart or not cart
    # != 0 means got cart
    if counter != 0:
        # Check if cart got any product
        anyProduct = toDict.get('Product')

        # If got product
        if anyProduct is not None:
            stringAppend = ""
            totalAmount = 0
            productList = []
            # Get all product details
            docs = db.collection(u'Products').document(u'Category').collections()
            for doc in docs:
                for i in doc.stream():
                    productList.append(i.to_dict())
            # Store all productID from cart to an array
            for i in anyProduct:
                for x in productList:
                    productListProductid = x.get('Productid')
                    if int(productListProductid) == int(i.get("ProductID")):
                        if int(x.get("Promo")) == 0:
                            stringAppend = stringAppend + "Product ID: " + str(x.get('Productid')) + "\n" + "Name: " + str(x.get('Name')) + "\n" + "Price: SGD$" + str('{:.2f}'.format(x.get('Price'))) + "\n"+ "Quantity: " + str(i.get("Quantity")) + "\n\n"
                            totalAmount = totalAmount + (float(x.get('Price')) * float(i.get("Quantity")))
                        else:
                            stringAppend = stringAppend + "Product ID: " + str(x.get('Productid')) + "\n" + "Name: " + str(x.get('Name')) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(x.get('Price')))]) + "\u0336 SGD$" + str('{:.2f}'.format(x.get('Price') * (1 - (x.get('Promo') / 100)))) + "\n"+ "Quantity: " + str(i.get("Quantity")) + "\n\n"
                            totalAmount = totalAmount + (float(x.get('Price')) * float(i.get("Quantity")))

            query.edit_message_text("<b>Cart</b>" + "\n\n" +
                                        stringAppend + "" +
                                        "Total Payable: <b>$" + str('{:.2f}'.format(totalAmount)) + "</b>\n\n"
                                        "To delete an item from cart, use" + "\n" + "/nosql_delete [Product ID] [Quantity]" + "\n"
                                        "example: /nosql_delete 1 2", parse_mode="html", reply_markup=reply_markup)
        # If no product
        else:
            query.edit_message_text("*Cart:*" + "\n" +
                            "You have no items in your cart\." + "\n" +
                            "Click on the 'Products' Button to browse products\!", parse_mode='MarkdownV2', reply_markup=reply_markup)
    else:
        query.edit_message_text("*Cart:*" + "\n" +
                            "You have no items in your cart\." + "\n" +
                            "Click on the 'Products' Button to browse products\!", parse_mode='MarkdownV2', reply_markup=reply_markup)
       

def nosql_getTotalAmount():
    return totalAmount