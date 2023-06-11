import unittest
from unittest.mock import patch

from scraper import Scraper
from tests.mock import mock_get_html


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    @patch('scraper.scraper.get_html', side_effect=mock_get_html)
    def test_tr_tr_araba(self, _):
        expected_response = {
            "word": "araba",
            "from_language": "tr",
            "to_language": "tr",
            "meanings": [
                {
                    "etymology": "Osmanl\u0131 T\u00fcrk\u00e7esi \u0622\u0631\u0627\u0628\u0647\u200e "
                                 "s\u00f6zc\u00fc\u011f\u00fcnden. \u00e7uva\u015f\u00e7a uraba (uraba) veya urava ("
                                 "urava, \u201ctekerlek\u201d) ve Mo\u011folca araa (\u201ctekerlek\u201d) ile "
                                 "ayn\u0131 k\u00f6kene dayanmaktad\u0131r. Araba kelimesi T\u00fcrk\u00e7eden "
                                 "Arap\u00e7a, \u0130ngilizce ve Rus\u00e7a gibi b\u00e2z\u0131 dillere de "
                                 "ge\u00e7mi\u015ftir.",
                    "definitions": [
                        {
                            "text": "(kara ula\u015f\u0131m\u0131, ta\u015f\u0131tlar) tekerlekli, motorlu her "
                                    "t\u00fcrl\u00fc kara ta\u015f\u0131t\u0131, oto, otomobil",
                            "examples": [
                                {
                                    "example": "Sarho\u015flar\u0131n araba s\u00fcrmeleri "
                                               "sak\u0131ncal\u0131d\u0131r. - Elif \u015eafak}}",
                                    "translation": None
                                }
                            ]
                        },
                        {
                            "text": "(kara ula\u015f\u0131m\u0131, ta\u015f\u0131tlar) motorsuz, genelde [[bir00 "
                                    "hayvan taraf\u0131ndan \u00e7ekilen bir veya daha fazla dingile sahip y\u00fck "
                                    "ta\u015f\u0131ma arac\u0131",
                            "examples": []
                        }
                    ],
                    "part_of_speech": "ad",
                    "metadata": "araba (belirtme h\u00e2li arabay\u0131, \u00e7o\u011fulu arabalar) -s\u0131",
                    "derived_terms": [
                        "arabaca, arabac\u0131, arabac\u0131k, arabal\u0131, arabas\u0131z, arabayken, arabayla, "
                        "arabaysa"
                    ]
                },
                {
                    "etymology": None,
                    "definitions": [
                        {
                            "text": "bir vas\u0131tan\u0131n ald\u0131\u011f\u0131 miktarda",
                            "examples": [
                                {
                                    "example": "Bir araba k\u00f6m\u00fcrle k\u0131\u015f ge\u00e7er mi hi\u00e7?",
                                    "translation": None,
                                },
                                {
                                    "example": "\u0130ki araba saman var orada.",
                                    "translation": None,
                                }
                            ],
                        }
                    ],
                    "part_of_speech": "\u00f6n ad",
                    "metadata": "araba (kar\u015f\u0131la\u015ft\u0131rma daha araba, \u00fcst\u00fcnl\u00fck en araba)",
                    "proverbs": [
                        "Araba devrilince yol g\u00f6steren \u00e7ok olur",
                        "Araba ile tav\u015fan avlanmaz"
                    ]
                }
            ],
            "pronunciation": [
                {
                    "type": "IPA",
                    "values": [
                        {
                            "type": "IPA",
                            "value": "/\u0251.\u027e\u0251.\u02c8b\u0251/"
                        }
                    ]
                },
                {
                    "type": "Ses",
                    "values": [
                {
                    "type": "audio/ogg; codecs=\"vorbis\"",
                    "value": "//upload.wikimedia.org/wikipedia/commons/9/99/Tr_araba.ogg"
                },
                {
                    "type": "audio/mpeg",
                    "value": "//upload.wikimedia.org/wikipedia/commons/transcoded/9/99/Tr_araba.ogg/Tr_araba.ogg.mp3"
                }
            ]
                }
            ]
        }
        response = Scraper('tr', 'tr').scrape('araba')

        import json
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
