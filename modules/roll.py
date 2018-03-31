import random


def roll(bot, update):
    nums = set()
    for item in update.message.text.split(" "):
        if item.isdigit():
            nums.add(int(item))
    roll_max = 100
    if nums:
        if max(nums) == 0:
            update.message.reply_text("Поделил на 0")
            return
        roll_max = max(nums)
    update.message.reply_text(random.randint(1, roll_max))
