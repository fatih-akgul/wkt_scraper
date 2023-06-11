import unittest
from unittest.mock import patch

from scraper import Scraper
from tests.mock import mock_get_html


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    @patch('scraper.scraper.get_html', side_effect=mock_get_html)
    def test_en_en_complicated(self, _):
        expected_response = {
            "word": "complicated",
            "from_language": "en",
            "to_language": "en",
            "meanings": [
                {
                    "etymology": None,
                    "definitions": [
                        {
                            "text": "Difficult or convoluted.",
                            "examples": [
                                {
                                    "example": "It seems this complicated situation will not blow over soon.",
                                    "translation": None
                                }
                            ]
                        },
                        {
                            "text": "(biology) Folded longitudinally (as in the wings of certain insects).",
                            "examples": []
                        }
                    ],
                    "part_of_speech": "adjective",
                    "metadata": "complicated (comparative more complicated, superlative most complicated)",
                    "antonyms": [
                        "simple"
                    ],
                    "derived_terms": [
                        "complicated fracture"
                    ]
                },
                {
                    "etymology": None,
                    "definitions": [
                        {
                            "text": "simple past tense and past participle of complicate",
                            "examples": [
                                {
                                    "example": "The process of fixing the car engine was complicated by the lack of "
                                               "tools.",
                                    "translation": None
                                }
                            ]
                        }
                    ],
                    "part_of_speech": "verb",
                    "metadata": "complicated",
                }
            ],
            "pronunciation": [
                {
                    "type": "IPA",
                    "values": [
                        {
                            "type": "General American",
                            "value": "/\u02c8k\u0251mpl\u026ake\u026at\u026ad/"
                        },
                        {
                            "type": "Received Pronunciation",
                            "value": "/\u02c8k\u0252mpl\u026ake\u026at\u026ad/"
                        }
                    ]
                },
                {
                    "type": "Hyphenation",
                    "values": [
                        {
                            "type": "Hyphenation",
                            "value": "com\u2027pli\u2027cat\u2027ed"
                        }
                    ]
                },
                {
                    "type": "Audio (US)",
                    "values": [
                        {
                            "type": "audio/ogg; codecs=\"vorbis\"",
                            "value": "//upload.wikimedia.org/wikipedia/commons/7/72/En-us-complicated.ogg"
                        },
                        {
                            "type": "audio/mpeg",
                            "value": "//upload.wikimedia.org/wikipedia/commons/transcoded/7/72/En-us-complicated.ogg/En-us-complicated.ogg.mp3"
                        }
                    ]
                }
            ]
        }
        response = Scraper('en', 'en').scrape('complicated')

        import json
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
