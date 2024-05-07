import os

import requests
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
from bs4 import BeautifulSoup
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

new_diccionario = {
    "title": "",
    "link": "",
    "image": "",
    "description": "",
    "tag": "",
    "media": "",
    "text": ""
}


def link_exists(news_list, link):
    """Verifica si un enlace ya existe en la lista de noticias."""
    return any(news["link"] == link for news in news_list)


def scrap_WRadio(limit=15):
    """
        Realiza web scraping a la página de W Radio y extrae las noticias más recientes.
        Devuelve una lista de noticias con título, enlace, imagen, descripción, texto completo y etiqueta.
    """
    newsInformation = []
    try:
        response = requests.get("https://www.wradio.com.co/actualidad/")
        response.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.findAll('article')

        for noticia in body:
            header_tag = noticia.find('h3')
            news_title = header_tag.text.strip() if header_tag else ""
            news_link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else ""
            news_link = "https://www.wradio.com.co" + news_link if news_link else ""
            image_tag = noticia.find('img')
            image_link = image_tag['src'] if image_tag else ""
            description_tag = noticia.find('p', class_='ent')
            description = description_tag.text.strip() if description_tag else ""

            if news_link:
                response_news = requests.get(news_link)
                response_news.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito
                soup_news = BeautifulSoup(response_news.text, 'html.parser')
                paragraphs = soup_news.find('div', class_='cnt-txt')
                if paragraphs:
                    paragraphs = paragraphs.find_all('p')
                    news_text = "\n".join([p.text if p.text != "Lea también:" else "" for p in paragraphs])
                    if news_text:
                        newsInformation.append(
                            {"title": news_title, "link": news_link, "image": image_link,
                             "description": description, "tag": "Izquierda",
                             "media": "W Radio", "text": news_text})
                        if len(newsInformation) >= limit:
                            break  # Detener el bucle si alcanzamos el límite
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")

    return newsInformation[:limit]


def scrap_LaSillaVacia():
    """
        Realiza web scraping a la página de La Silla Vacía y extrae las noticias más recientes.
        Devuelve una lista de noticias con título, enlace, imagen, descripción, texto completo y etiqueta.
    """
    newsInformation = []
    try:
        response = requests.get("https://www.lasillavacia.com/category/en-vivo/")
        response.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('main', class_='site-main').findAll('article')

        for noticia in body:
            header_tag = noticia.find('h2', class_='entry-title')
            news_title = header_tag.text.strip() if header_tag else ""
            news_link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else ""
            image_tag = noticia.find('img')
            image_link = image_tag['src'] if image_tag else ""
            description_tag = noticia.find('div', class_='entry-content').find('p')
            description = description_tag.text.strip() if description_tag else ""

            if news_link:
                response_news = requests.get(news_link)
                response_news.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito
                soup_news = BeautifulSoup(response_news.text, 'html.parser')
                paragraphs = soup_news.find('div', class_='entry-content').find_all('p')
                news_text = "\n".join([p.text.strip() for p in paragraphs if p.text != "Lea también:"])
                if news_text:
                    newsInformation.append(
                        {"title": news_title, "link": news_link, "image": image_link,
                         "description": description, "tag": "Centro Izquierda",
                         "media": "La Silla Vacía", "text": news_text})
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")

    return newsInformation


def scrap_noticiasCaracol(limit=10):
    """
       Realiza web scraping a la página de Noticias Caracol y extrae las noticias más recientes.
       Devuelve una lista de noticias con título, enlace, imagen, descripción, texto completo y etiqueta.
    """
    newsInformation = []
    try:
        response = requests.get("https://www.noticiascaracol.com/noticias")
        response.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('main', class_='SectionPage-main').findAll('div', class_='PromoB-content')

        for noticia in body:
            header_tag = noticia.find('h2', class_='PromoB-title')
            news_title = header_tag.text.strip() if header_tag else ""
            news_link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else ""
            image_tag = noticia.find('img', class_='Image')
            image_link = image_tag['data-src'] if image_tag else ""
            description_tag = noticia.find('h3', class_='PromoB-description')
            description = description_tag.text.strip() if description_tag else ""

            if news_link:
                response_news = requests.get(news_link)
                response_news.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito
                soup_news = BeautifulSoup(response_news.text, 'html.parser')
                paragraphs = soup_news.find('div', class_='RichTextBody').find_all('p')
                news_text = "\n".join([p.text.strip() for p in paragraphs if p.text != "Lea también:"])
                if news_text:
                    newsInformation.append(
                        {"title": news_title, "link": news_link, "image": image_link,
                         "description": description, "tag": "Centro Derecha",
                         "media": "Noticias Caracol", "text": news_text})
                    if len(newsInformation) >= limit:
                        break  # Detener el bucle si alcanzamos el límite
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")

    return newsInformation[:limit]


def scrap_revistaSemana(limit=10):
    """
        Realiza web scraping a la página de Revista Semana y extrae las noticias más recientes.
        Devuelve una lista de noticias con título, enlace, imagen, descripción, texto completo y etiqueta.
    """
    newsInformation = []
    try:
        response = requests.get("https://www.semana.com/actualidad")
        response.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('main', class_='main-section').findAll('div', class_='grid-item')

        for noticia in body:
            header_link = noticia.find('div', class_='card')
            link = "https://www.semana.com" + header_link.find('a')['href'] if header_link and header_link.find(
                'a') else ""
            if link:
                response_news = requests.get(link)
                response_news.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito
                soup_news = BeautifulSoup(response_news.text, 'html.parser')
                new = {
                    "title": soup_news.find('h1', class_='text-smoke-700').text.strip(),
                    "link": link,
                    "image": soup_news.find('img')['src'],
                    "description": soup_news.find('div', class_='mx-auto max-w-[968px]').find('p').text.strip(),
                    "tag": "Derecha",
                    "media": "Revista Semana",
                    "text": "\n".join([p.text.strip() for p in soup_news.find('div', class_='paywall').find_all('p') if
                                       p.text != "Lea también:"])
                }
                if new["text"] and not link_exists(newsInformation, new["link"]):
                    newsInformation.append(new)
                    if len(newsInformation) >= limit:
                        break  # Detener el bucle si alcanzamos el límite
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")

    return newsInformation[:limit]


def geminiNoticias(news):
    """
        Utiliza el modelo generativo de IA de Google para crear versiones imparciales de las noticias proporcionadas.
        Analiza el sesgo político y devuelve las noticias imparcializadas junto con su clasificación.
    """
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Voy a darte un arreglo de objectos los cuales son noticias y quiero que para cada noticia
    me crees otra de una manera imparcial evitando el sesgo politico. 
    Junto con ello que me identifiques si es Neutral, Parcial o Imparcial dentro del atrubuto "tag".

    Este es la estructura que tiene cada noticia:
    {new_diccionario}

    Quiero que me devuelves las noticias en un arreglo de la misma manera como te las doy.

    Estas son las noticas para imparcializar: {news}
    """
    response = model.generate_content(prompt)
    return response.text
