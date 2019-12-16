import unittest
from scraper import Scraper


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_en_tr_street(self):
        expected_response = {
            "meanings": [
                {
                    "etymology": None,
                    "definitions": [
                        {
                            "text": "[1] (ula\u015f\u0131m) cadde",
                            "examples": []
                        }
                    ],
                    "part_of_speech": "ad"
                }
            ]
        }
        response = Scraper('İngilizce', 'tr').scrape('street')

        self.assertDictEqual(response, expected_response)

    def test_en_tr_car(self):
        expected_response = {
            "meanings": [
                {
                    "etymology": 'Ana Keltçe ---> Latince carrum, carrus',
                    "definitions": [
                        {
                            "text": "(kara ula\u015f\u0131m\u0131, ta\u015f\u0131tlar) araba, otomobil",
                            "examples": []
                        },
                        {
                            "text": "(Kuzey Amerika'da) tren vagonu",
                            "examples": []
                        },
                        {
                            "text": "bir asans\u00f6r, teleferik veya balonun yolcu kompart\u0131man\u0131",
                            "examples": []
                        }
                    ],
                    "part_of_speech": "ad"
                }
            ]
        }
        response = Scraper('İngilizce', 'tr').scrape('car')

        import json
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
