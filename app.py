from flask import Flask, jsonify
from flask_cors import CORS
from utils import scrap_WRadio, scrap_LaSillaVacia

app = Flask(__name__)
CORS(app)


@app.route('/news/w-radio', methods=['GET'])
def get_news_WRadio():
    news = scrap_WRadio()
    return jsonify(news)

@app.route('/news/la-silla-vacia', methods=['GET'])
def get_news_LaSillaVacia():
    news = scrap_LaSillaVacia()
    return jsonify(news)

if __name__ == '__main__':
    app.run(debug=True)