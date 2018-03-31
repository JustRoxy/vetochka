"""Partial implementation of https://github.com/ppy/osu-api/wiki
wheelchairs included!
"""
import requests
import codecs
import asyncio
from aiohttp import ClientSession
from settings import io_folder, api_key


class OsuApi():

    def __init__(self, api_key_param):
        self.api_key = api_key_param
        self.api_get_beatmaps = 'https://osu.ppy.sh/api/get_beatmaps'
        self.api_get_user_recent = 'https://osu.ppy.sh/api/get_user_recent'
        self.api_download_beatmaps = 'https://osu.ppy.sh/osu/'
        self.api_get_user = 'https://osu.ppy.sh/api/get_user'

    def get_user(self, name, mode='0'):
        body = {
            'k': self.api_key,
            'u': name,
            'm': mode,
            'type': 'u'
        }
        response = requests.post(self.api_get_user, data=body)
        return response.json()

    def get_beatmap(self, since, mode='0', a='0'):
        body = {
            'k': self.api_key,
            'since': since,
            'm': mode,
            'a': a
        }
        response = requests.get(self.api_get_beatmaps, params=body)
        return response.json()

    def get_user_recent(self, username, limit=1, mode='0'):
        body = {
            'k': self.api_key,
            'u': username,
            'm': mode,
            'limit': limit,
            'type': 'string'
        }
        response = requests.get(self.api_get_user_recent, params=body)
        return response.json()

    def get_beatmaps(self, b_ids, mode='0', a='1', threads=10):

        async def api_get_beatmap(body, session):
            async with session.post(self.api_get_beatmaps, params=body) as response:
                resp = await response.json()
                return resp

        async def fetch_all(bodies):
            tasks = []
            async with ClientSession() as session:
                for body in bodies:
                    task = asyncio.ensure_future(
                        api_get_beatmap(body, session))
                    tasks.append(task)
                resp = await asyncio.gather(*tasks)
                return resp

        bodies = (
            {
                'k': self.api_key,
                'b': b_id,
                'm': mode,
                'a': a
            }
            for b_id in b_ids
        )
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(fetch_all(bodies))
        resp = loop.run_until_complete(future)
        return resp

    def download_beatmaps(self, b_ids, threads=10):

        async def download_beatmap(b_id, url, session):
            async with session.get(url) as response:
                fname = io_folder + b_id + '.osu'
                text = await response.text()
                with codecs.open(fname, 'w', 'utf-8') as f:
                    f.write(text)

        async def fetch_all(b_ids, urls):
            tasks = []
            async with ClientSession() as session:
                for b_id, url in zip(b_ids, urls):
                    task = asyncio.ensure_future(
                        download_beatmap(b_id, url, session))
                    tasks.append(task)
                _ = await asyncio.gather(*tasks)

        urls = [(self.api_download_beatmaps + b_id) for b_id in b_ids]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(fetch_all(b_ids, urls))
        loop.run_until_complete(future)


if __name__ == "__main__":
    api = OsuApi(api_key)
    # diffs = api.get_beatmaps(['1469103'])
    # for d in diffs:
    #     print(d[0]['beatmap_id'])
    resp = api.get_user("dasd134rrce2rc2r2f5hg5wg45trew3s5g4s654g3")
    if resp:
        print(resp)
    else:
        print("nope")
