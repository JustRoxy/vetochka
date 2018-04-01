"""Posts some hot dank memes from reddit."""
import praw
from random import shuffle
from datetime import datetime
from settings import rdt_client_id, rdt_client_secret, rdt_username, rdt_password


# subreddit and flair
subreddits = [('DeepFriedMemes', None),
              ('surrealmemes', None),
              ('nukedmemes', None),
              ('osugame', 'Fun')]


def fetch_memes(reddit, sub, flair=None):
    """Returns pic links of 50 hot memes of specified subreddit.

    Keyword arguments:
    sub -- subreddit name
    flair -- reddit flair (None by default)
    """
    response = reddit.subreddit(sub).hot(limit=50)
    urls = []
    if flair:
        urls = [submission.url for submission in response if submission.link_flair_text == 'Fun']
    else:
        urls = [submission.url for submission in response]
    return [url for url in urls if ".png" in url or ".jpg" in url]


def memes(bot, update):
    if not hasattr(memes, 'last_updated'):
        memes.last_updated = datetime.utcnow()
    if not hasattr(memes, 'reddit'):
        memes.reddit = praw.Reddit(client_id=rdt_client_id,
                                   client_secret=rdt_client_secret,
                                   user_agent='python_bot',
                                   username=rdt_username,
                                   password=rdt_password)
    if not hasattr(memes, 'urls'):
        memes.urls = []
    if not memes.urls or (datetime.utcnow() - memes.last_updated).seconds > 3600:
        for sub, flair in subreddits:
            memes.urls += fetch_memes(memes.reddit, sub, flair)
        shuffle(memes.urls)
        memes.last_updated = datetime.utcnow()
    meme_url = memes.urls.pop()
    bot.send_photo(chat_id=update.message.chat_id, photo=meme_url)
