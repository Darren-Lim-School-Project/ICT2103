import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

# Import of SQLite 3
import sqlite3

cartkeyboard = [
    [
        InlineKeyboardButton("Main Menu", callback_data='back'),
        InlineKeyboardButton("Checkout", callback_data='checkout'),
    ],
]

# Show Cart
def cart(update, context):
    global totalAmount
    totalAmount = 0
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(cartkeyboard)

    # TODO Update customerID when ready
    cur.execute("SELECT cartID from Shopping_Cart WHERE customerID=1 ORDER BY cartID DESC")
    data = cur.fetchone()
    if (data is not None):
        # A shopping cart exists
        # Check if the shopping cart is completed or abandoned
        cur.execute("SELECT cc.cartID, ac.cartID FROM Completed_Cart cc, Abandoned_Cart ac WHERE cc.cartID=" + str(data[0]) + " OR ac.cartID = " + str(data[0]))
        ccac = cur.fetchall()
        if (int(len(ccac)) > 0):
            # A shopping cart was either completed or abandoned
            # So technically cart is new and empty
            query.edit_message_text("*Cart:*" + "\n" +
                            "You have no items in your cart\." + "\n" +
                            "You may want to view products using /products", parse_mode='MarkdownV2', reply_markup=reply_markup)
        else:
            # Shopping exists, but was not completed or abandoned
            cur.execute("SELECT * FROM Cart_Contents WHERE cartID=" + str(data[0]))
            cartItem = cur.fetchall()
            #Check if shopping cart is empty
            if (len(cartItem) == 0):
                # Shopping cart empty
                query.edit_message_text("*Cart:*" + "\n" +
                            "You have no items in your cart\." + "\n" +
                            "You may want to view products using /products", parse_mode='MarkdownV2', reply_markup=reply_markup)
            else:
                # Shopping Cart not Empty
                # Get the productID based on cartID to be able to retrieve product details
                cur.execute("SELECT productID, quantity FROM Cart_Contents WHERE cartID=" + str(data[0]))
                cartProductID = cur.fetchall()
                # Create a list to store all the productIDs of the items in cart
                productIDs = []
                for i in cartProductID:
                    if len(i) > 0:
                        productIDs.append(i[0])
                # Use variable stringAppend to append product details which is needed to display later
                stringAppend = ''
                for i in productIDs:
                    # SQL statement to get products details based on productID
                    cur.execute("SELECT productID, productName, productPrice, promotion FROM Products WHERE productID=" + str(i))
                    productData = cur.fetchone()
                    # Get quantity of each item in shopping cart
                    cur.execute("SELECT * FROM Cart_Contents WHERE productID=" + str(i) + " AND cartID=" + str(data[0]))
                    quantityData = cur.fetchone()
                    # Check if item is on promo. If not on promo, run the IF statement. If on promo, run the ELSE statement
                    if productData[3] == 0:
                        stringAppend = stringAppend + "Product ID: " + str(productData[0]) + "\n" + "Name: " + str(productData[1]) + "\n" + "Price: SGD$" + str('{:.2f}'.format(float(productData[2]))) + "\n" + "Quantity: " + str(quantityData[2]) + "\n\n"
                        totalAmount = totalAmount + (float(productData[2]) * quantityData[2])
                    else:
                        stringAppend = stringAppend + "Product ID: " + str(productData[0]) + "\n" + "Name: " + str(productData[1]) + "\n" + "Price: S\u0336G\u0336D\u0336$\u0336" + ''.join([u'\u0336{}'.format(c) for c in str('{:.2f}'.format(productData[2]))]) + "\u0336 " + " SGD$" + str('{:.2f}'.format(productData[2] * (1 - (productData[3] / 100)))) + "\n" + "Quantity: " + str(quantityData[2]) +"\n\n"
                        totalAmount = totalAmount + (productData[2] * (1 - (productData[3] / 100)) * quantityData[2])
                
                # Print out the text needed including the products
                query.edit_message_text("<b>Cart</b>" + "\n\n" +
                                        stringAppend + "" +
                                        "Total Payable: <b>" + str('{:.2f}'.format(totalAmount)) + "</b>\n\n"
                                        "To delete an item from cart, use" + "\n" + "/delete [Product ID] [Quantity]" + "\n"
                                        "example: /delete 1 2", parse_mode="html", reply_markup=reply_markup)
                # Close DB connection as no longer needed
                con.close()
    else:
        # A shopping cart does not exist
        # Does not exist so technically need to prompt them to add products to create new cart
        # So technically cart is empty
        query.edit_message_text("*Cart:*" + "\n" +
                            "You have no items in your cart\." + "\n" +
                            "You may want to view products using /products", parse_mode='MarkdownV2', reply_markup=reply_markup)

def getTotalAmount():
    return totalAmount
