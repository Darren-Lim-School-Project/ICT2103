import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3
from datetime import datetime

sqlbackToProduct = [
    [
        InlineKeyboardButton("Main Menu", callback_data='sqlmainmenu'),
        InlineKeyboardButton("Back to Product", callback_data='sqlproduct'),
    ],
]

sqlbackToProductOrCart = [
    [
        InlineKeyboardButton("Main Menu", callback_data='sqlmainmenu'),
        InlineKeyboardButton("Back to Product", callback_data='sqlproduct'),
    ], [
        InlineKeyboardButton("View Cart", callback_data='sqlcart'),
    ],
]

# /sql_tocart command - Add Product to Cart
def sql_tocart(update, context):
    toProduct = InlineKeyboardMarkup(sqlbackToProduct)
    toProductOrCart = InlineKeyboardMarkup(sqlbackToProductOrCart)
    if (len(context.args) != 2):
        update.message.reply_text("Invalid commands!" + "\n" + "Syntax: /sql_tocart [Product ID] [Quantity]", reply_markup=toProduct)
    else:
        # Setup connection to "ICT2103_Group32.db"
        con = sqlite3.connect('ICT2103_Group32.db')
        cur = con.cursor()
        cur.execute("SELECT productID, inStock, productPrice, promotion, productName from Products WHERE productID=" + context.args[0])
        productInfo = cur.fetchall()
        if ((len(productInfo) == 1) and (int(context.args[1]) > 0)):
            # Product exists in the database
            quantityAmount = ((productInfo[0][2] * (1 - (productInfo[0][3] / 100))) * int(context.args[1]))

            if ((int(context.args[1]) > 0) and (int(context.args[1]) <= int(productInfo[0][1]))):
                # Add the product to cart - SQL
                # Need to change customerID=1 to global variable for stored customer ID
                shoppingCartID = 0
                cur.execute("SELECT cartID from Shopping_Cart WHERE customerID=1 ORDER BY cartID DESC")
                data = cur.fetchone()

                if (data is not None):
                    # A shopping cart exists
                    # Check if the shopping cart is completed or abandoned
                    cur.execute("SELECT cartID FROM Completed_Cart WHERE cartID=" + str(data[0]))
                    cc = cur.fetchall()

                    if (int(len(cc)) > 0):
                        # A shopping cart was either completed or abandoned
                        # Need to change customerID to global variable for stored customer ID
                        cur.execute("INSERT INTO Shopping_Cart (customerID, amount, creationDate) VALUES (1," + str(quantityAmount) + "," + datetime.now().strftime("%Y-%d-%m %H:%M:%S") + ")")
                        cur.execute("INSERT INTO Cart_Contents VALUES ((SELECT TOP 1 cartID FROM Shopping_Cart WHERE customerID=1 ORDER BY cartID desc)," + str(productInfo[0][0]) + "," + context.args[1] + ")")
                        con.commit()
                    else:
                        # Shopping exists, but was not completed
                        cur.execute("SELECT quantity FROM Cart_Contents WHERE cartID=" + str(data[0]) + " AND productID=" + str(productInfo[0][0]))
                        itemExist = cur.fetchone()

                        if (itemExist is not None):
                            # Item already existed in the Shopping Cart
                            if ((itemExist[0] + int(context.args[1])) > productInfo[0][1]):
                                update.message.reply_text("Product failed to add into cart\nYou currently have " + str(itemExist[0]) + " " + str(productInfo[0][4]) + 
                                                            " in your cart\nYou are only allowed to add " + str(int(context.args[1]) - itemExist[0]) + " more to your cart", reply_markup=toProduct)
                                con.close()
                                return
                            else:
                                cur.execute("UPDATE Cart_Contents SET quantity=" + str(itemExist[0] + int(context.args[1])) + " WHERE cartID=" + str(data[0]) + " AND productID=" + str(productInfo[0][0]))
                                con.commit()
                        else:
                            # Item did not exist in the Shopping Cart
                            cur.execute("INSERT INTO Cart_Contents VALUES (" + str(data[0]) + "," + str(productInfo[0][0]) + "," + context.args[1] + ")")
                            cur.execute("UPDATE Shopping_Cart SET amount=((SELECT amount FROM Shopping_Cart WHERE cartID=" + str(data[0]) + ") + " + str(quantityAmount) + ")")
                            con.commit()
                else:
                    # A shopping cart does not exist
                    # Create new record of Shopping_Cart and Cart_Contents
                    datetimeNow = str(datetime.now().strftime("%Y-%d-%m %H:%M:%S"))
                    #stringAppend = "INSERT INTO Shopping_Cart (customerID, amount, creationDate) VALUES ('1'," + str(quantityAmount) + ",'" + str(datetime.now().strftime("%Y-%d-%m %H:%M:%S")) + "')"
                    cur.execute("INSERT INTO Shopping_Cart (customerID, amount, creationDate) VALUES (1," + str(quantityAmount) + ",'" + datetimeNow + "')")
                    cur.execute("SELECT cartID FROM Shopping_Cart WHERE customerID=1 ORDER BY cartID desc")
                    lastCartID = cur.fetchone()
                    cur.execute("INSERT INTO Cart_Contents VALUES (" + str(lastCartID[0]) + "," + str(productInfo[0][0]) + "," + context.args[1] + ")")
                    con.commit()
            else:
                update.message.reply_text("Quantity must be lower than in stock", reply_markup=toProduct)
                con.close()
                return
        else:
            update.message.reply_text("Incorrect Product ID or Quantity must be more than 0", reply_markup=toProduct)
            con.close()
            return
        update.message.reply_text(str(productInfo[0][4]) + " has been added to the shopping cart", reply_markup=toProductOrCart)
        con.close()
    
