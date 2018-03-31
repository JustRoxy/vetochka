import os
import pyoppai
from telegram import ParseMode
from settings import io_folder
from global_objects import api, users
from osu_utils import parse_mods, datetime_fromnow


def oppai_call(score):
    """It's gonna be messy xd"""
    ctx = pyoppai.new_ctx()
    b = pyoppai.new_beatmap(ctx)
    BUFSIZE = 2000000  # should be big enough to hold the .osu file
    buf = pyoppai.new_buffer(BUFSIZE)
    fname = io_folder + score['beatmap_id'] + '.osu'
    mods = int(score['enabled_mods'])
    arg_keys = ('maxcombo', 'countmiss', 'count300', 'count100', 'count50')
    args = [int(score[arg]) for arg in arg_keys]
    pyoppai.parse(
        fname,
        b,
        buf,
        BUFSIZE,
        False,
        os.path.dirname(os.path.realpath(__file__))
    )
    dctx = pyoppai.new_d_calc_ctx(ctx)
    pyoppai.apply_mods(b, mods)
    stars, aim, speed, _, _, _, _ = pyoppai.d_calc(dctx, b)
    acc, pp, aim_pp, speed_pp, acc_pp = \
        pyoppai.pp_calc(ctx, aim, speed, b, mods, *args)
    # _, max_pp, _, _, _ = pyoppai.pp_calc_acc(ctx, aim, speed, b, 100.0)
    oppai_score_info = dict()
    oppai_score_info['map_info'] = "{} - {}[{}]".format(pyoppai.artist(b),
                                                        pyoppai.title(b),
                                                        pyoppai.version(b))
    oppai_score_info['mod_info'] = parse_mods(mods)
    oppai_score_info['combo_info'] = "{}/{}".format(score['maxcombo'],
                                                    pyoppai.max_combo(b))
    oppai_score_info['hitstat_info'] = "({}/{}/{}/{})".format(score['count300'],
                                                              score['count100'],
                                                              score['count50'],
                                                              score['countmiss'])
    oppai_score_info['acc_info'] = "{0:.2f}".format(acc)
    #pp_info = "{0:.2f}/{0:.2f}".format(pp, max_pp)
    oppai_score_info['pp_info'] = "{0:.2f}".format(pp)
    return oppai_score_info


def html_score_info(score, oppai_score_info):
    lines = []
    map_url = '"https://osu.ppy.sh/b/{}"'.format(score['beatmap_id'])
    date_info = datetime_fromnow(score['date'])
    lines.append("<b>({})</b> <a href={}>{}</a> <b>{} ({}%)</b>".format(score['rank'],
                                                                        map_url,
                                                                        oppai_score_info['map_info'],
                                                                        oppai_score_info['mod_info'],
                                                                        oppai_score_info['acc_info']))
    lines.append("{}x {} | {}pp".format(
        oppai_score_info['combo_info'], oppai_score_info['hitstat_info'], oppai_score_info['pp_info']))
    lines.append("{} ago\n".format(date_info))
    return "\n".join(lines)


def latest(bot, update):
    limit = 1
    for item in update.message.text.split(" "):
        if item.isdigit():
            if int(item) > 0 and int(item) < 15:
                limit = int(item)
    username = update.message.from_user.username
    if username in users:
        ingame_name = users[username]
    else:
        update.message.reply_text("Ты кто")
        return
    scores = api.get_user_recent(ingame_name, limit)
    if scores:
        b_ids = list(set(score['beatmap_id'] for score in scores))
        api.download_beatmaps(b_ids)
        reply_lines = []
        for score in scores:
            oppai_score_info = oppai_call(score)
            reply_lines.append(html_score_info(score, oppai_score_info))
        html_final_reply = "".join(reply_lines)
        bot.send_message(chat_id=update.message.chat_id,
                         text=html_final_reply,
                         parse_mode=ParseMode.HTML,
                         disable_web_page_preview=True,
                         reply_to_message_id=update.message.message_id)
    else:
        update.message.reply_text("Нет скоров")
