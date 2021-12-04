import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from firestoredb import db, firestore

# Import of SQLite 3
import sqlite3

nosqlcheckoutkeyboard = [
    [
        InlineKeyboardButton("Back", callback_data='nosqlcart'),
        InlineKeyboardButton("Products", callback_data='nosqlproduct'),
    ],
]

nosqlcheckoutkeyboard1 = [
    [
        InlineKeyboardButton("No", callback_data='nosqlcart'),
        InlineKeyboardButton("Yes", callback_data='nosqlcheckoutimg'),
    ],
]
nosqlcheckoutkeyboard2 = [
    [
        InlineKeyboardButton("Cart", callback_data='nosqlcart'),
        InlineKeyboardButton("Product", callback_data='nosqlproduct'),
    ],
]

# Checkout Cart
def nosql_checkout(update, context, totalAmount, chatid):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(nosqlcheckoutkeyboard)
    reply_markup1 = InlineKeyboardMarkup(nosqlcheckoutkeyboard1)
    reply_markup2 = InlineKeyboardMarkup(nosqlcheckoutkeyboard2)

    cartProductID = []
    outOfStockItems = []
    stringAppend = ""

    if totalAmount == 0:
        query.edit_message_text("*NoSQL Checkout:*" + "\n" +
                            "You have no items in your cart\." + "\n" +
                            "There is no items to make payment\." + "\n" +
                            "Click on the 'Products' Button to browse products\!", parse_mode='MarkdownV2', reply_markup=reply_markup)
    else:
        userCart = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').stream()
        productCategory = db.collection(u'Products').document(u'Category').collections()
        for cartDetail in userCart:
            cartDetailToDict = cartDetail.to_dict()
            if (cartDetailToDict.get('Status') == "Active"):
                for cartProductDetailToDict in cartDetailToDict.get("Product"):
                    for productCategoryDetail in productCategory:
                        for productCategoryItem in productCategoryDetail.stream():
                            if ((cartProductDetailToDict.get("ProductID") == productCategoryItem.id) and (int(cartProductDetailToDict.get("Quantity")) > productCategoryItem.get("Stock"))):
                                outOfStockItems.append(productCategoryItem.get("Name"))
        
        if len(outOfStockItems) == 0:
            query.edit_message_text("<b>NoSQL Checkout</b>" + "\n\n" +
                            "Total Payable: <b>$" + str('{:.2f}'.format(totalAmount)) + "</b>\n\n" +
                            "Would you like to make payment?", parse_mode="html", reply_markup=reply_markup1)
        else:
            stringAppend = '\n'.join(outOfStockItems)
            query.edit_message_text("<b>NoSQL Checkout</b>" + "\n\n" +
                            "There is not enough stock for the follow items:" + "\n" +
                            stringAppend + "\n\n"
                            "You may want to double check the items instock from Products Page", parse_mode="html", reply_markup=reply_markup2)