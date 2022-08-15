# https://rdrr.io/cran/telegram.bot/man/
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#post-an-image-file-from-disk
# https://rdrr.io/cran/telegram.bot/man/sendPhoto.html

from pathlib import Path

import telegram

from tracker.config import CurrentConf
from typing import Union

_tg_token = CurrentConf.get().get_telegram_token()
_tg_dst_chatid = CurrentConf.get().get_telegram_chat_id()


def tg_send_message(text: str) -> None:
    msg = " 💰 [ Crypto ] 💰 \n\n"
    msg += text

    bot = telegram.Bot(token=_tg_token)
    bot.sendMessage(chat_id=_tg_dst_chatid, text=msg)


def tg_send_image(img_path: Union[str, Path]) -> None:
    img = telegram.InputMediaPhoto(media=open(img_path, "rb"))

    bot = telegram.Bot(token=_tg_token)
    bot.send_media_group(chat_id=_tg_dst_chatid, media=[img])
