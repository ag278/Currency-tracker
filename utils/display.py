import csv
from sanic_ext import render


async def read_data_from_csv(filename):
    data = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    return data


class Display:
    class_variable = ''

    def __init__(self):
        pass

    @classmethod
    async def display_currency_handler(cls, not_found_symbol=None):
        if not_found_symbol is None:
            not_found_symbol = []
        data = await read_data_from_csv('data.csv')
        return await render("display_list.html",
                            context={"seq": data, "not_found_symbol": not_found_symbol,
                                     "length": len(not_found_symbol)},
                            status=200)
