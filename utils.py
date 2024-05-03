import requests
from bs4 import BeautifulSoup
def scrap_WRadio():
    newsInformation= []
    response = requests.get("https://www.wradio.com.co/actualidad/")
    if response.status_code == 200:
        # Parsea el contenido HTML de la página usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        body = soup.findAll('article')
        for index, noticia in enumerate(body):
            header_tag = noticia.find('h3')
            news_title = header_tag.text.strip() if header_tag else "Título no encontrado"
            news_link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else "Enlace de noticia no encontrado"
            image_tag = noticia.find('img')
            image_link = image_tag['src'] if image_tag else "Enlace de imagen no encontrado"
            description_tag = noticia.find('p', class_='ent')
            description = description_tag.text.strip() if description_tag else "Descripción no encontrada"
            newsInformation.append({"title": news_title, "news_link": "https://www.wradio.com.co/actualidad"+news_link, "image": image_link, "description": description, "tag": "Izquierda", "media": "W Radio" })
    else:
        print('Error al realizar la solicitud HTTP:', response.status_code)
    return newsInformation

print(scrap_WRadio())