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
    'en': Language(
        alpha2='en',
        name='English',
        etymology='Etymology',
        pronunciation='Pronunciation',
        derived_terms='Derived_terms',
        proverbs='Proverbs',
    ),
    'es': Language(
        alpha2='es',
        name='Spanish',
        etymology='Etimología',
        pronunciation='Pronunciación',
        derived_terms='Términos_derivados',
        proverbs='Proverbios',
    ),
    'tr': Language(
        alpha2='tr',
        name='Turkish',
        etymology='Köken',
        pronunciation='Söyleniş',
        derived_terms='Türetilmiş_kavramlar',
        proverbs='Atasözleri',
    ),
}

language_names = {
    'tr': {
        'en': 'İngilizce',
        'es': 'İspanyolca',
        'tr': 'Türkçe',
    },
    'en': {
        'en': 'English',
        'es': 'Spanish',
        'tr': 'Turkish',
    },
    'es': {
        'en': 'Inglés',
        'es': 'Español',
        'tr': 'Turco',
    }
}


def get_language(alpha2: str) -> Language:
    return languages.get(alpha2)
