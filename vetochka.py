from settings import token
from telegram.ext import Updater, CommandHandler
import logging
from modules import roll
from modules import new_maps
from modules import all_cmd
from modules import latest
from modules import memes
from modules import add_me


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('maps', new_maps.new_maps))
    dispatcher.add_handler(CommandHandler('roll', roll.roll))
    dispatcher.add_handler(CommandHandler('all', all_cmd.all_cmd))
    dispatcher.add_handler(CommandHandler('latest', latest.latest))
    dispatcher.add_handler(CommandHandler('memes', memes.memes))
    dispatcher.add_handler(CommandHandler('add_me', add_me.add_me))
    updater.start_polling()
    updater.idle()
