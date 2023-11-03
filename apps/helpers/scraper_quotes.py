import re
import json
import requests
import pandas as pd
from loguru import logger
from decouple import config
from bs4 import BeautifulSoup as bs

from core.models import NotificationsModel as notify


class ScraperQuotes:
    def __init__(self):
        self.url = config("URL_QUOTES")
        self.quotes_data = []
    
    def fetch_html(self, url):
        """Faz uma requisição para URL passada como parâmetro"""
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception("Erro ao fazer a solicitação HTTP")
    
    def find_element(self, soup: bs, *args):
        """
        Realiza uma pesquisa flexível de um elemento no BeautifulSoup com base em vários parâmetros.

        :param soup: Objeto BeautifulSoup representando a página da web.
        :param args: Parâmetros de pesquisa, como class_name, id, tag, name, css_selector.
        :return: Elemento BeautifulSoup correspondente à pesquisa ou None se não encontrado.
        """
        for param, value in args:
            if param == "class_name":
                element = soup.find(class_=value)
            elif param == "id":
                element = soup.find(id=value)
            elif param == "tag":
                element = soup.find(value)
            elif param == "text":
                element = soup.find(value)
            elif param == "name":
                element = soup.find(attrs={"name": value})
            elif param == "css_selector":
                element = soup.select_one(value)
            else:
                logger.error(f"Parâmetro de pesquisa inválido: {param}")
                raise ValueError(f"Parâmetro de pesquisa inválido: {param}")
            if element:
                return element
            
        logger.warning('O(s) elemento(s) em que fez a busca não foi encontrado.')
        return None


    def find_elements(self, soup: bs, *args):
        """
        Realiza uma pesquisa flexível de vários elementos no BeautifulSoup com base em vários parâmetros.

        :param soup: Objeto BeautifulSoup representando a página da web.
        :param args: Parâmetros de pesquisa, como class_name, id, tag, name, css_selector.
        :return: Elemento BeautifulSoup correspondente à pesquisa ou None se não encontrado.
        """
        for param, value in args:
            if param == "class_name":
                element = soup.find_all(class_=value)
            elif param == "id":
                element = soup.find_all(id=value)
            elif param == "tag":
                element = soup.find_all(value)
            elif param == "text":
                element = soup.find_all(value)
            elif param == "name":
                element = soup.find_all(attrs={"name": value})
            elif param == "css_selector":
                element = soup.select(value)
            else:
                logger.error(f"Parâmetro de pesquisa inválido: {param}")
                raise ValueError(f"Parâmetro de pesquisa inválido: {param}")
            if element:
                return element
            
        logger.warning('O(s) elemento(s) em que fez a busca não foi encontrado.')
        return None
    
    
    def fetch_about_info(self, about_url) -> tuple:
        '''Faz uma solicitação para a página "about"'''
        about_response = requests.get(about_url)
        if about_response.status_code == 200:
            about_html = about_response.text
            about_soup = bs(about_html, 'html.parser')

            author = self.find_element(about_soup, ("class_name", "author-title"), ("css_selector", "body > div > div.author-details > h3"))
            description = self.find_element(about_soup, ("class_name", "author-description"), ("css_selector", "body > div > div.author-details > div"))
            born = self.find_element(about_soup, ("class_name", "author-born-date"), ("css_selector", "body > div.container > div.author-details > p:nth-child(2) > span.author-born-date")) #nascimento
            location = self.find_element(about_soup, ("class_name", "author-born-location"), ("css_selector", "body > div.container > div.author-details > p:nth-child(2) > span.author-born-location"))
            return author, description, born, location
        
        else:
            logger.error("Erro ao fazer a solicitação HTTP para a página 'about'")
            return None

    def fetch_quotes_on_page(self, page_url) -> None:
        """Faz solicitção direta na url passada como prâmetro e percorre as paginas"""
        html = self.fetch_html(page_url)
        page_soup = bs(html, 'html.parser')

        elements = self.find_elements(page_soup, ("class_name", "quote"), ("css_selector", "body div.quote"))

        for element in elements:
            tag_list = []
            text = element.find("span", class_="text").text
            text = re.sub(r'[“”in ]', '', text)
            
            about_link = element.find("a")
            about = about_link.get('href')
            about_url = f"{self.url}{about}"

            tags = element.find_all("a", class_="tag")
            for tag in tags:
                tag_list.append(tag.text)

            about_info = self.fetch_about_info(about_url)
            if about_info:
                about_author, description, born, location = about_info
                location = re.sub(r'[in]', '', location.text)
                quote_data = {
                    'text': text,
                    "Author": about_author.text,
                    "Born": born.text,
                    "Location": location,
                    "Tags": ", ".join(tag_list),
                    "Description": description.text
                }
                self.quotes_data.append(quote_data)
                
    def run(self, save_json=True, save_xlsx=True, quantity_page:int=0) -> list:
        """Inicia o scraping e faz a paginação\nsave_json: Salvar no formato JSON\nsave_xlsxs: Salvar no formato xlsxs\nquantity_page: Quantidade de paginas a serem percorridas"""
        page_number = 1

        while True:
            page_url = f"{self.url}/page/{page_number}/"
            html = self.fetch_html(page_url)
            page_soup = bs(html, 'html.parser')

            # Verifica se há citações na página atual
            if not page_soup.find("span", class_="text"):
                break

            logger.info(f"Coletando dados da página {page_number}")
            self.fetch_quotes_on_page(page_url)
            page_number += 1
            
            if page_number == quantity_page:
                break
            
        if save_json:
            self.save_data_as_json()
        if save_xlsx:
            self.save_data_as_xlsx()
            
        return self.quotes_data

    def show_dataframe(self) -> pd.DataFrame:
        """Retornar visualização em Dataframe"""
        return pd.DataFrame(self.quotes_data)
    
    def save_data_as_json(self) -> bool:
        """Salvar Json"""
        file_path = 'media/quotes_data.json'
        with open(file_path, 'w', encoding="utf-8") as json_file:
            json.dump(self.quotes_data, json_file, indent=4, ensure_ascii=False)
        logger.success("Dados salvos em JSON.")
        notify.objects.create(title="Dados salvos em no formato JSON", 
                              description=f"Foram salvos todos os dados rapados do site: {self.url}")

    def save_data_as_xlsx(self) -> bool:
        """Salvar Xlsx"""
        file_path = 'media/quotes_data.xlsx'
        df = pd.DataFrame(self.quotes_data)
        df.to_excel(file_path, index=False)
        logger.success(f"Dados salvos em XLSX: {file_path}")
        notify.objects.create(title="Dados salvos em no formato XLSX", 
                              description=f"Foram salvos todos os dados rapados do site: {self.url}")
