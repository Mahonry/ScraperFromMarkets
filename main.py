import argparse
from common import config
import logging #Modulo para imprimir en consola
import re
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError
import datetime
import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from utils import get_random_agent

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
news_site_uid = 'chedrahui' #Prueba con el primer elementos del yaml

class spidermart(scrapy.Spider):


    name = 'Scraping de arroz'
    allowed_domains = [config()['news_sites'][news_site_uid]['allowed_domains']]

    custom_settings = {'FEED_FORMAT':'json',
                      'FEED_URI':'resultados.json',
                      'FEED_EXPORT_ENCODING': 'utf-8',
                      'USER_AGENT': get_random_agent()}

    start_urls = [config()['news_sites'][news_site_uid]['start_url']]



    def parse(self, response):

         productos = response.xpath(config()['news_sites'][news_site_uid]['queries']['productos']).getall()
         for producto in productos:
             yield response.follow(producto, callback = self.parse_producto)
        
         next_page = response.xpath(config()['news_sites'][news_site_uid]['queries']['next_page']).get()
         if next_page is not None:
             yield response.follow(next_page, callback = self.parse)
        
    def parse_producto(self, response):

        nombre = response.xpath(config()['news_sites'][news_site_uid]['queries']['nombre']).get()
        precio = response.xpath(config()['news_sites'][news_site_uid]['queries']['precio']).get()
        codigo = response.xpath(config()['news_sites'][news_site_uid]['queries']['codigo']).get()

        yield {'url':response.url,
              'nombre':nombre,
              'precio':precio.replace('\t','').replace('\n',''),
              'codigo':codigo
        }

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(spidermart)
    process.start()