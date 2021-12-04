import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from firestoredb import db, firestore

# Delete inline keyboard options
nosqldeletekeyboard = [
    [
        InlineKeyboardButton("Main Menu", callback_data='nosqlmainmenu'),
        InlineKeyboardButton("Cart", callback_data='nosqlcart'),
    ],
    [
        InlineKeyboardButton("Products", callback_data='nosqlproduct'),
    ],
]

# /nosql_tocart command - Add Product to Cart
def nosql_delete(update, context):

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(nosqldeletekeyboard)
    counter = 0
    # Check given argument if correct syntax
    if (len(context.args) != 2):
        update.message.reply_text("Invalid commands!" + "\n" + "Syntax: /nosql_delete [Product ID] [Quantity]")
    else:
        chatid = update.message.chat.id
        docs = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').stream()
        for doc in docs:
            toDict = doc.to_dict()
            counter = counter + 1
        # Check if got cart or not cart
        # != 0 means got cart
        print("toDict: ", toDict)
        if counter != 0:
            productList = []
            # Check if cart got any product
            anyProduct = toDict.get('Product')
            print("anyProduct: ", type(anyProduct))
            print("toDict.Products: ",  toDict["Product"][0]["Quantity"])

            # If got product
            if anyProduct is not None:
                for a in anyProduct:
                    if int(a.get('ProductID')) == int(context.args[0]):
                        if int(context.args[1]) == 0:
                            update.message.reply_text("Unable to delete\, you requested to remove 0 quantity" + "\n\n" +
                                            "You may want to check the quantity", parse_mode='MarkdownV2', reply_markup=reply_markup)
                        elif int(context.args[1]) < 0:
                            update.message.reply_text("Unable to delete\, you requested to remove negative quantity" + "\n\n" +
                                            "You may want to check the quantity", parse_mode='MarkdownV2', reply_markup=reply_markup)
                        elif int(a.get('Quantity')) < int(context.args[1]):
                            update.message.reply_text("You are trying to remove more quantity then what you have in cart" + "\n\n" +
                                            "You may want to check the quantity", parse_mode='MarkdownV2', reply_markup=reply_markup)
                        elif int(a.get('Quantity')) == int(context.args[1]):
                            print("[0]:", context.args[0])
                            print("[1]:", context.args[1])
                            doc_ref = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').document(str(doc.id))
                            doc_ref.update({
                                u'Product': firestore.ArrayRemove([
                                    {
                                    u'ProductID' : str(context.args[0]),
                                    u'Quantity': str(int(a.get('Quantity')))
                                    }
                                ])
                            })

                            # for n in anyProduct:
                            #     print("N: ", n)
                            #     if int(n.get("ProductID")) == int(context.args[0]):
                            #         n.pop("ProductID", context.args[0])
                            #         n.pop("Quantity", context.args[1])
                            # print("anyProduct: ", anyProduct)
                        elif int(a.get('Quantity')) > int(context.args[1]):
                            doc_ref = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').document(str(doc.id))
                            updatedInt = int(a.get('Quantity')) - int(context.args[1])
                            for x in anyProduct:
                                if int(x.get("ProductID")) == int(context.args[0]):
                                    update = {"Quantity" : updatedInt }
                                    x.update(update)
                            field_updates = {"Product": anyProduct}
                            doc_ref.update(field_updates)