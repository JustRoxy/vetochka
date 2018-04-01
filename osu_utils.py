"""Useful functions dump."""
from datetime import datetime, timedelta


def parse_mods(bitmask):
    """Returns string with enabled mods.
    See https://github.com/ppy/osu-api/wiki for reference."""
    mod_bits = {
        'NF': 1,
        'EZ': 2,
        'HD': 8,
        'HR': 16,
        'SD': 32,
        'DT': 64,
        'RX': 128,
        'HT': 256,
        'NC': 512,
        'FL': 1024,
        'SO': 4096,
        'PF': 16384
    }
    if bitmask == 0:
        return ''
    else:
        mods = '+'
        for k, v in mod_bits.items():
            if bitmask & v:
                mods += k
        if 'NC' in mods:
            mods.replace('DT', '')
        if 'PF' in mods:
            mods.replace('SD', '')
        return mods


def datetime_fromnow(date):
    """Returns time difference between datetime score was set and current datetime.
    NOTE - datetime got by osu! api is UTC+8

    Keyword arguments:
    date -- datetime got by osu! api"""
    date_score = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_now = datetime.utcnow() + timedelta(hours=8)
    date_diff = date_now - date_score
    hours = int(date_diff.seconds / 3600)
    minutes = int((date_diff.seconds - hours * 3600) / 60)
    seconds = date_diff.seconds - hours * 3600 - minutes * 60
    return "{}:{}:{}".format(hours, minutes, seconds)
