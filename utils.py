import requests
from bs4 import BeautifulSoup


def link_exists(news_list, link):
    return any(news["link"] == link for news in news_list)


def scrap_WRadio():
    newsInformation = []
    response = requests.get("https://www.wradio.com.co/actualidad/")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.findAll('article')
        for index, noticia in enumerate(body):
            header_tag = noticia.find('h3')
            news_title = header_tag.text.strip() if header_tag else ""
            news_link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else ""
            news_link = "https://www.wradio.com.co" + news_link if news_link else ""
            image_tag = noticia.find('img')
            image_link = image_tag['src'] if image_tag else ""
            description_tag = noticia.find('p', class_='ent')
            description = description_tag.text.strip() if description_tag else ""
            news_text = ""
            if news_link != "":
                response_news = requests.get(news_link)
                soup_news = BeautifulSoup(response_news.text, 'html.parser')
                paragraphs = soup_news.find('div', class_='cnt-txt')
                if paragraphs:
                    paragraphs = paragraphs.find_all('p')
                    news_text = "\n".join([p.text if p.text != "Lea también:" else "" for p in paragraphs])
            if news_text:
                newsInformation.append(
                    {"title": news_title, "link": news_link, "image": image_link, "description": description,
                     "tag": "Izquierda", "media": "W Radio", "text": news_text})
    else:
        print('Error al realizar la solicitud HTTP:', response.status_code)
    return newsInformation


def scrap_LaSillaVacia():
    newsInformation = []
    response = requests.get("https://www.lasillavacia.com/category/en-vivo/")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('main', class_='site-main').findAll('article')
        for index, noticia in enumerate(body):
            header_tag = noticia.find('h2', class_='entry-title')
            news_title = header_tag.text.strip() if header_tag else ""
            news_link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else ""
            image_tag = noticia.find('img')
            image_link = image_tag['src'] if image_tag else ""
            description_tag = noticia.find('div', class_='entry-content').find('p')
            description = description_tag.text.strip() if description_tag else ""
            news_text = ""

            if news_link:
                response_news = requests.get(news_link)
                if response_news.status_code == 200:
                    soup_news = BeautifulSoup(response_news.text, 'html.parser')
                    paragraphs = soup_news.find('div', class_='entry-content').find_all('p')
                    news_text = "\n".join([p.text.strip() for p in paragraphs if p.text != "Lea también:"])
            if news_text:
                newsInformation.append(
                    {"title": news_title, "link": news_link, "image": image_link, "description": description,
                     "tag": "Centro Izquierda", "media": "La Silla Vacía", "text": news_text})
    else:
        print('Error al realizar la solicitud HTTP:', response.status_code)
    return newsInformation


def scrap_noticiasCaracol():
    newsInformation = []
    response = requests.get("https://www.noticiascaracol.com/ahora")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('main', class_='SectionPage-main').findAll('div', class_='PromoB-content')
        for index, noticia in enumerate(body):
            header_tag = noticia.find('h2', class_='PromoB-title')
            news_title = header_tag.text.strip() if header_tag else ""
            news_link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else ""
            image_tag = noticia.find('img', class_='Image')
            image_link = image_tag['data-src'] if image_tag else ""
            description_tag = noticia.find('h3', class_='PromoB-description')
            description = description_tag.text.strip() if description_tag else ""
            news_text = ""

            if news_link:
                response_news = requests.get(news_link)
                if response_news.status_code == 200:
                    soup_news = BeautifulSoup(response_news.text, 'html.parser')
                    paragraphs = soup_news.find('div', class_='RichTextArticleBody-body RichTextBody').find_all('p')
                    news_text = "\n".join([p.text.strip() for p in paragraphs if p.text != "Lea también:"])
            if news_text:
                newsInformation.append(
                    {"title": news_title, "link": news_link, "image": image_link, "description": description,
                     "tag": "Centro Derecha", "media": "Noticias Caracol", "text": news_text})
    else:
        print('Error al realizar la solicitud HTTP:', response.status_code)
    return newsInformation


def scrap_revistaSemana():
    newsInformation = []
    response = requests.get("https://www.semana.com/actualidad")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('main', class_='main-section').findAll('div', class_='grid-item')
        for index, noticia in enumerate(body):
            header_link = noticia.find('div', class_='card')
            link = "https://www.semana.com" + header_link.find('a')['href'] if header_link and header_link.find(
                'a') else ""
            if link != "":
                response_news = requests.get(link)
                if response_news.status_code == 200:
                    new = {
                        "title": "",
                        "link": "",
                        "image": "",
                        "description": "",
                        "tag": "Derecha",
                        "media": "Revista Semana",
                        "text": ""
                    }
                    soup_news = BeautifulSoup(response_news.text, 'html.parser')
                    new["link"] = link
                    header_tag = soup_news.find('h1', class_='text-smoke-700')
                    new["title"] = header_tag.text.strip() if header_tag else ""
                    image_tag = soup_news.find('img')
                    new["image"] = image_tag['src'] if image_tag else ""
                    description_tag = soup_news.find('div', class_='mx-auto max-w-[968px]').find('p')
                    new["description"] = description_tag.text.strip() if description_tag else ""
                    paragraphs = soup_news.find('div', class_='paywall').find_all('p')
                    new["text"] = "\n".join([p.text.strip() for p in paragraphs if p.text != "Lea también:"])
            if new["text"] and not link_exists(newsInformation, new["link"]):
                newsInformation.append(new)
    else:
        print('Error al realizar la solicitud HTTP:', response.status_code)
    return newsInformation
