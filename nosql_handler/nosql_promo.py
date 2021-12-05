from firestoredb import db, firestore
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

nosqlbackToMainMenu = [
    [
        InlineKeyboardButton("Main Menu", callback_data='nosqlmainmenu'),
    ],
]

# Show current Promo items
def nosql_promo(update, context):

    query = update.callback_query
    toMainMenu = InlineKeyboardMarkup(nosqlbackToMainMenu)
    stringAppend = ""
    productCategoryCol = db.collection(u'Products').document(u'Category').collections()
    for productCategory in productCategoryCol:
        for productInfo in productCategory.stream():
            if (productInfo.get('Promo') > 0 and productInfo.get('Stock') > 0):
                stringAppend = stringAppend + "Product ID: " + str(productInfo.id) + "\n" + "Name: " + str(productInfo.get('Name')) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(productInfo.get('Price')))]) + "\u0336 SGD$" + str('{:.2f}'.format(productInfo.get('Price') * (1 - (productInfo.get('Promo') / 100)))) + "\n" + "Stock: " + str(productInfo.get('Stock')) + "\n\n"
   
    query.edit_message_text("<b>NoSQL Promotion</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/nosql_tocart [Product ID] [Quantity]", parse_mode="html", reply_markup=toMainMenu)