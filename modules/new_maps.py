from datetime import date, timedelta
from telegram import ParseMode
from global_objects import api


def new_maps(bot, update):
    delta = 0
    for item in update.message.text.split(" "):
        if item.isdigit():
            if int(item) > 0 and int(item) < 8:
                delta = int(item)
    since = date.today()
    since -= timedelta(delta)
    maps_new = api.get_beatmap(str(since))
    maps_hard = [m for m in maps_new if float(m['difficultyrating']) > 5.99]
    if maps_hard:
        reply_lines = []
        bset_ids = {m['beatmapset_id']: m['beatmap_id'] for m in maps_hard}
        b_ids = [bset_ids[k] for k in bset_ids]
        maps_info = api.get_beatmaps(b_ids)
        for b_id in b_ids:
            title, artist, url = "", "", ""
            for item in maps_info:
                if item[0]['beatmap_id'] == b_id:
                    title = item[0]['title']
                    artist = item[0]['artist']
                    url = "https://osu.ppy.sh/s/{}".format(item[0]['beatmapset_id'])
                    stars = "{0:.2f}".format(float(item[0]['difficultyrating']))
            reply_lines.append(
                '[{} - {}]({}) {} ★'.format(artist, title, url, stars))
        ans = "\n".join(reply_lines)
    else:
        ans = "@kugich няшка-милашка, а новых норм мап пока нет\n"
    bot.send_message(chat_id=update.message.chat_id,
                     text=ans,
                     parse_mode=ParseMode.MARKDOWN,
                     disable_web_page_preview=True,
                     reply_to_message_id=update.message.message_id)
