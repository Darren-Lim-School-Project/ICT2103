import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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

    query.edit_message_text("*Product Menu:*" + "\n" +
                            "Mickey Mouse and Friends   \- View Mickey Mouse and Friends Category " + "\n" + 
                            "Disney and Pixar           \- View Disney and Pixar Category " + "\n" +
                            "Marvel                     \- View Marvel Category " + "\n" +
                            "Frozen                     \- View Frozen Category " + "\n\n" +
                            "Please select a category to view the product inside\.", parse_mode='MarkdownV2', reply_markup=reply_markup)

# /mickeymouse command
def nosql_mickeymouse(update, context):
    
    reply_markup = InlineKeyboardMarkup(nosqldisplayedProductkeyboard)  # to change keyboard
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    
    query = update.callback_query
    cur.execute("SELECT productID, productName, productPrice, promotion, inStock FROM Products WHERE category = 'Mickey Mouse and Friends'")
    
    data = cur.fetchall()
    stringAppend = ""

    for i in data:
        if i[3] == 0:
            print("1")
            stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: SGD$" + str('{:.2f}'.format(i[2])) + "\n" + "Stock: " + str(i[4]) + "\n\n"
        else:
            print("2")
            stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(i[2]))]) + "\u0336 SGD$" + str('{:.2f}'.format(i[2] * (1 - (i[3] / 100)))) + "\n" + "Stock: " + str(i[4]) + "\n\n"


    print(stringAppend)
    query.edit_message_text("<b>Mickey Mouse Product</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/nosql_tocart [Product ID] [Quantity]", parse_mode="html", reply_markup=reply_markup)
    con.close()

# /disney and pixar command
def nosql_disneyAndPixar(update, context):
    
    reply_markup = InlineKeyboardMarkup(nosqldisplayedProductkeyboard)  # to change keyboard
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    
    query = update.callback_query
    cur.execute("SELECT productID, productName, productPrice, promotion, inStock FROM Products WHERE category = 'Disney and Pixar'")
    
    data = cur.fetchall()
    stringAppend = ""

    for i in data:
        if i[3] == 0:
            print("1")
            stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: SGD$" + str('{:.2f}'.format(i[2])) + "\n" + "Stock: " + str(i[4]) + "\n\n"
        else:
            print("2")
            stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(i[2]))]) + "\u0336 SGD$" + str('{:.2f}'.format(i[2] * (1 - (i[3] / 100)))) + "\n" + "Stock: " + str(i[4]) + "\n\n"


    print(stringAppend)
    query.edit_message_text("<b>Disney and Pixar Product</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/nosql_tocart [Product ID] [Quantity]", parse_mode="html", reply_markup=reply_markup)
    con.close()

# /marvel command
def nosql_marvel(update, context):
    
    reply_markup = InlineKeyboardMarkup(nosqldisplayedProductkeyboard)  # to change keyboard
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    
    query = update.callback_query
    cur.execute("SELECT productID, productName, productPrice, promotion, inStock FROM Products WHERE category = 'Marvel'")
    
    data = cur.fetchall()
    stringAppend = ""

    for i in data:
        if i[3] == 0:
            print("1")
            stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: SGD$" + str('{:.2f}'.format(i[2])) + "\n" + "Stock: " + str(i[4]) + "\n\n"
        else:
            print("2")
            stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(i[2]))]) + "\u0336 SGD$" + str('{:.2f}'.format(i[2] * (1 - (i[3] / 100)))) + "\n" + "Stock: " + str(i[4]) + "\n\n"


    print(stringAppend)
    query.edit_message_text("<b>Marvel Product</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/nosql_tocart [Product ID] [Quantity]", parse_mode="html", reply_markup=reply_markup)
    con.close()

# /frozen command
def nosql_frozen(update, context):
    
    reply_markup = InlineKeyboardMarkup(nosqldisplayedProductkeyboard)  # to change keyboard
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    
    query = update.callback_query
    cur.execute("SELECT productID, productName, productPrice, promotion, inStock FROM Products WHERE category = 'Frozen'")
    
    data = cur.fetchall()
    stringAppend = ""

    for i in data:
        if i[3] == 0:
            print("1")
            stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: SGD$" + str('{:.2f}'.format(i[2])) + "\n" + "Stock: " + str(i[4]) + "\n\n"
        else:
            print("2")
            stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(i[2]))]) + "\u0336 SGD$" + str('{:.2f}'.format(i[2] * (1 - (i[3] / 100)))) + "\n" + "Stock: " + str(i[4]) + "\n\n"


    print(stringAppend)
    query.edit_message_text("<b>Frozen Product</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/nosql_tocart [Product ID] [Quantity]", parse_mode="html", reply_markup=reply_markup)
    con.close()