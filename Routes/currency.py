from sanic import Blueprint
import asyncio

from Managers.available import Available
from Managers.remove import Remove
from Managers.fetch import Fetch
from Managers.convert import Convert
from utils import *

currency = Blueprint("currency", version=1)


@currency.get("/fetch-currency")
async def fetch_currency(request):
    response = await Fetch.fetch_currency_handler(request)
    return response


@currency.get("/available-currency")
async def available_currency(request):
    response = await Available.available_currency_handler()
    return response


@currency.get("/remove-currency")
async def remove_currency(request):
    response = await Remove.remove_currency_handler(request)
    return response


@currency.get("/convert-currency")
async def convert_currency(request):
    response = await Convert.convert_currency_handler(request)
    return response


@currency.get("/display-currency")
async def display_currency(request):
    response = await Display.display_currency_handler()
    return response


@currency.get("/help")
def help__(request):
    response = Help.help_handler()
    return response


@currency.get("/")
def home_page(request):
    response = HomePage.home_page_handler()
    return response
