from sanic.exceptions import SanicException
from sanic import Sanic, response
from sanic.exceptions import BadRequest, NotFound
from pydantic import BaseModel, ValidationError
import asyncio
from exceptions.error_messages import REQUEST_TIMEOUT_MESSAGE, WRONG_INPUT_MESSAGE,EMPTY_LIST_MESSAGE


class DataNotFoundError(SanicException):
    """
    Exception raised when data is not found
    """

    def __init__(self, message="We do not support this currency"):
        super().__init__(message)


class EmptyList(SanicException):
    """
    Exception raised when the list is empty
    """

    def __init__(self, message="The list is empty"):
        # print(message)
        super().__init__(message)


def custom_exception_handler(*exceptions):
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            try:
                return await func(request, *args, **kwargs)
            except ValidationError as e:
                return response.json({"status": 400, "error": "Validation error", "detail": str(e)}, status=400)
            except asyncio.TimeoutError as e:
                return response.json({"status": 408, "error": REQUEST_TIMEOUT_MESSAGE, "detail": str(e)}, status=408)
            except DataNotFoundError as e:
                return response.json({"status": 404, "error": WRONG_INPUT_MESSAGE , "detail": str(e)}, status=404)
            except EmptyList as e:
                return response.json({"status": 400, "error": EMPTY_LIST_MESSAGE, "detail": str(e)}, status=400)
            except exceptions as e:
                # Handle the specific exceptions here
                return response.json({"error": str(e)}, status=500)

        return wrapper

    return decorator
