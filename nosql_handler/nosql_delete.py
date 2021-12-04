import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from firestoredb import db

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
            print("anyProduct: ", anyProduct)
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
                            print("Remove item from cart")
                        elif int(a.get('Quantity')) > int(context.args[1]):
                            doc_ref = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').document(u'1')
                            # for doc_refs in doc_ref:
                            #     updateDict = doc_refs.to_dict()
                            updatedInt = int(a.get('Quantity')) - int(context.args[1])
                            for x in anyProduct:
                                if int(x.get("ProductID")) == int(context.args[0]):
                                    # x['Quantity'] == updatedInt 
                                    field_updates = {"Quantity":updatedInt}
                                    doc_ref.update(field_updates)

            # If no product
        #     else:
        #         query.edit_message_text("*Cart:*" + "\n" +
        #                         "You have no items in your cart\." + "\n" +
        #                         "Click on the 'Products' Button to browse products\!", parse_mode='MarkdownV2', reply_markup=reply_markup)
        # else:
        #     query.edit_message_text("*Cart:*" + "\n" +
        #                         "You have no items in your cart\." + "\n" +
        #                         "Click on the 'Products' Button to browse products\!", parse_mode='MarkdownV2', reply_markup=reply_markup)