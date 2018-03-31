import json
from global_objects import users, api
from settings import db_fname


def add_me(bot, update):
    osu_name = update.message.text.replace('/add_me ', '')
    username = update.message.from_user.username
    if username:
        response = api.get_user(osu_name)
        if response:
            if osu_name == response[0]['username']:
                users[username] = osu_name
            with open(db_fname, 'w') as outfile:
                json.dump(users, outfile)
            update.message.reply_text("Добавил, проверяй")
        else:
            update.message.reply_text("Попробуй еще раз")
    else:
        update.message.reply_text("Заведи юзернейм")
