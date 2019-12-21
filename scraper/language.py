from typing import Dict


class Language:
    def __init__(self, alpha2, name, etymology, pronunciation, **kwargs):
        self.alpha2 = alpha2
        self.name = name
        self.etymology = etymology
        self.pronunciation = pronunciation
        self.derived_terms = kwargs['derived_terms']
        self.proverbs = kwargs['proverbs']


languages: Dict[str, Language] = {
    'en': Language('en', 'English', 'Etymology', 'Pronunciation',
                   derived_terms='Derived_terms',
                   proverbs='Proverbs',
                   ),
    'tr': Language('tr', 'Turkish', 'Köken', 'Söyleniş',
                   derived_terms='Türetilmiş_kavramlar',
                   proverbs='Atasözleri',
                   ),
}


def get_language(alpha2: str) -> Language:
    return languages.get(alpha2)
