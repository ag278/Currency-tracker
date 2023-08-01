import os

from sanic import text, json
import csv
from dotenv import load_dotenv
from utils import *

load_dotenv()

payload = {}
headers = {
    "apikey": os.getenv('API_KEY')
}


class DataNotFoundInCSVError(Exception):
    """
        Exception raised when the list is empty
    """
    pass


class NoQueryParam(Exception):
    """
        Exception raised when the query parameter is not provided
    """
    pass


class Remove:

    def __init__(self):
        pass

    @classmethod
    async def delete_csv_row(cls, file_path, key_column, key_value):
        # Read the CSV file and load its contents into memory
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        if len(data) == 0:
            raise DataNotFoundInCSVError('The list is Empty')

        currency_list = key_value.split(',')
        # print(currency_list)

        # Identify the row(s) that need to be deleted
        rows_to_delete = []
        for val in currency_list:
            for row in data:
                if row[key_column] == val:
                    rows_to_delete.append(row)

        # print(rows_to_delete)

        if len(rows_to_delete) == 0:
            return text('All the currencies you have entered is/are not present in the list, kindly try again')

        # Remove the identified row(s) from the data
        for row in rows_to_delete:
            data.remove(row)

        # Write the updated data back to the CSV file
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(data)

        return await Display.display_currency_handler()

    @classmethod
    def remove_currency_handler(cls, request):
        try:
            query_params = request.args

            currency = query_params.get(['currency'][0], '-1')
            # print(currency)

            # Handles the case when the currency is provided
            if currency != '-1':
                currency = currency.upper()
                return cls.delete_csv_row('data.csv', 'currency', currency)

            raise NoQueryParam('Kindly enter the currency')
        except NoQueryParam as e:
            return json({'error': str(e)}, status=404)
        except DataNotFoundInCSVError as e:
            return json({'error': str(e)}, status=404)
        except Exception as e:
            return e
