from crontab import CronTab
from config.config import LOCAL_HOST_URL


def crontab_handler(url, interval):
    cron = CronTab(user='atul.goyal')
    cron.remove_all()
    job = cron.new(command=f'{url}')
    job.minute.every(interval)
    cron.write()


def create_crontab_url(symbols_list, base, interval):
    crontab_url = "curl --location '" + LOCAL_HOST_URL
    for currency in symbols_list:
        crontab_url += currency + "%2C"

    crontab_url = crontab_url[:-3]
    crontab_url += "&base=" + base

    crontab_url += "&interval=" + f'{interval}' + "'"
    crontab_handler(crontab_url, interval)
