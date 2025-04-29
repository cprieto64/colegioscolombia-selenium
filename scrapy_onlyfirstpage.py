from gc import callbacks
import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scraper_api import ScraperAPIClient
from pymongo import MongoClient
import time

class Empresa(Item):
    nombre = Field()
    telefono = Field()

client = MongoClient('localhost')
db = client['colegios-colombia']
col = db['ciudad']['bogota']

class PaginasAmarillasCrawler(CrawlSpider):
    name = 'paginasamarillas'
    custom_settings = {        
    "DOWNLOADER_MIDDLEWARES": { # pip install Scrapy-UserAgents and pip install scrapy_proxy_pool and pip install scrapy-user-agents
        'scrapyx_scraperapi.ScraperApiProxyMiddleware': 610,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    },    
    "USER_AGENTS": [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        # chrome
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        # chrome
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',  # firefox
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        # chrome
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
        # chrome
    ],
    # pip install scrapyx-scraperapi-v2 and pip install scraperapi-sdk https://snyk.io/advisor/python/scrapyx-scraperapi-v2
    "SCRAPERAPI_ENABLED" : False,
    "SCRAPERAPI_KEY" : 'c93021d36148fad4a9a44d9cc46c803d',
    "SCRAPERAPI_RENDER" : False,
    "SCRAPERAPI_PREMIUM" : False,
    "SCRAPERAPI_COUNTRY_CODE": 'US',
    
    #"PROXY_POOL_ENABLED" : True,
    #'LOG_LEVEL' : 'ERROR',

    'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',

    'CLOSESPIDER_PAGECOUNT': 2,
    #'CONCURRENT_REQUESTS': 1,   
    #'FEED_EXPORT_FIELDS': ['titulo', 'telefono', 'actividad', 'nit', 'ciudad', 'direccion'],  # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    'FEED_EXPORT_ENCODING': 'utf-8'
    
    }

    allowed_domains = ['colegioscolombia.com']
    start_urls = ['https://www.colegioscolombia.com/colegios/Mejores_colegios_BOGOTA.php?pagina=1']

    download_delay = 1

    # rules = {
	# 	# Para cada item
	# 	Rule(LinkExtractor(allow = (), restrict_xpaths = ("//a[contains(@aria-label, 'Next')]"))),
	# 	Rule(LinkExtractor(allow =(), restrict_xpaths = ("//div[@class='property']")),
	# 						callback = 'parse_item', follow = False)
	# }

    # rules = {
	# 	# Para cada item
    #     # Rule(LinkExtractor(allow = (), restrict_xpaths = ("//a[contains(@aria-label, 'Next')]"))),
	# 	Rule(LinkExtractor(allow =(), restrict_xpaths = ("//a[contains(@aria-label, 'Next')]")),
	# 						callback = 'parse_items', follow = True)
	# }

    rules = {
        Rule(
            LinkExtractor(
                allow=r'pagina=\d+'
            ), follow = True, callback = "parse_items"
        )
    }
    
    def parse_items(self, response):
        """Parses and extracts information from a web page response, specifically targeting company details.
        
        Args:
            self: The instance of the class containing this method.
            response (Response): The HTTP response object containing the web page content to be parsed.
        
        Returns:
            None: This method doesn't return a value, but updates a database collection with the extracted information.
        """
        print("Estoy entrando en la funcion?")      
        sel = Selector(response)
        empresas = sel.xpath('//div[@class="property"]')
        for empresa in empresas:

            nombre = empresa.xpath('.//h6[@class="title"]/a/text()').get()
            print(nombre)
            
            
            telefono = empresa.xpath('.//h6[@itemprop="telephone"]/i/following-sibling::text()[1]').get()
            print(telefono)
           
            # website = empresa.xpath('.//a[@class="webLink"]/text()').get()
            # if website is None:
            #     website = "N/A"
            # else:
            #     website = website.strip()
            # ciudad = empresa.xpath(".//span[@class='city']/text()").get()
            # if ciudad is None:
            #     ciudad = "N/A"
            # else:
            #     ciudad = ciudad.strip()
            # direccion = empresa.xpath(".//span[@class='directionFig']/text()").get()
            # if direccion is None:
            #     direccion = "N/A"
            # else:
            #     direccion = direccion.strip()
            # slogan = empresa.xpath('.//div[contains(@class, "slogan")]/p/text()').get()
            # if slogan is None:
            #     slogan = "N/A"
            # else:
            #     slogan = slogan.strip()
            
            #print(nombre, telefono)
            
            col.update_one({
                'Empresa': nombre
            }, {
            '$set': {
                'Empresa': nombre,
                'Telefono': telefono,
                # 'Website': website,
                # 'Ciudad': ciudad,
                # 'Direccion': direccion,
                # 'Slogan': slogan 
                }
            }, upsert=True) 
            


# scrapy runspider main.py
# scrapy runspider paginas_amarillas_scrapy_restaurantes_selector.py -o paginas_amarillas_scrapy_restaurantes.json -t json
# scrapy runspider paginas_amarillas_scrapy_restaurantes_selector.py -o paginas_amarillas_scrapy_restaurantes.csv -t csv
