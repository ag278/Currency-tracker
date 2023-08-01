from sanic import json

from config.config import CURRENCIES
from exceptions.custom_exceptions import EmptyList, DataNotFoundError


def validate_input_currency(currency, currencies):
    if currency not in currencies:
        raise DataNotFoundError(f'We do not support {currency}')


def currency_list_validator(currency_list):
    not_found_currency = []

    # stores correct currencies
    updated_currency = []

    for val in currency_list:
        if val not in CURRENCIES:
            if val not in not_found_currency:
                not_found_currency.append(val)
        else:
            updated_currency.append(val)

    # if all the input currencies are wrong
    if len(updated_currency) == 0:
        raise EmptyList('All the input currencies are wrong')

    return not_found_currency, updated_currency
