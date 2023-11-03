import sys
import configparser
from loguru import logger
from decouple import config
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

from bot.database.db import create_database_table
from bot.helpers.scraper_quotes import ScraperQuotes


logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini')


class Bot(Thread, ScraperQuotes):
    def __init__(self):
        "Projeto funcionando de moso assincrono, muito útil para multiplas tarefas simultâneas"
        self.url = config("URL_QUOTES")
        self.quotes_data = []
        Thread.__init__(self)

    def run(self) -> None:
        logger.success('Iniciando scrapyng dos dados')
        try:
            data = self.run_scraper(save_json=True, save_xlsx=True, save_database=True, quantity_page=0)
            print(self.show_dataframe())
        finally:
            logger.info('Processo finalizado')
            

def run_bot():
    create_database_table()# Criar tabela no banco de dados caso nao exista
    bot = Bot()
    bot.start()


if __name__ == "__main__":
    HOUR = config_ini['CONFIG']['UPDATE_HOUR']
    MINUTES = config_ini['CONFIG']['UPDATE_MINUTES']

    scheduler = BackgroundScheduler()
    scheduler.add_job(run_bot, 'cron', hour=HOUR, minute=MINUTES)
    scheduler.start()

    try:
        logger.success(f'BOT iniciado, atualização será iniciada no agendamento as: {HOUR}:{MINUTES}')
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()