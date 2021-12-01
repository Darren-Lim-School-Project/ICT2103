import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3
from datetime import datetime
from firestoredb import db, firestore

nosqlbackToProduct = [
    [
        InlineKeyboardButton("Main Menu", callback_data='nosqlmainmenu'),
        InlineKeyboardButton("Back to Product", callback_data='nosqlproduct'),
    ],
]

nosqlbackToProductOrCart = [
    [
        InlineKeyboardButton("Main Menu", callback_data='nosqlmainmenu'),
        InlineKeyboardButton("Back to Product", callback_data='nosqlproduct'),
    ], [
        InlineKeyboardButton("View Cart", callback_data='nosqlcart'),
    ],
]

# /nosql_tocart command - Add Product to Cart
def nosql_tocart(update, context):
    chatid = update.message.chat.id
    toProduct = InlineKeyboardMarkup(nosqlbackToProduct)
    toProductOrCart = InlineKeyboardMarkup(nosqlbackToProductOrCart)

    # All the boolean
    incorrectProductID = True
    inactiveCart = True
    itemNotFound = True

    # Temp variable
    activeID = None

    if (len(context.args) != 2):
        update.message.reply_text("Invalid commands!" + "\n" + "Syntax: /nosql_tocart [Product ID] [Quantity]", reply_markup=toProduct)
    else:
        categoryCollections = db.collection(u'Products').document(u'Category').collections()
        for catCol in categoryCollections:
            for productID in catCol.stream():
                if (int(productID.id) == int(context.args[0]) and (int(context.args[1]) > 0)):
                    incorrectProductID = False
                    if (int(context.args[1]) < int(productID.get('Stock'))):
                        userCart = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').stream()
                        for cartDetail in userCart:
                            cartDetailToDict = cartDetail.to_dict()
                            if (cartDetailToDict.get('Status') == 'Active'):
                                inactiveCart = False
                                for loopProducts in cartDetailToDict.get('Product'):
                                    if (loopProducts.get('ProductID') == context.args[0]):
                                        itemNotFound = False
                                        totalQuantity = int(loopProducts.get('Quantity')) + int(context.args[1])
                                        if (totalQuantity > int(productID.get('Stock'))):
                                            update.message.reply_text("Product failed to add into cart\nYou currently have " + str(loopProducts.get('Quantity')) + " " + str(productID.get('Name') +
                                                                        " in your cart\nYou are only allowed to add " + str(int(productID.get('Stock')) - int(loopProducts.get('Quantity'))) + " more to your cart"), reply_markup=toProduct)
                                            return
                                        else:
                                            doc_ref = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').document(str(cartDetail.id))
                                            doc_ref.update({
                                                u'Product': firestore.ArrayUnion([
                                                    {
                                                    u'ProductID' : str(context.args[0]),
                                                    u'Quantity': str(int(loopProducts.get('Quantity')) + int(context.args[1]))
                                                    }
                                                ])
                                            })
                                            doc_ref.update({
                                                u'Product': firestore.ArrayRemove([
                                                    {
                                                    u'ProductID' : str(context.args[0]),
                                                    u'Quantity': str(int(loopProducts.get('Quantity')))
                                                    }
                                                ])
                                            })

                                if (itemNotFound == True):
                                    doc_ref = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').document(str(cartDetail.id))
                                    doc_ref.update({
                                        u'Product': firestore.ArrayUnion([
                                            {
                                            u'ProductID' : str(context.args[0]),
                                            u'Quantity': str(context.args[1])
                                            }
                                        ])
                                    })

                        if (inactiveCart == True):
                            lengthOfCarts = len(list(db.collection(u'Customers').document(str(chatid)).collection(u'Carts').get()))
                            doc_ref = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').document(str(lengthOfCarts + 1))
                            doc_ref.set({
                                u'Product' : [
                                    {
                                        u'ProductID' : str(context.args[0]),
                                        u'Quantity': str(context.args[1])
                                    },
                                ],
                                u'Status' : 'Active'
                            })
                    else:
                        update.message.reply_text("Quantity must be lower than in stock", reply_markup=toProduct)
                        return

    if (incorrectProductID == True):
        update.message.reply_text("Incorrect Product ID or Quantity must be more than 0", reply_markup=toProduct)