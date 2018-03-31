import json
import osu_api
from settings import api_key, db_fname

api = osu_api.OsuApi(api_key)
users = json.load(open(db_fname))
