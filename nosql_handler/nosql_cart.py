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
    global nosqlTotalAmount
    nosqlTotalAmount = 0
    activeCart = False
    stringAppend = ""

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(sqlcartkeyboard)
    docs = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').stream()
    catCol = db.collection(u'Products').document(u'Category').collections()
    if docs is not None:
        for doc in docs:
            cartInfoDict = doc.to_dict()
            if (cartInfoDict.get('Status') == "Active"):
                activeCart = True
                if (cartInfoDict.get('Product') is not None):
                    for categoryName in catCol:
                        for productsDetail in categoryName.stream():
                            for cartProduct in cartInfoDict.get('Product'):
                                if (int(productsDetail.get('Productid')) == int(cartProduct.get('ProductID'))):
                                    if int(productsDetail.get("Promo")) == 0:
                                        stringAppend = stringAppend + "Product ID: " + str(productsDetail.get('Productid')) + "\n" + "Name: " + str(productsDetail.get('Name')) + "\n" + "Price: SGD$" + str('{:.2f}'.format(productsDetail.get('Price'))) + "\n"+ "Quantity: " + str(cartProduct.get("Quantity")) + "\n\n"
                                        nosqlTotalAmount = nosqlTotalAmount + (float(productsDetail.get('Price')) * float(cartProduct.get("Quantity")))
                                    else:
                                        stringAppend = stringAppend + "Product ID: " + str(productsDetail.get('Productid')) + "\n" + "Name: " + str(productsDetail.get('Name')) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(productsDetail.get('Price')))]) + "\u0336 SGD$" + str('{:.2f}'.format(productsDetail.get('Price') * (1 - (productsDetail.get('Promo') / 100)))) + "\n"+ "Quantity: " + str(cartProduct.get("Quantity")) + "\n\n"
                                        nosqlTotalAmount = nosqlTotalAmount + (float(productsDetail.get('Price')) * float(cartProduct.get("Quantity")))
                else:
                    query.edit_message_text("<b>NoSQL Cart</b>" + "\n\n" +
                                                "There are no items in the cart. You may want to view products add them in", parse_mode="html", reply_markup=reply_markup)
                    return


    if activeCart == False:
        query.edit_message_text("<b>NoSQL Cart</b>" + "\n\n" +
                                            "There are no items in the cart. You may want to view products add them in", parse_mode="html", reply_markup=reply_markup)
    else:
        query.edit_message_text("<b>NoSQL Cart</b>" + "\n\n" +
                                                stringAppend + "" +
                                                "Total Payable: <b>$" + str('{:.2f}'.format(nosqlTotalAmount)) + "</b>\n\n"
                                                "To delete an item from cart, use" + "\n" + "/nosql_delete [Product ID] [Quantity]" + "\n"
                                                "example: /nosql_delete 1 2", parse_mode="html", reply_markup=reply_markup)

def nosql_getTotalAmount():
    return nosqlTotalAmount