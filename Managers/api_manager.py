import aiohttp
from config.config import HEADERS, PAYLOAD
from aiohttp_client_cache import CachedSession, SQLiteBackend
from sanic.exceptions import NotFound, BadRequest, RequestTimeout


class ApiManager:
    headers = HEADERS
    payload = PAYLOAD

    @classmethod
    async def api_call(cls, url):
        print(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=cls.headers, data=cls.payload, ssl=False) as response:
                if response.status == 400:
                    raise BadRequest("Bad request")
                elif response.status == 404:
                    raise NotFound("Not found")
                result = await response.json()
                return result

    @classmethod
    async def api_call_with_cache(cls, url):
        async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
            async with session.get(url, headers=cls.headers, data=cls.payload, ssl=False) as response:
                if response.status == 400:
                    raise BadRequest()
                elif response.status == 404:
                    raise NotFound()
                result = await response.json()
                return result
