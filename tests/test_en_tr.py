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
    def test_en_tr_street(self, _):
        expected_response = {
            "word": "street",
            "from_language": "en",
            "to_language": "tr",
            "meanings": [
                {
                    "etymology": None,
                    "definitions": [
                        {
                            "text": "[1] (ula\u015f\u0131m) cadde",
                            "examples": []
                        }
                    ],
                    "part_of_speech": "ad",
                    "metadata": "street (\u00e7o\u011fulu streets)",
                }
            ],
            "pronunciation": [],
        }
        response = scrape('en', 'tr', 'street')
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)

    @patch('scraper.scraper.get_html', side_effect=mock_get_html)
    def test_en_tr_car(self, _):
        expected_response = {
            "word": "car",
            "from_language": "en",
            "to_language": "tr",
            "meanings": [
                {
                    "etymology": 'Ana Keltçe ---> Latince carrum, carrus',
                    "definitions": [
                        {
                            "text": "(kara ula\u015f\u0131m\u0131, ta\u015f\u0131tlar) araba, oto, otomobil, makine",
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
                    "part_of_speech": "ad",
                    "metadata": "car (\u00e7o\u011fulu cars)",
                }
            ],
            "pronunciation": [],
        }
        response = scrape('en', 'tr', 'car')
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
