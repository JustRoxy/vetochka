from global_objects import users


def all_cmd(bot, update):
    usernames = ["@" + username for username in users]
    update.message.reply_text(" ".join(usernames))
