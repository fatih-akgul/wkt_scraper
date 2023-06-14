import unittest
from unittest.mock import patch

from scraper import scrape
import json

from tests.mock import mock_get_html


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    @patch('scraper.scraper.get_html', side_effect=mock_get_html)
    def test_en_es_aprender(self, _):
        expected_response = {
            "word": "aprender",
            "from_language": "es",
            "to_language": "es",
            "meanings": [
                {
                    "etymology": "Del lat\u00edn apprehend\u0115re, a su vez de ad\u00a0(\"a\") y prehend\u0115re (\"percibir, asir, agarrar\").1 Doblete del cultismo aprehender.",
                    "definitions": [
                        {
                            "text": "Adquirir conocimiento o experiencia.\nUso: se emplea tambi\u00e9n como intransitivo",
                            "examples": []
                        },
                        {
                            "text": "Tomar algo en la memoria.1\nUso: se emplea tambi\u00e9n como pronominal: aprenderse.",
                            "examples": []
                        },
                        {
                            "text": "Asir, agarrar, tomar.\nSin\u00f3nimo: prender",
                            "examples": []
                        },
                        {
                            "text": "Acompa\u00f1ado de la preposici\u00f3n \"de\" y de un nombre propio, alude el hecho de tomar como ejemplo alguna acci\u00f3n ejecutada por esa persona",
                            "examples": []
                        }
                    ],
                    "part_of_speech": "verbo\u00a0transitivo"
                }
            ],
            "pronunciation": []
        }

        response = scrape('es', 'es', 'aprender')
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
