#---------- O código deve ser capaz de realizar as seguintes operações ----------
#Abrir o navegador: framework selenium
#Login no instagram: variáveis de ambiente
#Selecionar o perfil
#Curtir diversas fotos

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import dotenv
import os

class InstaBot():

    def __init__(self):
        print("Carregando variáveis de ambiente do programa")
        dotenv.load_dotenv(".env")
        print("Iniciando o navegador Google Chrome")
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized --disable-notifications')
        options.add_argument('--incognito')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def login_instagram(self,user,senha):
        self.driver.get("https://www.instagram.com/")
        sleep(1)
        login = self.driver.find_element(by=By.NAME,value = 'username')
        login.send_keys(user)
        password = self.driver.find_element(by=By.NAME,value = 'password')
        password.send_keys(senha)
        entrar = self.driver.find_element(by=By.XPATH,value = '//*[@id="loginForm"]/div/div[3]/button/div')
        entrar.click()
        sleep(10)
    
    def carregar_pagina(self,pagina_escolhida):
        self.driver.get(f"https://www.instagram.com/{pagina_escolhida}/")
        sleep(5)
        pics = []
        links = self.driver.find_elements(by=By.TAG_NAME,value='a')
        for link in links:
            url = link.get_attribute("href")
            if url.startswith("https://www.instagram.com/p/"):
                print(url)
                pics.append(url)
        return pics
    
    def curtida(self,url):
        self.driver.get(url)
        sleep(5)
        like = self.driver.find_elements(by=By.CLASS_NAME, value='_abl-')
        like[1].click()

if __name__ == '__main__':
    robo = InstaBot()
    insta = robo.login_instagram(os.getenv('LOGIN'),os.getenv('PASSWORD'))
    fotos = robo.carregar_pagina('mazzclub')
    for pictures in fotos:
        dar_like = robo.curtida(pictures)
