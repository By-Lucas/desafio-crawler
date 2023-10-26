import os
import json
import requests
import pandas as pd
from loguru import logger
from decouple import config
from bs4 import BeautifulSoup as bs


class ScraperQuotex:
    def __init__(self):
        self.url = config("URL_QUOTES")
        self.quotes_data = []
    
    def fetch_html(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception("Erro ao fazer a solicitação HTTP")

    def parse_html_with_beautifulsoup(self, html):
        soup = bs(html, 'html.parser')
        # Agora você pode usar o BeautifulSoup para extrair dados da página da web
        # Por exemplo, para obter o texto da citação:
        quote_text = soup.find("span", {"itemprop": "text"}).text
        # E para obter o autor:
        author = soup.find("small", {"class": "author"}).text
        # E assim por diante...

        # Você pode retornar os dados ou usá-los como desejar
        return quote_text, author

    
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
                logger.success('Elementro encontrado.')
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
                logger.success('Elementro encontrado.')
                return element
            
        logger.warning('O(s) elemento(s) em que fez a busca não foi encontrado.')
        return None
    
    
    def fetch_about_info(self, about_url):
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


    def fetch_quotes_on_page(self, page_url):
        """Faz solicitção diretna na url passada como prâmetro"""
        html = self.fetch_html(page_url)
        page_soup = bs(html, 'html.parser')

        elements = self.find_elements(page_soup, ("class_name", "quote"), ("css_selector", "body div.quote"))

        for element in elements:
            tag_list = []
            text = element.find("span", class_="text").text
            author = element.find("small", class_="author").text
            about_link = element.find("a")
            about = about_link.get('href')
            about_url = f"{self.url}{about}"

            tags = element.find_all("a", class_="tag")
            for tag in tags:
                tag_list.append(tag.text)

            about_info = self.fetch_about_info(about_url)
            if about_info:
                about_author, description, born, location = about_info
                quote_data = {
                    'text': text,
                    "Author": about_author.text,
                    "Born": born.text,
                    "Location": location.text,
                    "Tags": ", ".join(tag_list),
                    "Description": description.text
                }
                self.quotes_data.append(quote_data)
                
        # Após coletar todos os dados, salve-os em JSON e XLSX
        self.save_data_as_json()
        self.save_data_as_xlsx()
        
    def run(self):
        
        """Inicia o scraping e faz a paginação"""
        page_number = 1

        while True:
            page_url = f"{self.url}/page/{page_number}/"
            html = self.fetch_html(page_url)
            page_soup = bs(html, 'html.parser')

            # Verifica se há citações na página atual
            if not page_soup.find("span", class_="text"):
                break  # Sai do loop se não houver mais citações

            logger.info(f"Coletando dados da página {page_number}")
            self.fetch_quotes_on_page(page_url)
            page_number += 1
            
            if page_number == 2:
                break

    def save_data_as_json(self):
        with open('quotes_data.json', 'w', encoding="utf-8") as json_file:
            json.dump(self.quotes_data, json_file, indent=4, ensure_ascii=False)
        logger.success("Dados salvos em JSON.")

    def save_data_as_xlsx(self):
        file_path = 'quotes_data.xlsx'

        # if os.path.exists(file_path):
        #     os.remove(file_path)

        df = pd.DataFrame(self.quotes_data)
        print(df)
        df.to_excel(file_path, index=False)
        logger.success(f"Dados salvos em XLSX: {file_path}")
 
 
# Exemplo de uso
scraper = ScraperQuotex()
scraper.run()
