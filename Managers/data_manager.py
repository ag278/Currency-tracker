import csv
import aiofiles
import asyncio


class DataManager:

    @classmethod
    async def read_file(cls):
        async with aiofiles.open('data.csv', mode='r') as file:
            csv_reader = csv.DictReader(await file.readlines())
            csv_list = list(csv_reader)
            return csv_list

    @classmethod
    async def write_file(cls, currency_list):
        async with aiofiles.open('data.csv', mode='w', newline='') as outfile:
            fieldnames = ['currency', 'value', 'base']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)

            await writer.writeheader()  # Write the header row

            await asyncio.gather(*[writer.writerow(row) for row in currency_list])
