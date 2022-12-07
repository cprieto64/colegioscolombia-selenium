import csv

import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import requests
from bs4 import BeautifulSoup 
from lxml import html
from lxml import etree
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib

productos = []


client = MongoClient('mongodb+srv://user:password@cluster0.mamup.mongodb.net')
db = client['colegios-colombia']

try:
            
    for i in range(15,34):
        
        # options = webdriver.ChromeOptions()
        # options.add_argument('--start-maximized')
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        
        # Headless
        options = Options()
        options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


        url = f"https://www.colegioscolombia.com/colegios_por_ciudad.php?812035190"
        driver.get(url)
        
        departamento = driver.find_element(By.XPATH, f'//div[@class="sidebar-widget category-posts"]/ul[@class="list-unstyled list-cat"]/li[{i}]')
        
        departamento = departamento.text
        departamento = departamento.replace("Colegios en", "")
        departamento = departamento.replace("2022", "")
        num_departamentos = departamento.split()
        num_departamentos = num_departamentos[-1]
        departamento = departamento.replace(num_departamentos, "")
        departamento = departamento.strip()
        # print(departamento)
        
        ciudades = driver.find_elements(By.XPATH, f'//div[@class="sidebar-widget category-posts"]/ul[@class="list-unstyled list-cat"]/ul[{i}]/li')
        

        for ciudad in ciudades:
            lista_urls = []
            link = ciudad.find_element(By.XPATH, "./a").get_attribute('href')
            # print(link)
            ciudad = ciudad.text
            ciudad = ciudad.strip()     
            #print(f"1", ciudad)
            ciudad = ciudad.replace("Colegios en", "")
            #print("2", ciudad)
            num_colegios = ciudad.split()
            # print("3", num_colegios)
            num_colegios = num_colegios[-1]
            num_colegios = num_colegios.replace("(","")
            num_colegios = num_colegios.replace(")","")
            # print(num_colegios)
            # print("4", num_colegios)
            ciudad = ciudad.replace(num_colegios, "")
            #print("5", ciudad)
            ciudad = ciudad.strip()
            ciudad = ciudad.replace("(","")
            ciudad = ciudad.replace(")","")
            ciudad = ciudad.strip()
            # ciudad = ciudad.replace(" ", "-").lower()        
            col = db['colegios']
            #print(num_colegios)
            pagerange = round(int(num_colegios)/10)+2

            for i in range(1, pagerange):
                url = f"{link}?pagina={i}"
                server = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
                }
                respuesta = requests.get(url, headers = server)
                parseador = BeautifulSoup(respuesta.text, features="lxml")

                resultados = parseador.find_all('div', class_="property")

                for resultado in resultados:
                    producto = {}
                    try:
                        nombre = resultado.find(class_="title").text
                        nombre = nombre.strip()
                        telefono = resultado.findAll('h6')[2].text
                        telefono = telefono.strip()

                        colegio_id = nombre + ciudad
                        #print(colegio_id)
                        colegio_id_hash = hashlib.md5(colegio_id.encode('utf-8')).hexdigest()
                        #print(colegio_id_hash)

                        get_item_id = col.find_one({'colegio_id' : colegio_id_hash}, {'_id': 1})
                        
                        if get_item_id is not None:
                            get_item_id = get_item_id["_id"]
                            get_item_id = col.find_one({'_id': ObjectId(get_item_id) })           
                            get_nombre = get_item_id["colegio_id"]
                            print(f"DUPLICATED: {nombre} - {ciudad} - {departamento}")                            
                            

                            col.update_one({
                                'colegio_id': colegio_id_hash
                            }, {
                            '$set': {
                                'colegio_id': colegio_id_hash,
                                'nombre': nombre,
                                'telefono': telefono,
                                'departamento': departamento,
                                'ciudad': ciudad,
                                'source': url,
                                }
                            }, upsert=True)
                        else:
                            print(f"SAVED: {nombre} - {ciudad} - {departamento}")
                            col.update_one({
                                'colegio_id': colegio_id_hash
                            }, {
                            '$set': {
                                'colegio_id': colegio_id_hash,
                                'nombre': nombre,
                                'telefono': telefono,
                                'departamento': departamento,
                                'ciudad': ciudad,
                                'source': url, 
                                }
                            }, upsert=True)
                    except Exception as e:
                        print(e)
                        driver.quit()
                print(f"Sleeping for 10 seconds: last url was {url}")
                time.sleep(15)
        driver.quit()
except Exception as e:
    print(e)
    driver.quit()

