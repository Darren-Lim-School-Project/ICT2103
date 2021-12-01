import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

nosqlhelpkeyboard = [
    [
        InlineKeyboardButton("Profile", callback_data='nosqlprofile'),
        InlineKeyboardButton("Product", callback_data='nosqlproduct'),
    ],
    [
        InlineKeyboardButton("Cart", callback_data='nosqlcart'),
        InlineKeyboardButton("Checkout", callback_data='nosqlcheckout'),
    ], [
        InlineKeyboardButton("Promo", callback_data='nosqlpromo')
    ],
]

# /help command 
def nosql_help(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(nosqlhelpkeyboard)

    query.edit_message_text("*Help:*" + "\n" +
                            "Product     \- View available products " + "\n" +
                            "Cart        \- View shopping cart" + "\n" +
                            "Checkout    \- Cart checkout" + "\n" +
                            "Profile     \- User profile" + "\n" +
                            "Promo       \- View promotional item" + "\n\n" +
                            "If you require additional assistance, you can contact us at @darrennnnnlim, @kendricklee or @yongkhengs\!", parse_mode='MarkdownV2', reply_markup=reply_markup)
