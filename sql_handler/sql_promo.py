import telegram

# Import of SQLite 3
import sqlite3

# Show current Promo items
def sql_promo(update, context):
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()
    
    query = update.callback_query
    cur.execute("SELECT productID, productName, productPrice, promotion, inStock FROM Products WHERE promotion>0")
    print("1")
    data = cur.fetchall()
    print("2")
    stringAppend = ""

    print(str(data))

    for i in data:
        stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(i[2]))]) + "\u0336 SGD$" + str(i[2] * (1 - (i[3] / 100))) + "\n" + "Stock: " + str(i[4]) + "\n\n"
        #stringAppend = stringAppend + "Product ID: " + str(i[0]) + "\n" + "Name: " + str(i[1]) + "\n" + "Price: SGD$" + str(i[2]) + " SGD$" + str(i[2] * (1 - (i[3] / 100))) + "\n" + "Stock: " + str(i[4]) + "\n\n"
            
    query.edit_message_text("<b>Promotion</b>" + "\n\n" +
                            stringAppend + "\n" +
                            "To add an item to cart, use" + "\n" + "/sql_tocart [Product ID] [Quantity]", parse_mode="html")
    con.close()