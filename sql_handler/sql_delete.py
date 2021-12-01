import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

# Delete inline keyboard options
sqldeletekeyboard = [
    [
        InlineKeyboardButton("Main Menu", callback_data='sqlmainmenu'),
        InlineKeyboardButton("Cart", callback_data='sqlcart'),
    ],
    [
        InlineKeyboardButton("Products", callback_data='sqlproduct'),
    ],
]

# /sql_tocart command - Add Product to Cart
def sql_delete(update, context):

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(sqldeletekeyboard)
    # Check given argument if correct syntax
    if (len(context.args) != 2):
        update.message.reply_text("Invalid commands!" + "\n" + "Syntax: /sql_delete [Product ID] [Quantity]")
    else:
        # Setup connection to "ICT2103_Group32.db"
        con = sqlite3.connect('ICT2103_Group32.db')
        cur = con.cursor()
        # TODO Update customerID when ready
        cur.execute("SELECT cartID from Shopping_Cart WHERE customerID=1 ORDER BY cartID DESC")
        data = cur.fetchone()
        if (data is not None):
            # A shopping cart exists
            # Check if the shopping cart is completed or abandoned
            cur.execute("SELECT cartID FROM Completed_Cart WHERE cartID=" + str(data[0]))
            ccac = cur.fetchall()
            if (int(len(ccac)) > 0):
                # A shopping cart was either completed or abandoned
                # So technically cart is new and empty
                update.message.reply_text("You have no items in your cart\, no products to remove" + "\n\n" +
                            "Click on the 'Products' Button to browse products\!", parse_mode='MarkdownV2', reply_markup=reply_markup)
            else:
                # Shopping cart exist and not completed or abandoned
                # Getting cart contents based on cartID
                cur.execute("SELECT * FROM Cart_Contents WHERE cartID=" + str(data[0]))
                cartItem = cur.fetchall()
                print("cartItem ", cartItem)
                print("Length cartItem ", len(cartItem))
                #Check if shopping cart is empty
                if (len(cartItem) == 0):
                    # Shopping cart empty
                    update.message.reply_text("You have no items in your cart\, no products to remove" + "\n\n" +
                            "Click on the 'Products' Button to browse products\!", parse_mode='MarkdownV2', reply_markup=reply_markup)
                else:
                    # need check if argument productID is in cart
                    counter = 0
                    for i in cartItem:
                        if str(context.args[0]) == str(i[1]):
                            counter = counter + 1
                        else:
                            counter = counter
                    # productID exist in cart
                    if counter > 0:
                        # Shopping cart not empty so continue to delete item
                        cur.execute("SELECT quantity FROM Cart_Contents WHERE cartID=" + str(data[0]) + " AND productID=" + str(context.args[0]))
                        totalQuantityInCart = cur.fetchone()
                        totalQuantity = totalQuantityInCart[0]
                        argumentQuantity = int(context.args[1])
                        # If keyed in to remove 0
                        if argumentQuantity == 0:
                            update.message.reply_text("Unable to delete\, you requested to remove 0 quantity" + "\n\n" +
                                            "You may want to check the quantity", parse_mode='MarkdownV2', reply_markup=reply_markup)
                        # Check if trying to remove negative quantity
                        elif argumentQuantity < 0:
                            update.message.reply_text("Unable to delete\, you requested to remove negative quantity" + "\n\n" +
                                            "You may want to check the quantity", parse_mode='MarkdownV2', reply_markup=reply_markup)
                        # Check if trying to remove more than quantity in cart
                        elif argumentQuantity > totalQuantity:
                            update.message.reply_text("You are trying to remove more quantity then what you have in cart" + "\n\n" +
                                            "You may want to check the quantity", parse_mode='MarkdownV2', reply_markup=reply_markup)
                        # Check if trying to remove lesser then quantity in cart
                        elif argumentQuantity < totalQuantity:
                            leftover = totalQuantity - argumentQuantity
                            print("leftover", leftover)
                            print("cartID ", str(data[0]))
                            print("productID ", str(context.args[0]))
                            cur.execute("UPDATE Cart_Contents SET quantity=" + str(leftover) + " WHERE cartID=" + str(data[0]) + " AND productID=" + str(context.args[0]))
                            cur.execute("SELECT productName FROM Products WHERE productID=" + str(context.args[0]))
                            productNameData = cur.fetchone()
                            productName = productNameData[0]
                            con.commit()
                            update.message.reply_text("Removed " + str(argumentQuantity) + " " + str(productName) + " from shopping cart", reply_markup=reply_markup)
                            con.close()
                        # Check if planning to remove all quantity
                        elif argumentQuantity == totalQuantity:
                            cur.execute("DELETE FROM Cart_Contents WHERE cartID=" + str(data[0]) + " AND productID=" + str(context.args[0]))
                            cur.execute("SELECT productName FROM Products WHERE productID=" + str(context.args[0]))
                            productNameData = cur.fetchone()
                            productName = productNameData[0]
                            con.commit()
                            update.message.reply_text("Removed " + str(argumentQuantity) + " " + str(productName) + " from shopping cart", reply_markup=reply_markup)
                            con.close()
                    else:
                        update.message.reply_text("You keyed in a product ID that does not exist in your cart" + "\n\n" +
                                "You may want to check your command", parse_mode='MarkdownV2', reply_markup=reply_markup)
        else:
            # Shopping cart don't exist
            # A shopping cart don't exist
            # So technically cart is new and empty
            update.message.reply_text("You have no items in your cart\, no products to remove" + "\n\n" +
                        "Click on the 'Products' Button to browse products\!", parse_mode='MarkdownV2', reply_markup=reply_markup)