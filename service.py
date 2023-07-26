import asyncio

from sanic import Sanic, text

from sanic.exceptions import NotFound
from Routes import root_group

app = Sanic("currency-tracker")
app.blueprint(root_group)


@app.exception(NotFound)
async def not_found(request, exception):
    return text('You entered the wrong URL, kindly check again')


if __name__ == '__main__':
    app.run()
