from sanic import Blueprint
from .currency import currency

root_group = Blueprint.group(currency)
