"""
OBJETIVO: 
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX autos.
    - Aprender a realizar extracciones que requieran una accion de click para cargar datos.
    - Introducirnos a la logica de Selenium
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 23 NOVIEMBRE 2020
"""

import csv
#####
### ATENCION: OLX necesita que le demos permisos de geolocalizacion al navegador de selenium para que nos muestre los datos
### Esto lo haremos una unica vez en la primer corrida del programa. Este problema es mas comun en usuarios de MAC
#####
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# options = Options()
# options.headless = True
# driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())

productos = []


for i in range (1,10): 

    # Headless
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())

    # options = webdriver.ChromeOptions()
    # options.add_argument('--start-maximized')
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # #driver = webdriver.Chrome(ChromeDriverManager().install())

    # # Iniciarla en la pantalla 2
    # driver.set_window_position(2000, 0)
    # driver.maximize_window()
    # time.sleep(1)

    print("####################### \n  INITIALIZED SCRAPER    \n#######################") 
    
    indice=+i

    url = f"https://www.colegioscolombia.com/colegios/Mejores_colegios_BOGOTA.php?pagina={indice}"
    driver.get(url)
    print("Going into:", url)

    # productos = []

    time.sleep(5)



    scroll_pause_time = 4 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

    resultados = driver.find_elements('xpath', '//div[@class="property"]')

    for resultado in resultados:
        #print(resultado.text)
        producto = {}
        try:

            telefono = resultado.find_element('xpath', './/h6[3]')            
            telefono = telefono.text
            #print(f"el mardito tel: {telefono}")
            
            nombre = resultado.find_element('xpath', './/h6[@class="title"]/a')
            # print(type(nombre))
            nombre = nombre.text
            #print(nombre) 
            # tel = tel.strip()
            # print(tel)
            # imgurl = resultado.find_element_by_xpath('.//img')
            # imgurl = imgurl.get_attribute("src")
            # precio = resultado.find_element_by_xpath('.//span[@class="product-prices__value product-prices__value--best-price"]')
            # precio = precio.text
            # precio = precio.replace('$', '')
            # precio = precio.replace('\n', ' ')
            # discount = resultado.find_element_by_xpath('.//div[@class="flag discount-percent"]').text
        except Exception as e:
            print(e)
            # pass        

        producto["Nombre"] = nombre
        producto["Telefono"] = telefono
    #     producto["Precio"] = precio
    #     producto["URL Imagen"] = imgurl
    #     producto["Descuento"] = discount
    #     producto["Categoria"] = categoria
        productos.append(producto)
    #     print("Iterando por: ", {producto["Nombre"]})
    # #print(productos)

        time.sleep(0.5)

    driver.quit()

try:
    with open(f"colegios.csv", mode='w', newline='',
                encoding="utf-8") as f:
        #fieldnames = ["Nombre", "Precio", "Descuento", "Categoria", "URL Imagen"]
        fieldnames = ["Nombre", "Telefono"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerows(productos)
        print("Excel Document Writted")
except Exception as e:
    print(f"Error writing to csv: {e}")

    time.sleep(3)
    driver.quit()

print("####################### \n  SCRAPER FINISHED    \n#######################")