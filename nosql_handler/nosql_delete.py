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
        productList = []
        chatid = update.message.chat.id
        docs = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').stream()
        for doc in docs:
            toDict = doc.to_dict()
            counter = counter + 1
        # Check if got cart or not cart
        # != 0 means got cart
        if counter != 0:
            productList = []
            # Check if cart got any product
            anyProduct = toDict.get('Product')

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
                            doc_ref = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').document(str(doc.id))
                            doc_ref.update({
                                u'Product': firestore.ArrayRemove([
                                    {
                                    u'ProductID' : str(context.args[0]),
                                    u'Quantity': str(int(a.get('Quantity')))
                                    }
                                ])
                            })
                        # Store all productID from cart to an array
                            for x in productList:
                                productListProductid = x.get('Productid')
                                if int(productListProductid) == int(context.args[0]):
                                    update.message.reply_text("Removed " + str(context.args[1]) + " " + str(x.get('Name')) + " from shopping cart", reply_markup=reply_markup)

                        elif int(a.get('Quantity')) > int(context.args[1]):
                            doc_ref = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').document(str(doc.id))
                            updatedInt = int(a.get('Quantity')) - int(context.args[1])
                            for x in anyProduct:
                                if int(x.get("ProductID")) == int(context.args[0]):
                                    updateQuantity = {"Quantity" : updatedInt }
                                    x.update(updateQuantity)
                            field_updates = {"Product": anyProduct}
                            doc_ref.update(field_updates)
                            
                            docs = db.collection(u'Products').document(u'Category').collections()
                            for doc in docs:
                                for i in doc.stream():
                                    productList.append(i.to_dict())
                            # Store all productID from cart to an array
                            for p in productList:
                                if int(p.get('Productid')) == int(context.args[0]):
                                    productName = p.get('Name')
                                    quantity = context.args[1]
                            update.message.reply_text("Removed " + str(quantity) + " " + str(productName) + " from shopping cart", reply_markup=reply_markup)