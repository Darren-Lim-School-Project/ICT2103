import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from firestoredb import db

# Import of SQLite 3
import sqlite3

nosqlproductkeyboard = [
    [
        InlineKeyboardButton("Mickey Mouse and Friends", callback_data='nosqlmickeymouse'),
        InlineKeyboardButton("Disney and Pixar", callback_data='nosqlpixar'),
        
    ], [
        InlineKeyboardButton("Marvel", callback_data='nosqlmarvel'),
        InlineKeyboardButton("Frozen", callback_data='nosqlfrozen'),
    ],
]

nosqldisplayedProductkeyboard = [
    [
        InlineKeyboardButton("Back", callback_data='nosqlproduct'),
        
    ],
]

# /product command
def nosql_product(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(nosqlproductkeyboard)  # to change keyboard

    query.edit_message_text("*NoSQL Product Menu:*" + "\n" +
                            "Mickey Mouse and Friends   \- View Mickey Mouse and Friends Category " + "\n" + 
                            "Disney and Pixar           \- View Disney and Pixar Category " + "\n" +
                            "Marvel                     \- View Marvel Category " + "\n" +
                            "Frozen                     \- View Frozen Category " + "\n\n" +
                            "Please select a category to view the product inside\.", parse_mode='MarkdownV2', reply_markup=reply_markup)

# /mickeymouse command
def nosql_mickeymouse(update, context):
    reply_markup = InlineKeyboardMarkup(nosqldisplayedProductkeyboard)  # to change keyboard
    query = update.callback_query
    docs = db.collection(u'Products').document(u'Category').collection(u'Mickey Mouse and Friends').stream()
    stringAppend = ""
    for doc in docs:
        toDict = doc.to_dict()
        if (toDict.get('Promo') == 0):
            stringAppend = stringAppend + "Product ID: " + str(doc.id) + "\n" + "Name: " + str(toDict.get('Name')) + "\n" + "Price: SGD$" + str('{:.2f}'.format(toDict.get('Price'))) + "\n" + "Stock: " + str(toDict.get('Stock')) + "\n\n"
        else:
            stringAppend = stringAppend + "Product ID: " + str(doc.id) + "\n" + "Name: " + str(toDict.get('Name')) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(toDict.get('Price')))]) + "\u0336 SGD$" + str('{:.2f}'.format(toDict.get('Price') * (1 - (toDict.get('Promo') / 100)))) + "\n" + "Stock: " + str(toDict.get('Stock')) + "\n\n"
        #print(f'{doc.id} => {doc.to_dict()}')

    query.edit_message_text("<b>NoSQL Mickey Mouse and Friends Product</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/nosql_tocart [Product ID] [Quantity]", parse_mode="html", reply_markup=reply_markup)

# /disney and pixar command
def nosql_disneyAndPixar(update, context):
    reply_markup = InlineKeyboardMarkup(nosqldisplayedProductkeyboard)  # to change keyboard
    query = update.callback_query
    docs = db.collection(u'Products').document(u'Category').collection(u'Disney and Pixar').stream()
    stringAppend = ""
    for doc in docs:
        toDict = doc.to_dict()
        if (toDict.get('Promo') == 0):
            stringAppend = stringAppend + "Product ID: " + str(doc.id) + "\n" + "Name: " + str(toDict.get('Name')) + "\n" + "Price: SGD$" + str('{:.2f}'.format(toDict.get('Price'))) + "\n" + "Stock: " + str(toDict.get('Stock')) + "\n\n"
        else:
            stringAppend = stringAppend + "Product ID: " + str(doc.id) + "\n" + "Name: " + str(toDict.get('Name')) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(toDict.get('Price')))]) + "\u0336 SGD$" + str('{:.2f}'.format(toDict.get('Price') * (1 - (toDict.get('Promo') / 100)))) + "\n" + "Stock: " + str(toDict.get('Stock')) + "\n\n"
        #print(f'{doc.id} => {doc.to_dict()}')

    query.edit_message_text("<b>NoSQL Disney and Pixar Product</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/nosql_tocart [Product ID] [Quantity]", parse_mode="html", reply_markup=reply_markup)

# /marvel command
def nosql_marvel(update, context):
    reply_markup = InlineKeyboardMarkup(nosqldisplayedProductkeyboard)  # to change keyboard
    query = update.callback_query
    docs = db.collection(u'Products').document(u'Category').collection(u'Marvel').stream()
    stringAppend = ""
    for doc in docs:
        toDict = doc.to_dict()
        if (toDict.get('Promo') == 0):
            stringAppend = stringAppend + "Product ID: " + str(doc.id) + "\n" + "Name: " + str(toDict.get('Name')) + "\n" + "Price: SGD$" + str('{:.2f}'.format(toDict.get('Price'))) + "\n" + "Stock: " + str(toDict.get('Stock')) + "\n\n"
        else:
            stringAppend = stringAppend + "Product ID: " + str(doc.id) + "\n" + "Name: " + str(toDict.get('Name')) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(toDict.get('Price')))]) + "\u0336 SGD$" + str('{:.2f}'.format(toDict.get('Price') * (1 - (toDict.get('Promo') / 100)))) + "\n" + "Stock: " + str(toDict.get('Stock')) + "\n\n"
        #print(f'{doc.id} => {doc.to_dict()}')

    query.edit_message_text("<b>NoSQL Marvel Product</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/nosql_tocart [Product ID] [Quantity]", parse_mode="html", reply_markup=reply_markup)

# /frozen command
def nosql_frozen(update, context):
    reply_markup = InlineKeyboardMarkup(nosqldisplayedProductkeyboard)  # to change keyboard
    query = update.callback_query
    docs = db.collection(u'Products').document(u'Category').collection(u'Frozen').stream()
    stringAppend = ""
    for doc in docs:
        toDict = doc.to_dict()
        if (toDict.get('Promo') == 0):
            stringAppend = stringAppend + "Product ID: " + str(doc.id) + "\n" + "Name: " + str(toDict.get('Name')) + "\n" + "Price: SGD$" + str('{:.2f}'.format(toDict.get('Price'))) + "\n" + "Stock: " + str(toDict.get('Stock')) + "\n\n"
        else:
            stringAppend = stringAppend + "Product ID: " + str(doc.id) + "\n" + "Name: " + str(toDict.get('Name')) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(toDict.get('Price')))]) + "\u0336 SGD$" + str('{:.2f}'.format(toDict.get('Price') * (1 - (toDict.get('Promo') / 100)))) + "\n" + "Stock: " + str(toDict.get('Stock')) + "\n\n"
        #print(f'{doc.id} => {doc.to_dict()}')

    query.edit_message_text("<b>NoSQL Frozen Product</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/nosql_tocart [Product ID] [Quantity]", parse_mode="html", reply_markup=reply_markup)