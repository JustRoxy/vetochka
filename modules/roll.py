"""Rolls number, range is 1-100 by default."""
import random


def parse_limit(text):
    """Returns roll range parsed from sometimes random user input.
    Negative numbers are not accepted.
    The greatest value found in user input is taken.
    """
    nums = set()
    for item in text.split(" "):
        if item.isdigit():
            nums.add(int(item))
    if nums:
        return max(nums)
    else:
        return None


def roll(bot, update):
    user_input = parse_limit(update.message.text)
    roll_max = 100
    if user_input:
        roll_max = user_input
    if roll_max == 0: # easter eggs
        update.message.reply_text("Поделил на 0")
        return
    update.message.reply_text(random.randint(1, roll_max))
