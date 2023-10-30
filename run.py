import sys
from loguru import logger
from decouple import config
from threading import Thread

from bot.helpers.scraper_quotes import ScraperQuotes

logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


class Bot(Thread, ScraperQuotes):
    
    def __init__(self):
        self.url = config("URL_QUOTES")
        self.quotes_data = []
        Thread.__init__(self)

    def run(self) -> None:
        logger.success('Bot iniciado.')
        try:
            data = self.run_scraper(save_json=True, save_xlsx=True, save_database=True, quantity_page=2)
            print(self.show_dataframe()) # Exibir dataframe
        finally:
            logger.info('Processo finalizado')
            

if __name__ == "__main__":
    bot = Bot()
    bot.start()