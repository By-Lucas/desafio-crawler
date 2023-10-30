import sys
from loguru import logger
from decouple import config
from celery import shared_task

from bot.helpers.scraper_quotes import ScraperQuotes


logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


@shared_task
def scrape_data():
    logger.success("Scraping agendado iniciado")
    url = config("URL_QUOTES")
    scraper = ScraperQuotes(url)
    data = scraper.run_scraper(save_json=True, save_xlsx=True, quantity_page=2)
    logger.info("Scraping agendado completo")
    return data
