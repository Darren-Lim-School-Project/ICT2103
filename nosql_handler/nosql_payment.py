import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from firestoredb import db, firestore

nosqlbackToMainMenu = [
    [
        InlineKeyboardButton("Main Menu", callback_data='nosqlmainmenu'),
    ],
]

# /help command 
def nosql_payment(update, context):
    chatid = update.message.chat.id
    reply_markup = InlineKeyboardMarkup(nosqlbackToMainMenu)
    activeCartExist = False

    if (len(context.args) != 2):
        update.message.reply_text("Invalid commands!" + "\n" + "Syntax: /nosql_payment [Delivery Postal Code] [Delivery Unit Number]", reply_markup=reply_markup)
    else:
        userCart = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').stream()
        for cartDetail in userCart:
            cartDetailToDict = cartDetail.to_dict()
            if (cartDetailToDict.get('Status') == 'Active'):
                activeCartExist = True
                doc_ref = db.collection(u'Customers').document(str(chatid)).collection(u'Carts').document(str(cartDetail.id))
                deliveryInfo = [{"PostalCode":context.args[0], "UnitNumber":context.args[1]}]
                doc_ref.update({
                    u"DeliveryInfo": deliveryInfo,
                    u"Status": "Completed"
                })
                update.message.reply_text("<b>NoSQL Payment</b>" + "\n\n" + "Thank you for shopping with us at MulungShop!\nYou will receive your delivery in 3 days time.", parse_mode="html", reply_markup=reply_markup)
                return
    
    if activeCartExist == False:
        update.message.reply_text("<b>NoSQL Error</b>" + "\n\n" + "No active cart found. Please add items to your cart.", parse_mode="html", reply_markup=reply_markup)