import unittest
from scraper import Scraper
import json


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_en_tr_street(self):
        expected_response = {
            "word": "street",
            "from_language": "en",
            "to_language": "es",
            "meanings": [
                {
                    "etymology": "Del ingl\u00e9s antiguo str\u00e6t.",
                    "definitions": [],
                    "part_of_speech": "sustantivo"
                },
                {
                    "etymology": None,
                    "definitions": [
                        {
                            "text": "Propio o relacionado con la calle.",
                            "examples": []
                        },
                        {
                            "text": "Callejero.",
                            "examples": []
                        },
                        {
                            "text": "De la ropa que se puede usar cotidianamente.",
                            "examples": []
                        },
                        {
                            "text": "De un precio que es del mercado detallista.",
                            "examples": []
                        }
                    ],
                    "part_of_speech": "adjetivo"
                }
            ]
        }
        response = Scraper('en', 'es').scrape('street')
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
