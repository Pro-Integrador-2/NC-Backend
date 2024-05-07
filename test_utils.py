import unittest
import requests_mock
from utils import scrap_WRadio, scrap_LaSillaVacia, scrap_noticiasCaracol, scrap_revistaSemana, geminiNoticias

class TestScrapingFunctions(unittest.TestCase):

    @requests_mock.Mocker()
    def test_scrap_WRadio_empty_response(self, mock):
        mock.get("https://www.wradio.com.co/actualidad/", text="")
        result = scrap_WRadio()
        self.assertEqual(len(result), 0, "Debe manejar respuestas vacías correctamente")

    @requests_mock.Mocker()
    def test_scrap_LaSillaVacia_error_handling(self, mock):
        mock.get("https://www.lasillavacia.com/category/en-vivo/", status_code=500)
        result = scrap_LaSillaVacia()
        self.assertEqual(len(result), 0, "Debe manejar errores HTTP correctamente")

    def test_geminiNoticias_format_check(self):
        input_news = [{'title': 'Noticia 1', 'link': 'http://example.com', 'image': '', 'description': 'esta es una prueba de funcionamiento del api, devuelve una lista con una noticia de prueba', 'tag': '', 'media': '', 'text': 'Texto de prueba'}]
        output_news = geminiNoticias(input_news)
        self.assertIsInstance(output_news, str, "Debe devolver una lista en str")
        self.assertIn('[', output_news[0], "Debe procesar y devolver noticias")
        self.assertIn(']', output_news[-1], "Debe procesar y devolver noticias")

if __name__ == '__main__':
    unittest.main()
