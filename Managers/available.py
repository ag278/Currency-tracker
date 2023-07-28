import os
import asyncio
import aiohttp
import requests_cache, requests
from sanic import text
from dotenv import load_dotenv
from sanic_ext import render
from utils import currencies
from aiohttp_client_cache import CachedSession, SQLiteBackend
load_dotenv()

payload = {}
headers = {
    "apikey": os.getenv('API_KEY')
}


class Available:

    def __init__(self):
        pass

    @classmethod
    async def fetch_data(cls):

        url = "https://api.apilayer.com/exchangerates_data/symbols"

        # Check if the data is present in the cache
        async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
            async with session.get(url, headers=headers, data=payload, ssl=False) as response:
                ans = await response.json()
                data = ans.get('symbols')
                new_currencies = list(data.keys())

                # writing the updated currency list to the currencies list
                with open('utils/currencies.py', 'w') as file:
                    file.write(f"currencies = {new_currencies}\n")

                return await render("available.html", context={"seq": data}, status=200)

    @classmethod
    async def available_currency_handler(cls):
        try:
            task3 = asyncio.create_task(asyncio.wait_for(cls.fetch_data(), timeout=60))
            data = await task3
            return data
        except asyncio.TimeoutError:
            raise Exception("Response not received within the timeout period (60 seconds)")
        except Exception as e:
            return text(f"Error: {str(e)}")
