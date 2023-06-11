import unittest
from scraper import Scraper


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_es_en_aprender(self):
        expected_response = {
            "word": "aprender",
            "from_language": "es",
            "to_language": "en",
            "meanings": [
                {
                    "etymology": "Inherited from Old Spanish aprender, from Latin appr\u0113ndere, from earlier "
                                 "apprehendere. Compare the borrowed doublet aprehender. "
                                 "Cognate with English apprehend.",
                    "definitions": [
                        {
                            "text": "(transitive, intransitive) to learn (to acquire, or attempt to acquire "
                                    "knowledge or an ability to do something)",
                            "examples": []
                        },
                        {
                            "text": "(transitive, uncommon) to teach",
                            "examples": []
                        }
                    ],
                    "part_of_speech": "verb",
                    "metadata": "aprender (first-person singular present aprendo, first-person singular "
                                "preterite aprend\u00ed, past participle aprendido)"
                }
            ],
            "pronunciation": [
                {
                    "type": "IPA",
                    "values": [
                        {
                            "type": "IPA",
                            "value": "/ap\u027een\u02c8de\u027e/"
                        },
                        {
                            "type": "IPA",
                            "value": "[a.p\u027e\u1ebdn\u032a\u02c8d\u032ae\u027e]"
                        },
                        {
                            "type": "IPA",
                            "value": "-e\u027e"
                        }
                    ]
                },
                {
                    "type": "Hyphenation",
                    "values": [
                        {
                            "type": "Hyphenation",
                            "value": "a\u2027pren\u2027der"
                        }
                    ]
                },
                {
                    "type": "Audio (Colombia)",
                    "values": [
                        {
                            "type": "audio/ogg; codecs=\"vorbis\"",
                            "value": "//upload.wikimedia.org/wikipedia/commons/transcoded/6/6a/LL-Q1321_%28spa%29-"
                                     "AdrianAbdulBaha-aprender.wav/LL-Q1321_%28spa%29-AdrianAbdulBaha-aprender.wav.ogg"
                        },
                        {
                            "type": "audio/mpeg",
                            "value": "//upload.wikimedia.org/wikipedia/commons/transcoded/6/6a/LL-Q1321_%28spa%29-"
                                     "AdrianAbdulBaha-aprender.wav/LL-Q1321_%28spa%29-AdrianAbdulBaha-aprender.wav.mp3"
                        },
                        {
                            "type": "audio/wav",
                            "value": "//upload.wikimedia.org/wikipedia/commons/6/6a/LL-Q1321_%28spa%29-"
                                     "AdrianAbdulBaha-aprender.wav"
                        }
                    ]
                }
            ]
        }

        response = Scraper('es', 'en').scrape('aprender')

        import json
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
