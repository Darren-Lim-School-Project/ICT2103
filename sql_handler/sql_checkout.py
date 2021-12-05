import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Import of SQLite 3
import sqlite3

sqlcheckoutkeyboard = [
    [
        InlineKeyboardButton("Back", callback_data='sqlcart'),
        InlineKeyboardButton("Products", callback_data='sqlproduct'),
    ],
]
sqlcheckoutkeyboard2 = [
    [
        InlineKeyboardButton("Cart", callback_data='sqlcart'),
        InlineKeyboardButton("Product", callback_data='sqlproduct'),
    ],
]

# Checkout Cart
def sql_checkout(update, context, totalAmount, cartID):
    # Setup connection to "ICT2103_Group32.db"
    con = sqlite3.connect('ICT2103_Group32.db')
    cur = con.cursor()

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(sqlcheckoutkeyboard)
    reply_markup2 = InlineKeyboardMarkup(sqlcheckoutkeyboard2)

    if totalAmount == 0:
        # A shopping cart does not exist
        # Does not exist so technically need to prompt them to add products to create new cart
        # So technically cart is empty
        query.edit_message_text("*SQL Checkout:*" + "\n" +
                            "You have no items in your cart\." + "\n" +
                            "There is no items to make payment\." + "\n" +
                            "Click on the 'Products' Button to browse products\!", parse_mode='MarkdownV2', reply_markup=reply_markup)
            
    else:
        # Use productID get stock, compare with quantity checkout
        comparingList = []
        insufficientQuantityProduct = []
        stringAppend = ""
        cur.execute("SELECT p.instock, cc.quantity, p.productName from Products P, Cart_Contents cc WHERE cc.productID = p.productID")
        data = cur.fetchall()
        # For loop to append SQL result into a list
        for i in data:
            comparingList.append(i)
        # Use the list and compare the element to see if instock enough to checkout
        # If not enough, add the product name into insufficientQuantityProduct list
        for i in comparingList:
            if i[0] < i[1]:
                insufficientQuantityProduct.append(i[2])
        
        # Split each element in insufficientQuantityProduct list into new line
        stringAppend = '\n'.join(insufficientQuantityProduct)

        # If insufficientQuantityProduct list is empty, means all items have stock, proceed to checkout
        if len(insufficientQuantityProduct) == 0:
            # Print out the text needed including the products
            query.edit_message_text("<b>SQL Checkout</b>" + "\n\n" +
                                        "Cart ID: " + str(data[0]) +
                            "Total Payable: <b>$" + str('{:.2f}'.format(totalAmount)) + "</b>\n\n" +
                            "Would you like to make payment?" + "\n\n" +
                            "To complete Checkout, please insert the following command" + "\n" + 
                            "/payment [Cart ID][Postal Code] [Unit Number]" + "\n" +
                            "Example: /payment 1 530157 04-920", parse_mode="html")
        # Else there is at least 1 item that does not have enough stock
        # Print out the product names of those that instock is not enough
        else:              
            query.edit_message_text("<b>SQL Checkout</b>" + "\n\n" +
                            "There is not enough stock for the follow items:" + "\n" +
                            stringAppend + "\n\n"
                            "You may want to double check the items instock from Products Page", parse_mode="html", reply_markup=reply_markup2)