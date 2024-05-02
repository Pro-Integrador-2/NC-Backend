import requests
from bs4 import BeautifulSoup
def scrap_NoticiasUno():
    newsInformation= []
    response = requests.get("https://www.noticiasuno.com/category/nacional/")
    if response.status_code == 200:
        # Parsea el contenido HTML de la página usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        body = soup.findAll('div', class_="td_module_10 td_module_wrap td-animation-stack")
        for index, noticia in enumerate(body):
            title_tag = noticia.find('h3', class_='entry-title td-module-title')
            if title_tag:
                title = title_tag.text.strip()
                newsInformation.append({"title": title})
                print(index, title)
            else:
                print(index, "Título no encontrado")

    else:
        print('Error al realizar la solicitud HTTP:', response.status_code)

scrap_NoticiasUno()