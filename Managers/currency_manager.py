import asyncio
from sanic import text, response, json
from sanic.exceptions import BadRequest
from config import config
from Managers.api_manager import ApiManager
from sanic.exceptions import RequestTimeout
from pydantic import BaseModel, ValidationError
from exceptions.custom_exceptions import *
from exceptions.error_messages import *
from Managers.data_manager import DataManager
from utils.crontab import create_crontab_url
from utils.currency_validator import currency_list_validator, validate_input_currency
from models.response import *


class Currency:

    def __init__(self, base_url=None, query_params=None):
        self.base_url = base_url
        self.query_params = query_params
        self.final_url = ""

    def build(self):
        query_string = ""
        for key, value in self.query_params.items():
            join_value = ','.join(value)
            join_value = join_value.upper()
            query_string += key + "=" + join_value + '&'

        query_string = query_string[:-1]
        self.final_url = f"{self.base_url}{query_string}"

    async def remove(self):
        # try:
        currency = self.query_params['currency'][0]
        currency = currency.upper()
        currency_list = currency.split(',')

        not_found_currency, updated_currency = currency_list_validator(currency_list)

        data = await DataManager.read_file()

        if len(data) == 0:
            raise EmptyList(" The csv file is empty")

        # storing the rows which are not deleted by the request
        retain_curr = []

        for row in data:
            if row['currency'] not in currency_list:
                retain_curr.append(row)

        await DataManager.write_file(retain_curr)
        return not_found_currency

    # except Exception as e:
    #     return e

    async def fetch(self):
        try:
            symbols = self.query_params.get(['symbols'][0])
            base = self.query_params.get(['base'][0])
            base = base.upper()
            validate_input_currency(base, config.CURRENCIES)

            symbols_list = symbols.split(',')
            symbols_list = [item.upper() for item in symbols_list]

            not_found_currency, updated_currency = currency_list_validator(symbols_list)

            # if all the input currencies are wrong
            if len(updated_currency) == 0:
                raise EmptyList('All the currencies you want to fetch are wrong')

            interval = int(self.query_params.get('interval'))
            if interval < 0:
                raise BadRequest("interval Must be Positive")

            create_crontab_url(symbols_list, base, interval)

            self.build()
            task = asyncio.create_task(
                asyncio.wait_for(ApiManager.api_call(self.final_url), timeout=60))

            res = await task
            result = FetchModel(**res)
            data = []

            for currency, values in result.rates.items():
                data.append({"currency": currency, "value": values, "base": base})

            await DataManager.write_file(data)

            return not_found_currency

        except asyncio.TimeoutError:
            raise RequestTimeout(REQUEST_TIMEOUT_MESSAGE)
        # except Exception as e:
        #     return e

    async def convert(self):
        try:
            convert_to = self.query_params['to'][0]
            convert_to = convert_to.upper()
            validate_input_currency(convert_to, config.CURRENCIES)

            convert_from = self.query_params['from'][0]
            convert_from = convert_from.upper()
            validate_input_currency(convert_from, config.CURRENCIES)

            amount = float(self.query_params['amount'][0])
            if amount < 0:
                raise BadRequest("Amount must be positive")

            self.build()

            task = asyncio.create_task(asyncio.wait_for(ApiManager.api_call(self.final_url), timeout=60))
            res = await task
            result = ConvertModel(**res)

            return json({"success": result.success, "status-code": 200, "response": result.result})

        except asyncio.TimeoutError:
            raise RequestTimeout(REQUEST_TIMEOUT_MESSAGE)
        # except Exception as e:
        #     return response.json({'error': str(e)}, status=404)

    async def available(self):
        try:
            task = asyncio.create_task(asyncio.wait_for(ApiManager.api_call(self.base_url), timeout=60))
            res = await task
            result = AvailableModel(**res)
            return json({"success": result.success, "status-code": 200, "response": result.symbols})
        except asyncio.TimeoutError:
            raise RequestTimeout(REQUEST_TIMEOUT_MESSAGE)
        except Exception as e:
            return response.json({'error': str(e)}, status=404)
