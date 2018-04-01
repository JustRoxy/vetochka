"""Adds new user to 'database'."""
import json
from global_objects import users, api
from settings import db_fname


def osu_name_exists(osu_name):
    """Checks if user exists and is correct."""
    response = api.get_user(osu_name)
    if response:
        return osu_name == response[0]['username']
    else:
        return False


def add_me(bot, update):
    """Adds new user to 'database'.
    There is a check via osu! api which guarantees that user name is valid.
    """
    osu_name = update.message.text.replace('/add_me ', '')
    username = update.message.from_user.username
    if username:
        if osu_name_exists(osu_name):
            users[username] = osu_name
            with open(db_fname, 'w') as outfile:
                json.dump(users, outfile)
            update.message.reply_text("Добавил, проверяй")
        else:
            update.message.reply_text("Попробуй еще раз")
    else:
        update.message.reply_text("Заведи юзернейм")
