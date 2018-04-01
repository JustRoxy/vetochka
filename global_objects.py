"""Global objects which are used from multiple places.
Such approach is used because there is no actual sense in passing them via arguments.
Probably it's bad :("""

import json
import osu_api
from settings import api_key, db_fname

api = osu_api.OsuApi(api_key)
with open(db_fname) as f:
    users = json.load(f)
