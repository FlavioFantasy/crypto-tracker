# https://rdrr.io/cran/telegram.bot/man/
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#post-an-image-file-from-disk
# https://rdrr.io/cran/telegram.bot/man/sendPhoto.html

import telegram

from tracker.config import CurrentConf

bot_token = CurrentConf.get().get_telegram_token()
my_chatid = CurrentConf.get().get_telegram_chat_id()


def send_message(text: str):
    msg = " 💰 [ Crypto ] 💰 \n"
    msg += text

    bot = telegram.Bot(token=bot_token)
    bot.sendMessage(chat_id=my_chatid, text=msg)


def send_image(img_path: str):
    img = telegram.InputMediaPhoto(media=open(img_path, "rb"))
    bot = telegram.Bot(token=bot_token)
    bot.send_media_group(chat_id=my_chatid, media=[img])
