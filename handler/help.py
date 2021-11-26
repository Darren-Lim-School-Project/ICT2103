import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

helpkeyboard = [
    [
        InlineKeyboardButton("Profile", callback_data='profile'),
        InlineKeyboardButton("Product", callback_data='product'),
    ],
    [
        InlineKeyboardButton("Cart", callback_data='cart'),
        InlineKeyboardButton("Checkout", callback_data='checkout'),
    ], [
        InlineKeyboardButton("Promo", callback_data='promo')
    ],
]

# /help command 
def help(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(helpkeyboard)

    query.edit_message_text("*Help:*" + "\n" +
                            "Product     \- View available products " + "\n" +
                            "Cart        \- View shopping cart" + "\n" +
                            "Checkout    \- Cart checkout" + "\n" +
                            "Profile     \- User profile" + "\n" +
                            "Promo       \- View promotional item" + "\n\n" +
                            "If you require additional assistance, you can contact us at @darrennnnnlim, @kendricklee or @yongkhengs\!", parse_mode='MarkdownV2', reply_markup=reply_markup)