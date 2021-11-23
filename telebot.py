from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext, commandhandler
import telegram
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

#Variable Declaration
STATE = None
# STATEs for Drawing Keys
KEY_ID_DRAW = 1
DRAWER_NAME = 2
# STATEs for Returning Keys
KEY_ID_RETURN = 3
RETURN_NAME = 4
#Storage system for key
#keys_dict = {'key':'Name + ',' + Date'}
#Future implementation to store this information in cloud
keys_dict = {0: None, 1:"Keypress", 2:"Keypress", 3:"Keypress", 4:"Keypress", 5:"Keypress"}

startkeyboard = [
        [
            InlineKeyboardButton("Product", callback_data='product'),
            InlineKeyboardButton("Cart", callback_data='cart'),
        ],
        [
            InlineKeyboardButton("Checkout", callback_data='checkout'),
            InlineKeyboardButton("Profile", callback_data='profile'),
        ],[
            InlineKeyboardButton("Promo", callback_data='promo'),
            InlineKeyboardButton("Help", callback_data='help'),
        ],
    ]
helpkeyboard = [
        [
            InlineKeyboardButton("Product", callback_data='product'),
            InlineKeyboardButton("Cart", callback_data='cart'),
        ],
        [
            InlineKeyboardButton("Checkout", callback_data='checkout'),
            InlineKeyboardButton("Profile", callback_data='profile'),
        ],[
            InlineKeyboardButton("Promo", callback_data='promo')
        ],
    ]
#End of variable declaration

# DONE
# /start command
def start(update: Update, context: CallbackContext):
    first_name = update.message.chat.first_name

    reply_markup = InlineKeyboardMarkup(startkeyboard)
    update.message.reply_text("Hello %s, nice to meet you and welcome to dissney mama shop!" % first_name)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

# Buttoon for callbackquery on inline button
def button(update: Update, context: CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data == "product":
        query.edit_message_text(text=f"Selected option: Product")
    elif query.data == "cart":
        query.edit_message_text(text=f"Selected option: Cart")
    elif query.data == "checkout":
        query.edit_message_text(text=f"Selected option: Checkout")
    elif query.data == "profile":
        query.edit_message_text(text=f"Selected option: Profile")
    elif query.data == "promo":
        query.edit_message_text(text=f"Selected option: Promo")
    elif query.data == "help":
        help(update, context)

# DONE
# /help command
def help(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(helpkeyboard)

    query.edit_message_text("Here are the commands:" + "\n\n" +
                              "Product     - View available products " + "\n" +
                              "Cart        - View shopping cart" + "\n" +
                              "Checkout    - Cart checkout" + "\n" +
                              "Profile     - User profile" + "\n" +
                              "Promo       - View promotional item" + "\n" + 
                              "Help        - View available help " + "\n\n" +
                              "If you require additional assistance, you can contact us at @darrennnnnlim, @kendricklee or @yongkhengs!", reply_markup=reply_markup)

# /product command
def product(update, context):
    update.message.reply_text("You have landed at the product page!")
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
    
# /cart command
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

# /checkout command
def checkout(update, context):
    update.message.reply_text("You have landed at the checkout page!")
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

# /profile command
def profile(update, context):
    update.message.reply_text("You have landed at the profile page!")
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

# /promo command
def promo(update, context):
    update.message.reply_text("You have landed at the promo page!")
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

# Error message displayed to user
def error(update, context):
    update.message.reply_text('An error has occured')

# function to handle normal text
# Add the different STATE here as response are received through text
def text(update, context):
    global STATE

    if STATE == KEY_ID_DRAW:
        return received_key_id_draw(update, context)

    if STATE == DRAWER_NAME:
        return received_drawer_name(update, context)

    if STATE == KEY_ID_RETURN:
        return received_key_id_return(update, context)

    if STATE == RETURN_NAME:
        return received_return_name(update, context)

# /draw command
def draw_keys(update, context):
    global STATE

    STATE = KEY_ID_DRAW
    
    update.message.reply_text("You are now DRAWING a key" + "\n\n" +
                                "Key Information" + "\n\n" +
                                "Key ID 1 - Audit 1" + "\n" +
                                "Key ID 2 - Audit 2" + "\n" +
                                "Key ID 3 - MPH" + "\n" +
                                "Key ID 4 - PLR 1" + "\n" +
                                "Key ID 5 - PLR4")
    update.message.reply_text("Enter the Key ID to draw:")
    
# Get Key ID (Drawing) from reply
def received_key_id_draw(update, context):
    global STATE
    
    try:
        key_id_to_draw = int(update.message.text)
        
        if key_id_to_draw < 0 or key_id_to_draw > 5:
            raise ValueError("Key does not seem to exist!")
        context.user_data['key_id_to_draw'] = key_id_to_draw
        update.message.reply_text("What is your name?")

        STATE = DRAWER_NAME
    except:
        update.message.reply_text("Please use the key ID found in /help")
    
# Get name of drawer from reply
def received_drawer_name(update, context):
    global STATE

    try:
        time_now = datetime.now()
        dt_now_string = time_now.strftime("%d/%m/%Y %H:%M")
        drawer_name = str(update.message.text)
        key_id_to_draw = context.user_data['key_id_to_draw']
        
        STATE = None
        update.message.reply_text("Key ID {} drawn by {} on {}" .format(key_id_to_draw, drawer_name, dt_now_string))
        keys_dict[key_id_to_draw] = drawer_name + " on " + dt_now_string
    except:
        update.message.reply_text("Drawing of key failed.")

# /return command
def return_keys(update, context):
    global STATE

    STATE = KEY_ID_RETURN
    
    update.message.reply_text("You are now RETURNING a key" + "\n\n" +
                                "Key Information" + "\n\n" +
                                "Key ID 1 - Audit 1" + "\n" +
                                "Key ID 2 - Audit 2" + "\n" +
                                "Key ID 3 - MPH" + "\n" +
                                "Key ID 4 - PLR 1" + "\n" +
                                "Key ID 5 - PLR4")
    update.message.reply_text("Enter the Key ID to return:")

# Get Key ID (Returning) from reply
def received_key_id_return(update, context):
    global STATE
    
    try:
        key_id_to_return = int(update.message.text)
        
        if key_id_to_return < 0 or key_id_to_return > 5:
            raise ValueError("Key does not seem to exist!")
           
        context.user_data['key_id_to_return'] = key_id_to_return
        update.message.reply_text("What is your name?")

        STATE = RETURN_NAME
    except:
        update.message.reply_text("Are you sure the key exists?")

# Get name of person that return from reply
def received_return_name(update, context):
    global STATE

    try:
        time_now = datetime.now()
        dt_now_string = time_now.strftime("%d/%m/%Y %H:%M")
        return_name = str(update.message.text)
        key_id_to_return = context.user_data['key_id_to_return']
        
        STATE = None
        
        update.message.reply_text("Key ID {} returned by {} on {}" .format(key_id_to_return, return_name, dt_now_string))
        keys_dict[key_id_to_return] = "Keypress (returned by {} on {})" .format(return_name, dt_now_string)
    except:
        update.message.reply_text("Returning of key failed.")

# /view command
def view_keys(update, context):
    #Implement function
    str_to_print = ''
    
    for i in range(1, len(keys_dict), 1):
        str_to_print += "Key {} last seen with {}\n".format(i, keys_dict[i])
    update.message.reply_text(str_to_print)


#Main function
# THIS IS THE PART THAT LINK THE COMMANDS TO THE FUNCTION
def main():
    #Change TOKEN here
    TOKEN = "2132985175:AAEMPGwqmVmki5okwnzoonFti0XN5NlT4UA"

    # create the updater, that will automatically create also a dispatcher and a queue to 
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher


    # add handlers for start and help commands
    # CommandHandler(Command User Type, function to call)
    # Add commands here
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("product", product))
    dispatcher.add_handler(CommandHandler("cart", cart))
    dispatcher.add_handler(CommandHandler("checkout", checkout))
    dispatcher.add_handler(CommandHandler("profile", profile))
    dispatcher.add_handler(CommandHandler("promo", promo))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CallbackQueryHandler(help))
    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()

