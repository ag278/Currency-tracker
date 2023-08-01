import asyncio
import os, time

from crontab import CronTab
import aiohttp
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
    """
        Exception raised when data is not found
    """
    pass


class EmptyList(Exception):
    """
        Exception raised when the list in empty
    """
    pass


class Fetch:

    def __init__(self):
        pass

    @classmethod
    def store_dict_list_to_csv(cls, file_path, dict_list):
        # Extract the keys from the first dictionary in the list
        fieldnames = dict_list[0].keys()

        # Open the CSV file for writing
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for row in dict_list:
                writer.writerow(row)

    @classmethod
    def crontab_handler(cls, url, interval):

        cron = CronTab(user='atul.goyal')
        job = cron.new(command=f'{url}')
        job.minute.every(interval)
        cron.write()

    @classmethod
    async def asyncio_fetch_currency(cls, symbols, base, not_found_symbol):
        try:
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, data=payload, ssl=False) as response:
                    result = await response.json()

                    rates = result['rates']

                    data = []

                    for currency, values in rates.items():
                        data.append({"currency": currency, "value": values, "base": base})

                    cls.store_dict_list_to_csv('data.csv', data)
                    return json({"sdff":"sdf"})
                    # return await Display.display_currency_handler(not_found_symbol)

        except Exception as e:
            return e

    @classmethod
    async def fetch_currency_handler(cls, request):
        try:
            query_params = request.args

            symbols = query_params.get(['symbols'][0], 'USD')

            symbols_list = symbols.split(',')
            symbols_list = [item.upper() for item in symbols_list]

            # stores wrong currencies
            not_found_symbol = []

            # stores correct currencies
            updated_symbol_list = []

            for val in symbols_list:
                if val not in currencies:
                    if val not in not_found_symbol:
                        not_found_symbol.append(val)
                else:
                    updated_symbol_list.append(val)

            # if all the input currencies are wrong
            if len(updated_symbol_list) == 0:
                raise EmptyList('All the currencies you want to fetch are wrong')

            base = query_params.get(['base'][0], 'INR')

            # wrong base currency
            if base not in currencies:
                raise DataNotFoundError('api does not support the base currency you want to send')

            # after what time user has to refresh the currency
            interval = int(query_params.get('interval', 1))

            # creating the crontab url
            crontab_url = "curl --location 'http://127.0.0.1:8000/v1/fetch-currency?symbols="
            for currency in symbols_list:
                crontab_url += currency + "%2C"

            crontab_url = crontab_url[:-3]
            crontab_url += "&base=" + base + "'"

            # cls.crontab_handler(crontab_url, interval)

            task1 = asyncio.create_task(
                asyncio.wait_for(cls.asyncio_fetch_currency(symbols, base, not_found_symbol), timeout=60))

            data = await task1
            return data

        except asyncio.TimeoutError:
            # If the api does not give the response within the given time period
            raise Exception("Response not received within the timeout period (60 seconds)")
        except ValueError:
            # If 'interval' is not an integer, handle the error
            return json({'error': 'Interval must be a integer'}, status=400)
        except EmptyList as e:
            return json({'error': str(e)}, status=404)
        except DataNotFoundError as e:
            return json({'error': str(e)}, status=404)
        except Exception as e:
            return text(f"Error: {str(e)}")
