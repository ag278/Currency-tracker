import os
from tortoise import Tortoise
from sanic import Sanic, text
from sanic.exceptions import NotFound
from crontab import CronTab
from Routes import root_group
from Managers.api_manager import ApiManager
from config.config import AVAILABLE_URL
from models.database.models import InitDatabase

app = Sanic("currency-tracker")
app.blueprint(root_group)
app.config.FALLBACK_ERROR_FORMAT = "json"


@app.listener("before_server_start")
async def check_api(app, loop):
    res = await ApiManager.api_call(AVAILABLE_URL)
    if not res.get('success'):
        app.stop()
        return text("Api is not working")


@app.listener("before_server_start")
def clear_crontab(app, loop):
    cron = CronTab(user='atul.goyal')
    cron.remove_all()
    cron.write()


@app.listener('before_server_start')
async def setup_db(app, loop):
    await InitDatabase.init_db()


@app.listener('before_server_stop')
async def stop_db(app, loop):
    await Tortoise.close_connections()


@app.exception(NotFound)
async def not_found(request, exception):
    return text('You entered the wrong URL, kindly check again')


if __name__ == '__main__':
    app.run()
