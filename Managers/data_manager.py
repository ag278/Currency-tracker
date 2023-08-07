import csv
import aiofiles
import asyncio
from models.database.models import *
from sanic.log import logger


class DataManager:

    @classmethod
    async def read_file(cls):
        return await TrackCurrency.all().values('currency', 'value', 'base')
        # async with aiofiles.open('data.csv', mode='r') as file:
        #     csv_reader = csv.DictReader(await file.readlines())
        #     csv_list = list(csv_reader)
        #     return csv_list

    @classmethod
    async def write_file(cls, currency_list):
        # async with aiofiles.open('data.csv', mode='w', newline='') as outfile:
        #     fieldnames = ['currency', 'value', 'base']
        #     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        #
        #     await writer.writeheader()  # Write the header row
        #
        #     await asyncio.gather(*[writer.writerow(row) for row in currency_list])

        await TrackCurrency.all().delete()

        for row in currency_list:
            request = TrackCurrency(
                currency=row['currency'],
                value=row['value'],
                base=row['base']
            )
            await request.save()
