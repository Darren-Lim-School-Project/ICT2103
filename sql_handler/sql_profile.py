import telegram
import sqlite3
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

sqlprofilekeyboard = [
    [
        InlineKeyboardButton("Update Email Address", callback_data='sqlemail'),
        InlineKeyboardButton("Cart", callback_data='sqlcart'),
    ], [
        InlineKeyboardButton("Product", callback_data='sqlproduct'),
        InlineKeyboardButton("Promo", callback_data='sqlpromo'),
    ], [
        InlineKeyboardButton("Help", callback_data='sqlhelp')
    ],
]

# /profile command
def sql_profile(update, context, chatid, username):
    query = update.callback_query
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    user_object = cur.execute(f"SELECT * FROM Customers WHERE chatID = {chatid}")
    con.commit()
    for i in user_object:
        fname = i[2]
        lname = i[3]
        email = i[4]
    if email is None:
        email = "None"
    telegramname = username
    reply_markup = InlineKeyboardMarkup(sqlprofilekeyboard) # to change keyboard

    query.edit_message_text("*Profile:*" + "\n" +
                              "We will contact you through email if you cannot be reached on Telegram\." + "\n\n" +
                              "This is the information we have from you:" + "\n\n" +
                              "First name: __" + fname + "__\n" +
                              "Last name: __" + lname + "__\n" +
                              "Telegram username: __@"+ username + "__\n" +
                              "Email: __" + email + "__\n\n", parse_mode='MarkdownV2', reply_markup=reply_markup)  
                            

# Get Key ID (Drawing) from reply
def sql_received_email(update, context, chatid):
    global STATE
    print("In sql_received_email")
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    new_string = ""
    temp_array = []
    counter = 0
    temp_array_to_insert = []
    reply_markup = InlineKeyboardMarkup(sqlhelpkeyboard)
    email = "'" + str(update.message.text) + "'"
    for i in email:
        temp_array.append(i)
    for i,j in enumerate(temp_array):
        if j == "@" or j == ".":
            temp_array_to_insert.append(int(i))
            continue
    for i in range(0, len(temp_array_to_insert), 1):
        temp_array.insert(temp_array_to_insert[i] + counter, "\\")
        counter += 1
    for i in temp_array:
        new_string+= i

    cur.execute(f"UPDATE Customers SET email = {new_string} WHERE chatID = {chatid}")
    con.commit()
    update.message.reply_text("*Updated Email*" + "\n" +
                              "Your email has been updated to the following:" + "\n" +
                              "Email: __" + str(new_string) + "__\n\n", parse_mode='MarkdownV2', reply_markup=reply_markup)