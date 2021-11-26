import telegram

# Show Cart
def cart(update, context):
    update.message.reply_text("You have landed at the cart page!")
    update.message.reply_text("This page is still under development!")
    # update.message.reply_text("You have landed at the cart page!" + "\n\n" +
    #                             "/view    - Use this command to view the current location of keys." + "\n" +
    #                             "/draw    - Use this command to draw keys from people or from the key press." + "\n" +
    #                             "/return  - Use this command to return key to keypress." + "\n\n" +
    #                             "Key Information" + "\n\n" +
    #                             "Key ID 1 - Audit 1" + "\n" +
    #                             "Key ID 2 - Audit 2" + "\n" +
    #                             "Key ID 3 - MPH" + "\n" +
    #                             "Key ID 4 - PLR 1" + "\n" +
    #                             "Key ID 5 - PLR4")