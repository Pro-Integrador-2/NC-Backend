from flask import Flask, jsonify
from flask_cors import CORS
from utils import scrap_WRadio

app = Flask(__name__)
CORS(app)


@app.route('/news/w-radio', methods=['GET'])
def get_news():
    news = scrap_WRadio()
    return jsonify(news)



if __name__ == '__main__':
    app.run(debug=True)