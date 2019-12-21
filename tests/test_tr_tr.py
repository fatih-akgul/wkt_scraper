import unittest
from scraper import Scraper


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_tr_tr_araba(self):
        expected_response = {
            "meanings": [
                {
                    "etymology": "Eski T\u00fcrk\u00e7e k\u00f6kenli bir kelimedir. Bu kelime \u00c7uva\u015f\u00e7a "
                                 "uraba veya urava tekerlek ve Mo\u011folca araa tekerlek ile ayn\u0131 k\u00f6kene "
                                 "dayanmaktad\u0131r. Bunun ispat\u0131 baz\u0131 T\u00fcrk leh\u00e7elerinde araba "
                                 "anlam\u0131nda kullan\u0131lan k\u00f6l\u00fck kelimesinin Saha "
                                 "T\u00fcrk\u00e7esinde k\u00fcl\u00fc\u00f6he tekerlek bi\u00e7iminde "
                                 "bulunmas\u0131d\u0131r. Araba kelimesi T\u00fcrk\u00e7eden \u0130ngilizce, "
                                 "Arap\u00e7a ve Rus\u00e7a gibi baz\u0131 dillere de ge\u00e7mi\u015ftir.",
                    "definitions": [
                        {
                            "text": "(kara ula\u015f\u0131m\u0131, ta\u015f\u0131tlar) tekerlekli, motorlu veya "
                                    "motorsuz her t\u00fcrl\u00fc kara ta\u015f\u0131t\u0131",
                            "examples": []
                        },
                        {
                            "text": "(ta\u015f\u0131tlar) oto, otomobil",
                            "examples": [
                                {
                                    "example": "Sarho\u015flar\u0131n araba s\u00fcrmeleri "
                                               "sak\u0131ncal\u0131d\u0131r. - Elif \u015eafak",
                                    "translation": None
                                }
                            ]
                        },
                        {
                            "text": "(ta\u015f\u0131tlar) genelde bir hayvan taraf\u0131ndan \u00e7ekilen bir veya "
                                    "daha fazla dingille sahip y\u00fck ta\u015f\u0131ma arac\u0131",
                            "examples": []
                        }
                    ],
                    "part_of_speech": "ad",
                    "derived_terms": [
                        "arabaca, arabac\u0131, arabac\u0131k, arabal\u0131, arabas\u0131z, arabayken, arabayla, arabaysa"
                    ]
                },
                {
                    "etymology": None,
                    "definitions": [
                        {
                            "text": "bir vas\u0131tan\u0131n ald\u0131\u011f\u0131 miktarda",
                            "examples": [
                                {
                                    "example": "\u0130ki araba saman. Bir araba k\u00f6m\u00fcr.",
                                    "translation": None
                                }
                            ]
                        }
                    ],
                    "part_of_speech": "\u00f6n ad"
                }
            ],
            "pronunciation": [
                {
                    "type": "IPA",
                    "values": [
                        {
                            "type": "IPA",
                            "value": "a\u027ea\u02c8ba"
                        }
                    ]
                },
                {
                    "type": "Audio",
                    "values": [
                        {
                            "type": "audio/ogg; codecs=\"vorbis\"",
                            "value": "//upload.wikimedia.org/wiktionary/tr/f/f1/tr_tr_araba.ogg"
                        },
                        {
                            "type": "audio/mpeg",
                            "value": "//upload.wikimedia.org/wiktionary/tr/transcoded/f/f1/tr_tr_araba.ogg"
                                     + "/tr_tr_araba.ogg.mp3"
                        }
                    ]
                }
            ]
        }
        response = Scraper('Türkçe', 'tr').scrape('araba')

        import json
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
