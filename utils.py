import requests
from bs4 import BeautifulSoup
def scrap_WRadio():
    newsInformation= []
    response = requests.get("https://www.wradio.com.co/actualidad/")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.findAll('article')
        for index, noticia in enumerate(body):
            header_tag = noticia.find('h3')
            news_title = header_tag.text.strip() if header_tag else ""
            news_link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else ""
            news_link ="https://www.wradio.com.co/actualidad"+news_link if news_link else ""
            image_tag = noticia.find('img')
            image_link = image_tag['src'] if image_tag else ""
            description_tag = noticia.find('p', class_='ent')
            description = description_tag.text.strip() if description_tag else ""

            if news_link != "":
                response_news = requests.get(news_link)
                soup_news = BeautifulSoup(response_news.text, 'html.parser')
                paragraphs = soup_news.find('div', class_='cnt-txt').find_all('p')
                news_text = "\n".join([p.text if p.text != "Lea también:" else "" for p in paragraphs])

            newsInformation.append({"title": news_title, "news_link": news_link, "image": image_link, "description": description, "tag": "Izquierda", "media": "W Radio" , "news_text": news_text})
    else:
        print('Error al realizar la solicitud HTTP:', response.status_code)
    return newsInformation

