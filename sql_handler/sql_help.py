import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

sqlhelpkeyboard = [
    [
        InlineKeyboardButton("Profile", callback_data='sqlprofile'),
        InlineKeyboardButton("Product", callback_data='sqlproduct'),
    ],
    [
        InlineKeyboardButton("Cart", callback_data='sqlcart'),
        InlineKeyboardButton("Checkout", callback_data='sqlcheckout'),
    ], [
        InlineKeyboardButton("Promo", callback_data='sqlpromo')
    ],
]

# /help command 
def sql_help(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(sqlhelpkeyboard)

    query.edit_message_text("*Help:*" + "\n" +
                            "Product     \- View available products " + "\n" +
                            "Cart        \- View shopping cart" + "\n" +
                            "Checkout    \- Cart checkout" + "\n" +
                            "Profile     \- User profile" + "\n" +
                            "Promo       \- View promotional item" + "\n\n" +
                            "If you require additional assistance, you can contact us at @darrennnnnlim, @kendricklee or @yongkhengs\!", parse_mode='MarkdownV2', reply_markup=reply_markup)
