import pytest
import pandas as pd
from decouple import config
from bs4 import BeautifulSoup as bs

from bot.helpers.scraper_quotes import ScraperQuotes  # Importe a classe ScraperQuotes do seu módulo

url = "https://quotes.toscrape.com"#config('URL_QUOTES')

print(url)

# Crie um objeto ScraperQuotes de exemplo para testes
scraper = ScraperQuotes(url)


# Teste o método fetch_html
def test_fetch_html():
    html = scraper.fetch_html(url)
    assert isinstance(html, str)

# Teste o método find_element
def test_find_element():
    soup = scraper.fetch_html(url)
    page_soup = bs(soup, 'html.parser')
    element = scraper.find_element(page_soup, ("class_name", "text"))
    assert element is not None

# Teste o método find_elements
def test_find_elements():
    soup = scraper.fetch_html(url)
    page_soup = bs(soup, 'html.parser')
    elements = scraper.find_elements(page_soup, ("class_name", "quote"))
    assert len(elements) > 0

# Teste o método fetch_about_info
def test_fetch_about_info():
    author, description, born, location = scraper.fetch_about_info(f"{url}/author/Albert-Einstein/")
    assert author is not None
    assert description is not None
    assert born is not None
    assert location is not None

# Teste o método fetch_quotes_on_page
def test_fetch_quotes_on_page():
    scraper.fetch_quotes_on_page(f"{url}/page/1/")
    assert len(scraper.quotes_data) > 0

# Teste o método run_scraper
def test_run_scraper():
    scraper.run_scraper(quantity_page=2)  # Defina a quantidade de páginas que deseja testar
    assert len(scraper.quotes_data) > 0

# Teste o método show_dataframe
def test_show_dataframe():
    df = scraper.show_dataframe()
    assert isinstance(df, pd.DataFrame)

# Teste o método save_data_as_json
def test_save_data_as_json():
    scraper.save_data_as_json()
    # Verifique se o arquivo JSON foi criado com sucesso

# Teste o método save_data_as_xlsx
def test_save_data_as_xlsx():
    scraper.save_data_as_xlsx()
    # Verifique se o arquivo XLSX foi criado com sucesso
