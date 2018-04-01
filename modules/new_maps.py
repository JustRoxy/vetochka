"""Prints info about newest ranked (or loved) more or less hard maps."""
from datetime import date, timedelta
from telegram import ParseMode
from global_objects import api


def parse_days(text):
    """Converts number of days specified by user to MySQL date."""
    delta = 0
    for item in text.split(" "):
        if item.isdigit():
            if int(item) > 0 and int(item) < 8:
                delta = int(item)
    since = date.today()
    since -= timedelta(delta)
    return since


def prettify(map_info):
    """Returns more or less pretty map info in HTML."""
    title = map_info[0]['title']
    artist = map_info[0]['artist']
    url = "https://osu.ppy.sh/s/{}".format(map_info[0]['beatmapset_id'])
    stars = "{0:.2f}".format(float(map_info[0]['difficultyrating']))
    return '[{} - {}]({}) {} ★'.format(artist, title, url, stars)


def new_maps(bot, update):
    since = parse_days(update.message.text)
    maps_new = api.get_beatmap(str(since))
    maps_hard = [m for m in maps_new if float(m['difficultyrating']) > 5.99]
    if maps_hard:
        reply_lines = []
        bset_ids = {m['beatmapset_id']: m['beatmap_id'] for m in maps_hard}
        b_ids = [bset_ids[k] for k in bset_ids]
        maps_info = api.get_beatmaps(b_ids)
        for b_id in b_ids:
            info = ""
            for item in maps_info:
                if item[0]['beatmap_id'] == b_id:
                    info = prettify(item)
            reply_lines.append(info)
        ans = "\n".join(reply_lines)
    else:
        ans = "@kugich няшка-милашка, а новых норм мап пока нет\n"
    bot.send_message(chat_id=update.message.chat_id,
                     text=ans,
                     parse_mode=ParseMode.MARKDOWN,
                     disable_web_page_preview=True,
                     reply_to_message_id=update.message.message_id)
