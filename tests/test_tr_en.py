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
    def test_tr_en_foobar(self, _):
        expected_response = {
            "word": "foobar",
            "from_language": "tr",
            "to_language": "en",
            'meanings': []
        }
        response = Scraper('tr', 'en').scrape('foobar')
        self.assertDictEqual(response, expected_response)

    @patch('scraper.scraper.get_html', side_effect=mock_get_html)
    def test_tr_en_gibi(self, _):
        expected_response = {
            "word": "gibi",
            "from_language": "tr",
            "to_language": "en",
            'meanings': [
                {
                    'etymology': 'From Ottoman Turkish \u06af\u0628\u06cc\u200e (gibi), '
                                 'from Proto-Turkic *k\u0113pi (\u201clike\u201d).',
                    'definitions': [
                        {
                            'text': 'like (similar to)',
                            'examples': [
                                {
                                    'example': 'Annen gibi konu\u015fuyorsun.',
                                    'translation': 'You are talking like your mother.'
                                }
                            ]
                        },
                        {
                            'text': 'such as',
                            'examples': [
                                {
                                    'example': 'Vietnam, Kambo\u00e7ya ve Laos gibi Asya \u00fclkeleri\u2026',
                                    'translation': 'Asian countries such as Vietnam, Cambodia and Laos\u2026'
                                }
                            ]
                        }
                    ],
                    'part_of_speech': 'postposition',
                    "metadata": "gibi"
                }
            ],
            'pronunciation': [
                {
                    'type': 'IPA',
                    'values': [{'type': 'IPA', 'value': '/\u025fibi/'}]
                }
            ]
        }
        response = Scraper('tr', 'en').scrape('gibi')
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)

    @patch('scraper.scraper.get_html', side_effect=mock_get_html)
    def test_tr_en_el(self, _):
        expected_meanings = {
            "word": "el",
            "from_language": "tr",
            "to_language": "en",
            'meanings': [
                {
                    'definitions': [
                        {
                            'text': 'hand',
                            'examples': []
                        }
                    ],
                    'part_of_speech': 'noun',
                    'metadata': 'el (definite accusative eli, plural eller)',
                    "derived_terms": [
                        "el arabas\u0131",
                        "ele ge\u00e7irmek"
                    ]
                },
                {
                    'etymology': 'From Ottoman Turkish \u0627\u06cc\u0644\u200e (el), from Common Turkic *\u0113l '
                                 '(\u201cpeople\u201d).',
                    'definitions': [
                        {
                            'text': 'a foreign person',
                            'examples': []
                        }
                    ],
                    'part_of_speech': 'noun',
                    "metadata": "el (definite accusative eli, plural eller)",
                    "derived_terms": [
                        "el g\u00fcn"
                    ]
                },
                {
                    'etymology': 'From Ottoman Turkish \u0627\u06cc\u0644\u200e (el), '
                                 'from Proto-Turkic *\u0113l (\u201crealm\u201d). '
                                 'Doublet of il. Cognate with Old Turkic [script needed] '
                                 '(\u00e9l), Kazakh \u0435\u043b (el), Azerbaijani el, etc.',
                    'definitions': [
                        {
                            'text': 'country, homeland, province',
                            'examples': []
                        }
                    ],
                    'part_of_speech': 'noun',
                    "metadata": "el (definite accusative eli, plural eller)",
                    "derived_terms": [
                        "el\u00e7i"
                    ]
                }
            ],
            'pronunciation': [
                {
                    'type': 'IPA', 'values': [
                        {'type': 'IPA', 'value': '/el/'}
                    ]
                }
            ]
        }
        meanings = Scraper('tr', 'en').scrape('el')
        print(json.dumps(meanings, indent=4))

        del meanings['meanings'][0]['etymology']  # etymology is not stable
        self.assertDictEqual(meanings, expected_meanings)

    @patch('scraper.scraper.get_html', side_effect=mock_get_html)
    def test_tr_en_araba(self, _):
        expected_response = {
            "word": "araba",
            "from_language": "tr",
            "to_language": "en",
            'meanings': [
                {
                    'etymology': "Inherited from Ottoman Turkish \u0639\u0631\u0628\u0647\u200e (araba).  Ultimate "
                                 "origin uncertain. Originally intended to mean \"a two-wheeled cart\" now being used "
                                 "generically for all kinds of vehicles and bicycles (Schwarz 1992: 393). According "
                                 "to Ramstedt (1905: 23), the Turkic form was borrowed into Iranian (Afgh. "
                                 "arab\u00e1, Shg. ar\u014db\u0101), Arabic "
                                 "\u0639\u064e\u0631\u064e\u0628\u064e\u0629\u200e (\u0295araba), Uralic, "
                                 "European and Caucasian languages. A Turkic loan relation with Burushaski arab\u00e1 "
                                 "is also discussed by Rybatzki. Considering Doerfer (1963/1965/1967/1975), "
                                 "the etymology of the word seems unclear, being either of Turkic or Arabic origin. "
                                 "Uzbek arava was loaned into Tajik \u0430\u0440\u043e\u0431\u0430 (aroba) 'cart, "
                                 "carriage' (Doerfer 1967: 12) and Ormuri ar\u00e2ba 'wheel' (M29: 387). Other Turkic "
                                 "cognates include Uyghur \u06be\u0627\u0631\u06cb\u0627\u200e\u200e (harwa\u200e), "
                                 "Kazakh \u0430\u0440\u0431\u0430 (arba), Kyrgyz \u0430\u0440\u0431\u0430 (arba), "
                                 "Taranchi hariba, as well as Chuvash \u0443\u0440\u0430\u043f\u0430 (urap\u032ca), "
                                 "Bashkir \u0430\u0440\u0431\u0430 (arba) and Tatar \u0430\u0440\u0431\u0430 (arba, "
                                 "\u201ccovered wagon\u201d)[1]. Rybatzki notes that all Turkic forms are too similar "
                                 "with Burushaski, concluding the exact donor language can not be determined.[2]",
                    'definitions': [
                        {
                            'text': 'car',
                            'examples': []
                        },
                        {
                            'text': 'cart',
                            'examples': []
                        },
                        {
                            'text': 'carriage',
                            'examples': []
                        }
                    ],
                    'part_of_speech': 'noun',
                    "metadata": "araba (definite accusative arabay\u0131, plural arabalar)",
                }
            ],
            'pronunciation': [
                {
                    'type': 'IPA',
                    'values': [{'type': 'IPA', 'value': '/\u0251.\u027e\u0251.\u02c8b\u0251/'}]
                },
                {
                    'type': 'Hyphenation',
                    'values': [{'type': 'Hyphenation', 'value': 'a‧ra‧ba'}]
                }
            ]
        }
        response = Scraper('tr', 'en').scrape('araba')
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)
