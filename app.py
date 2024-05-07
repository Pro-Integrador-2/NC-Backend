from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import scrap_WRadio, scrap_LaSillaVacia, scrap_noticiasCaracol, scrap_revistaSemana, geminiNoticias

app = Flask(__name__)
CORS(app)


@app.route('/news/w-radio', methods=['GET'])
def get_news_WRadio():
    """Endpoint que realiza web scraping a la página web de W Radio y retorna la lista de las noticias más recientes."""
    news = scrap_WRadio()
    return jsonify(news)

@app.route('/news/la-silla-vacia', methods=['GET'])
def get_news_LaSillaVacia():
    """Endpoint que realiza web scraping a la página web de La Silla Vacía y retorna la lista de las noticias más recientes."""
    news = scrap_LaSillaVacia()
    return jsonify(news)

@app.route('/news/noticias-caracol', methods=['GET'])
def get_news_noticiasCaracol():
    """Endpoint que realiza web scraping a la página web de Noticias Caracol y retorna la lista de las noticias más recientes."""
    news = scrap_noticiasCaracol()
    return jsonify(news)

@app.route('/news/revista-semana', methods=['GET'])
def get_news_revistaSemana():
    """Endpoint que realiza web scraping a la página web de Revista Semana y retorna la lista de las noticias más recientes."""
    news = scrap_revistaSemana()
    return jsonify(news)


@app.route('/news/procesar-noticias', methods=["POST"])
def post_news_procesarNoticias():
    """Endpoint que procesa una lista de noticias para imparcializar su contenido y retorna las noticias procesadas."""
    news = request.get_json()
    impartialNews = geminiNoticias(news['news'])
    return jsonify({"response": impartialNews})

if __name__ == '__main__':
    app.run()