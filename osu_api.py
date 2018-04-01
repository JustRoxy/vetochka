"""Partial implementation of https://github.com/ppy/osu-api/wiki
Wheelchairs included!
"""
import requests
import codecs
import asyncio
from aiohttp import ClientSession
from settings import io_folder, api_key


api_get_beatmaps = 'https://osu.ppy.sh/api/get_beatmaps'
api_get_user_recent = 'https://osu.ppy.sh/api/get_user_recent'
api_download_beatmaps = 'https://osu.ppy.sh/osu/'
api_get_user = 'https://osu.ppy.sh/api/get_user'

class OsuApi():

    def __init__(self, api_key_param):
        """
        Keyword arguments:
        api_key_param -- osu! api key, can be retrieved here https://osu.ppy.sh/p/api"""
        self.api_key = api_key_param


    def get_user(self, name, mode='0'):
        """Returns general user information.

        Keyword arguments:
        name -- osu! user name
        mode -- game mode ('0' = osu!, '1' = Taiko, '2' = CtB, '3' = osu!mania)"""
        body = {
            'k': self.api_key,
            'u': name,
            'm': mode,
            'type': 'u'
        }
        response = requests.post(api_get_user, data=body)
        return response.json()

    def get_beatmap(self, since, mode='0', a='0'):
        """Returns general beatmap information.

        Keyword arguments:
        since -- return all beatmaps ranked or loved since this date. Must be a MySQL date.
        mode -- game mode
        a -- specify whether converted beatmaps are included ('0' = not included, '1' = included)"""
        body = {
            'k': self.api_key,
            'since': since,
            'm': mode,
            'a': a
        }
        response = requests.get(api_get_beatmaps, params=body)
        return response.json()

    def get_user_recent(self, name, limit=1, mode='0'):
        """Returns the user's ten most recent plays over the last 24 hours.
        
        Keyword arguments:
        name -- osu! user name
        limit -- amount of results (range between 1 and 50)
        mode -- game mode
        """
        body = {
            'k': self.api_key,
            'u': name,
            'm': mode,
            'limit': limit,
            'type': 'string'
        }
        response = requests.get(api_get_user_recent, params=body)
        return response.json()

    def get_beatmaps(self, b_ids, mode='0', a='1', threads=10):
        """Returns general beatmap information for multiple beatmaps.
        
        Keyword arguments:
        b_ids -- list of beatmap ids to return metadata from
        mode -- game mode
        a -- specify whether converted beatmaps are included
        threads -- number of threads used to make http requests, b_ids are split between them
        """

        async def api_get_beatmap(body, session):
            async with session.post(api_get_beatmaps, params=body) as response:
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
        """Downloads .osu beatmap file into io_folder.
        
        Keyword arguments:
        b_ids - list of beatmap ids to download
        threads -- number of threads used to download beatmap files, b_ids are split between them
        """

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

        urls = [(api_download_beatmaps + b_id) for b_id in b_ids]
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
