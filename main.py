import requests
from bs4 import BeautifulSoup
import telegram.ext
import os

# telegram token environment variable
TOKEN = os.environ["TELEGRAM_TOKEN"]

# start command
def start(update, context):
    update.message.reply_text(
        """Merhaba, /menu yazarak yemek listesine ulaşabilirsin.
    /menu - Yemek Listesi
    """
    )


# get the YKS login page
def get_url(update, context):
    update.message.reply_text("https://yks.mu.edu.tr/Login.aspx")


# get the menu
def get_menu(update, context):
    # the url of the menu
    url = "https://www.mu.edu.tr/tr/yemek"

    # get the html code of the page
    r = requests.get(url)
    # parse the html code
    soup = BeautifulSoup(r.text, "html.parser")

    # get the menu items
    try:
        # get the table of the menu
        menu = soup.find("ul", class_="list listgeneral list-group yemekList")
        rows = menu.find_all("li")
        for row in rows:
            # get the name of the meal and the date
            meal = row.get_text(separator=" ").replace(" cal ", "")[:-13]
            # message to send
            update.message.reply_text(meal)
        update.message.reply_text("Yemek satın al: https://yks.mu.edu.tr/Login.aspx")
    except:
        update.message.reply_text("Yemek listesi boş.")


# create the updater
updater = telegram.ext.Updater(TOKEN)
# create the dispatcher
dispatcher = updater.dispatcher

# add the handlers
dispatcher.add_handler(telegram.ext.CommandHandler("start", start))
dispatcher.add_handler(telegram.ext.CommandHandler("menu", get_menu))
dispatcher.add_handler(telegram.ext.CommandHandler("yks", get_url))

# start the bot
updater.start_polling()
# stop the bot
updater.idle()
