import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from time import sleep

class Magalu:

    def __init__(self):
        print("Iniciando o navegador Google Chrome")
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('test-type')
        options.add_argument("disable-popup-blocking")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument('--start-maximized --disable-notifications --silent')
        options.add_argument('--incognito')
        driver_manager = ChromeDriverManager().install()
        s = Service(driver_manager)
        self.driver = webdriver.Chrome(service=s, options=options)
    
    def smartfones(self):
        self.driver.get("https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/?page=1")
        sleep(3)
        links = self.driver.find_elements(by=By.TAG_NAME,value='a')
        urls = []
        for href in links:
            h_ref = href.get_attribute('href')
            if h_ref is None:
                pass
            elif h_ref.startswith("https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/?page="):
                urls.append(h_ref)
        print(f"Estes foram as url's encontradas: {urls}")
        return urls[-1]
    
    def coletar_dados(self,url):
        self.driver.get(url)
        sleep(3)
        source = bs(self.driver.page_source,'html.parser')
        #original_price = source.find_all("p", attrs={"class": "sc-kDvujY gcLiKJ sc-dcntqk cJvvNV"})
        description = source.find_all("h2", attrs={"class": "sc-eQVdPn kMrHVo"})
        price_value = source.find_all("p", attrs={"class": "sc-kDvujY jDmBNY sc-ehkVkK kPMBBS"})
        print(f"Foram encontradas {len(description)} produtos com seus respectivos valores")
        prod = []
        preco = []
        for i in range(len(description)):
            print(description[i].text, price_value[i].text)
            prod.append(description[i].text)
            preco.append(price_value[i].text)
        return prod,preco

    def construir_planilha(self,dados):
        df = pd.DataFrame(data=dados)
        df.to_excel("Webscraping_magalu.xlsx",index=False)

    def fechar_navegador(self):
        return self.driver.close()

if __name__ == '__main__':
    magalu = Magalu()
    ultima_url = magalu.smartfones()
    number_url = ultima_url.split("=")[1]
    produtos = {"Descrição":[],"Preço":[]}
    for i in range(1,number_url,1):
        colect = magalu.coletar_dados(f'https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/?page={i}')
        dados1 = colect[0]
        for j in dados1:
            produtos["Descrição"].append(j)
        dados2 = colect[1]
        for k in dados2:
            produtos["Preço"].append(k)
    magalu.fechar_navegador()
    magalu.construir_planilha(produtos)
