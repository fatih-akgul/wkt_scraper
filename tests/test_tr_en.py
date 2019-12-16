import unittest
from scraper import Scraper


class ScraperTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_tr_en_foobar(self):
        expected_response = {'meanings': []}
        response = Scraper('Turkish', 'en').scrape('foobar')
        self.assertDictEqual(response, expected_response)

    def test_tr_en_gibi(self):
        expected_response = {
            'meanings': [
                {
                    'etymology': 'From Proto-Turkic *käpä (compare Hungarian kép (“picture”), a Turkic borrowing).',
                    'definitions': [
                        {
                            'text': 'like (similar to)',
                            'examples': [
                                {
                                    'example': 'Tupac bir kahraman gibi öldü.',
                                    'translation': 'Tupac died like a hero.'
                                }
                            ]
                        }
                    ],
                    'part_of_speech': 'postposition'
                }
            ],
            'pronunciation': [
                {
                    'type': 'IPA',
                    'values': [{'type': 'IPA', 'value': '/ɡibi/'}]
                }
            ]
        }
        response = Scraper('Turkish', 'en').scrape('gibi')

        import json
        print(json.dumps(response, indent=4))

        self.assertDictEqual(response, expected_response)

    def test_tr_en_el(self):
        expected_response = {
            'meanings': [
                {
                    'etymology': 'From Old Turkic élig (“hand”), from Proto-Turkic *alı-, *ạl- (“to take”) or *el;-ig '
                                 '("hand"). Cognates with Uzbek ilik, Turkmen el, Gagauz el and Sary-Yughur ɨlɨɣ.',
                    'definitions': [
                        {
                            'text': 'hand',
                            'examples': []
                        }
                    ],
                    'part_of_speech': 'noun'
                },
                {
                    'etymology': None,
                    'definitions': [
                        {
                            'text': 'a foreign person',
                            'examples': []
                        }
                    ],
                    'part_of_speech': 'noun'
                },
                {
                    'etymology': 'From Old Turkic él, from Proto-Turkic.',
                    'definitions': [
                        {
                            'text': 'country, homeland, province',
                            'examples': []
                        }
                    ],
                    'part_of_speech': 'noun'
                }
            ],
            'pronunciation': [
                {
                    'type': 'IPA', 'values': [{'type': 'IPA', 'value': '/el/'}, {'type': 'IPA', 'value': '/əl/'}]
                }
            ]
        }
        response = Scraper('Turkish', 'en').scrape('el')
        self.assertDictEqual(response, expected_response)

    def test_tr_en_araba(self):
        expected_response = {
            'meanings': [
                {
                    'etymology': 'Ultimate origin uncertain. Originally intended to mean "a two-wheeled cart" '
                                 'now being used generically for all kinds of vehicles and bicycles '
                                 '(Schwarz 1992: 393). According to Ramstedt (1905: 23), the Turkic form was '
                                 'borrowed into Iranian (Afgh. arabá, Shg. arōbā), Arabic عَرَبَة\u200e (ʿaraba), '
                                 'Uralic, European and Caucasian languages. A Turkic loan relation with Burushaski '
                                 'arabá is also discussed by Rybatzki. Considering Doerfer (1963/1965/1967/1975), the '
                                 'etymology of the word seems unclear, being either of Turkic or Arabic origin. Uzbek '
                                 'arava was loaned into Tajik aråba \'cart, carriage\' (Doerfer 1967: 12) and Ormuri '
                                 'arâba \'wheel\' (M29: 387). Other Turkic congnates include Uyghur araba, Kyrgyz '
                                 'арба (arba), Taranchi hariba, as well as Chuvash урапа (urapa), '
                                 'Bashkir арба (arba) and Tatar арба (arba, “covered wagon”)[1]. Rybatzki notes that '
                                 'all Turkic forms are too similar with Burushaski, concluding the exact donor '
                                 'language can not be determined.[2]',
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
                    'part_of_speech': 'noun'
                }
            ],
            'pronunciation': [
                {
                    'type': 'IPA',
                    'values': [{'type': 'IPA', 'value': '/aɾaˈba/'}]
                },
                {
                    'type': 'Hyphenation',
                    'values': [{'type': 'Hyphenation', 'value': 'a‧ra‧ba'}]
                }
            ]
        }
        response = Scraper('Turkish', 'en').scrape('araba')
        self.assertDictEqual(response, expected_response)
