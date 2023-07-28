import asyncio
import os
import aiohttp
from sanic import json, text
from dotenv import load_dotenv
from utils import currencies

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


class Convert:

    def __init__(self):
        pass

    @classmethod
    async def asyncio_convert_currency(cls, convert_to, convert_from, amount):
        # print("async convert just started")
        try:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={convert_from}&amount={amount}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, data=payload, ssl=False) as response:
                    result = await response.json()
                    return json({"status-code": 200, "result": result})
        except Exception as e:
            return e

    @classmethod
    async def convert_currency_handler(cls, request):

        try:

            query_params = request.args

            convert_to = query_params['to'][0]
            convert_to = convert_to.upper()
            if convert_to not in currencies:
                raise DataNotFoundError(f'We do not support {convert_to}')

            convert_from = query_params['from'][0]
            convert_from = convert_from.upper()
            if convert_from not in currencies:
                raise DataNotFoundError(f'We do not support {convert_from}')

            amount = float(query_params['amount'][0])

            # print("convert_currency gonna start")
            task2 = asyncio.create_task(
                asyncio.wait_for(cls.asyncio_convert_currency(convert_to, convert_from, amount), timeout=60))

            data = await task2
            # print("convert_currency_end")
            return data

        except asyncio.TimeoutError:
            # If the api does not give the response within the given time period
            raise Exception("Response not received within the timeout period (60 seconds)")
        except ValueError:
            # If 'amount' is not an integer or not provided, handle the error
            return json({'error': 'amount must be a integer or float'}, status=400)
        except DataNotFoundError as e:
            return json({'error': str(e)}, status=404)
        except Exception as e:
            return text(f"Error: {str(e)}")
