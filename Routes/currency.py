from sanic import Blueprint
from sanic.request import Request
from sanic_ext import render
from config import config
from Managers.currency_manager import Currency
from utils import *
from models.request import *
from pydantic import ValidationError
from exceptions.custom_exceptions import DataNotFoundError, EmptyList

currency = Blueprint("currency", version=1)


@currency.route("/fetch-currency", methods=['GET'], name='fetch-currency')
@custom_exception_handler(ValidationError, DataNotFoundError, EmptyList)
async def fetch_currency(request: Request):
    FetchModel(**request.args)
    req = Currency(config.FETCH_URL, request.args)
    res = await req.fetch()
    return await Display.display_currency_handler(res)


@currency.route("/available-currency", methods=['GET'], name='available-currency')
async def available_currency(request: Request):
    req = Currency(config.AVAILABLE_URL)
    res = await req.available()
    return res


@currency.route('/remove-currency', methods=['DELETE'], name="remove-currency")
@custom_exception_handler(ValidationError, EmptyList)
async def remove_currency(request: Request):
    RemoveModel(**request.args)
    req = Currency(config.REMOVE_URL, request.args)
    res = await req.remove()
    return await Display.display_currency_handler(res)


@currency.route("/convert-currency", methods=['GET'], name="convert-currency")
@custom_exception_handler(ValidationError, DataNotFoundError)
async def convert_currency(request: Request):
    ConvertModel(**request.args)
    req = Currency(config.CONVERT_URL, request.args)
    return await req.convert()


@currency.route("/display-currency", methods=['GET'])
async def display_currency(request: Request):
    res = await Display.display_currency_handler()
    return res


@currency.route("/help", methods=['GET'])
async def help__(request: Request):
    return await render("help.html", status=200)


@currency.route("/", methods=['GET'])
async def home_page(request: Request):
    return await render('home.html', status=200)
