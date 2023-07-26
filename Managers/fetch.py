import asyncio
import os, time
import threading

import requests_cache
from sanic_ext import render
from sanic_jinja2 import SanicJinja2
import aiohttp
import schedule
from sanic import Sanic, json, text, redirect, html
from dotenv import load_dotenv
import csv
from utils import Display, currencies

load_dotenv()

payload = {}
headers = {
    "apikey": os.getenv('API_KEY')
}


class DataNotFoundError(Exception):
    pass


class EmptyList(Exception):
    pass


class Fetch:

    def __init__(self):
        pass

    @classmethod
    async def store_dict_list_to_csv(cls, file_path, dict_list):
        # Extract the keys from the first dictionary in the list
        fieldnames = dict_list[0].keys()

        # Open the CSV file for writing
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Write the data row by row
            for row in dict_list:
                writer.writerow(row)

    @classmethod
    async def asyncio_fetch_currency(cls, symbols, base, interval, not_found_symbol):
        print("async fetch gonna start")
        try:
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, data=payload, ssl=False) as response:
                    print("sdv")
                    result = await response.json()
                    rates = result['rates']
                    data = []
                    for currency, values in rates.items():
                        data.append({"currency": currency, "value": values, "base": base})

                    await cls.store_dict_list_to_csv('data.csv', data)

                    # # time.sleep(1)
                    # print("sdc")
                    # return await render("prac.html",context={"data": data, "symbol": symbols, "base": base, "interval": interval})
                    return await Display.display_currency_handler(not_found_symbol)
                    # res = await display_currency_handler(not_found_symbol)
                    # return html(res)
        except Exception as e:
            return e

    # async def my_task():
    #     print("Task executed at:", time.strftime("%Y-%m-%d %H:%M:%S"))
    # async def trial(symbols, base, interval, not_found_symbol):
    #     while True:
    #         # Wait for 10 seconds
    #         print("Scheduled make_api_call task started")
    #         await asyncio_fetch_currency(symbols, base, interval, not_found_symbol)
    #         # await as
    #         print("Scheduled make_api_call task completed")
    #         await asyncio.sleep(interval)

    # def run_scheduler():
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)
    #

    @classmethod
    async def fetch_currency_handler(cls, request):
        try:
            query_params = request.args

            symbols = query_params.get(['symbols'][0], 'USD')

            symbols_list = symbols.split(',')
            symbols_list = [item.upper() for item in symbols_list]

            not_found_symbol = []

            for val in symbols_list:
                if val not in currencies:
                    not_found_symbol.append(val)
                    symbols_list.remove(val)

            if len(symbols_list) == 0:
                raise DataNotFoundError('All the currencies you want to fetch are wrong')

            base = query_params.get(['base'][0], 'INR')

            if base not in currencies:
                raise DataNotFoundError('api does not support the base currency you want to send')

            interval = float(query_params.get('interval', 20))

            # print("fetch_task start")
            # data = await asyncio_fetch_currency(symbols, base, interval, not_found_symbol)
            task1 = asyncio.create_task(asyncio.wait_for(cls.asyncio_fetch_currency(symbols, base, interval, not_found_symbol),timeout=100))
            # schedule.every(10).seconds.do(task1)
            # scheduler_thread = threading.Thread(target=run_scheduler)
            # scheduler_thread.start()

            # task1 = asyncio.create_task(trial(symbols, base, interval, not_found_symbol))
            # return data
            data = await task1
            return data

            # res = await display_currency_handler(not_found_symbol)
            # return html(res)

        except asyncio.TimeoutError:
            raise Exception("Response not received within the timeout period (100 seconds)")
        except ValueError:
            # If 'amount' is not an integer or not provided, handle the error
            return json({'error': 'Interval must be a integer'}, status=400)
        except EmptyList as e:
            return json({'error': str(e)}, status=404)
        except DataNotFoundError as e:
            return json({'error': str(e)}, status=404)
        except Exception as e:
            return text(f"Error: {str(e)}")
