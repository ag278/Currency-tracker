from sanic import json
from Managers.data_manager import DataManager


class Display:
    @classmethod
    async def display_currency_handler(cls, not_found_symbol=None):
        data = await DataManager.read_file()
        return json({"data": data, "invalid-currency": not_found_symbol, "status": 200})
