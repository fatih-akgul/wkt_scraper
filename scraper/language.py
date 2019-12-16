from typing import Dict


class Language:
    def __init__(self, alpha2, name, etymology, pronunciation):
        self.alpha2 = alpha2
        self.name = name
        self.etymology = etymology
        self.pronunciation = pronunciation


languages: Dict[str, Language] = {
    'en': Language('en', 'English', 'Etymology', 'Pronunciation'),
    'tr': Language('tr', 'Turkish', 'Köken', 'Söyleniş'),
}


def get_language(alpha2: str) -> Language:
    return languages.get(alpha2)
