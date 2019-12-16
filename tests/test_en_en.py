import unittest
from scraper import Scraper


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_en_en_complicated(self):
        expected_response = {
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
                    "antonyms": [
                        "simple"
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
                    "part_of_speech": "verb"
                }
            ],
            "pronunciation": [
                {
                    "type": "IPA",
                    "values": [
                        {
                            "type": "IPA",
                            "value": "/\u02c8k\u0251mpl\u026ake\u026at\u026ad/"
                        },
                        {
                            "type": "IPA",
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
        response = Scraper('English', 'en').scrape('complicated')

        import json
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
