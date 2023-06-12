import unittest
from unittest.mock import patch

from scraper import Scraper
import json

from tests.mock import mock_get_html


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    @patch('scraper.scraper.get_html', side_effect=mock_get_html)
    def test_en_es_street(self, _):
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
            ],
            "pronunciation": [
                {
                    "type": "Audio",
                    "values": [
                        {
                            "type": "audio/ogg; codecs=\"vorbis\"",
                            "value": "//upload.wikimedia.org/wikipedia/commons/6/6e/En-us-street.ogg"
                        },
                        {
                            "type": "audio/mpeg",
                            "value": "//upload.wikimedia.org/wikipedia/commons/transcoded/6/6e/En-us-street."
                                     "ogg/En-us-street.ogg.mp3"
                        }
                    ]
                }
            ]
        }
        response = Scraper('en', 'es').scrape('street')
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
