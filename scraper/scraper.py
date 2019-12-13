import re
from typing import Dict, Any, List
from iso639 import languages
import requests
from bs4 import BeautifulSoup
import json


def get_html(url: str) -> str:
    response = requests.get(url)
    code = response.status_code
    if code != 200:
        raise FileNotFoundError(f'URL not found with status code {code}: {url}')
    return response.content


def get_root_element(url: str) -> BeautifulSoup:
    html = get_html(url)
    return BeautifulSoup(html, 'html.parser')


def process_header(header: BeautifulSoup, response: Dict[str, Any], processed_headers) -> Dict[str, Any]:
    if is_pronunciation_header(header):
        response['pronunciation'] = get_pronunciation(header)
    elif is_etymology_header(header):
        response['meanings'].append(get_meaning_with_etymology(header, processed_headers))
    elif is_part_of_speech_header(header):
        response['meanings'].append(get_meaning_without_etymology(header))

    return response


def is_meaning_switcher(header: BeautifulSoup):
    return is_pronunciation_header(header) \
           or is_etymology_header(header) \
           or is_part_of_speech_header(header)


def is_pronunciation_header(header: BeautifulSoup) -> bool:
    if header.find_all('span', text='Pronunciation'):
        return True
    return False


def get_pronunciation(header: BeautifulSoup) -> List[Dict[str, Any]]:
    results = []
    if header.find_next_sibling().name == 'ul':
        ul: BeautifulSoup = header.find_next_sibling()
        get_pronunciation_type(ul, results, 'IPA', 'IPA')
        get_pronunciation_type(ul, results, 'Hyphenation', 'Latn')
    return results


def get_pronunciation_type(ul: BeautifulSoup,
                           results: List[Dict[str, Any]],
                           pronunciation_type: str,
                           css_class: str):
    values = ul.find_all('span', class_=css_class)
    if values:
        results.append({
            'type': pronunciation_type,
            'values': [span.text for span in values]
        })


def is_etymology_header(header: BeautifulSoup) -> bool:
    if header.find_all('span', text=re.compile('Etymology.*')):
        return True
    return False


def get_meaning_with_etymology(header: BeautifulSoup, processed_headers) -> [Dict[str, Any]]:
    result = {'etymology': None, 'values': []}
    next_sibling: BeautifulSoup = header.find_next_sibling()
    # p is etymology details, capture it
    while next_sibling.name == 'p':
        p: BeautifulSoup = header.find_next_sibling()
        etymology = result.get('etymology')
        result['etymology'] = p.get_text().strip() if etymology is None \
            else etymology + '\n' + p.get_text().strip()
        next_sibling = next_sibling.find_next_sibling()
    # Skip pronunciation headers
    while is_pronunciation_header(next_sibling) or next_sibling.name == 'ul':
        next_sibling = next_sibling.find_next_sibling()
    # h4 is the header for parts of speech
    if is_part_of_speech_header(next_sibling):
        span: BeautifulSoup = next_sibling.find('span')
        if span:
            result['part_of_speech'] = span.get_text().strip().lower()
        if next_sibling.name == 'h3':
            processed_headers.append(str(next_sibling))
        next_sibling = next_sibling.find_next_sibling()
        process_meaning_values(next_sibling, result)
    return result


def process_meaning_values(word_p: BeautifulSoup, meaning: Dict[str, Any]):
    next_sibling: BeautifulSoup = word_p
    while next_sibling.name == 'p':
        next_sibling = next_sibling.find_next_sibling()
    if next_sibling.name == 'ol':
        lis = next_sibling.find_all('li')
        for li in lis:
            dl: BeautifulSoup = li.find('dl')
            examples = []
            if dl:
                dl.extract()
                example_divs = dl.find_all(class_='h-usage-example')
                for example_div in example_divs:
                    example_span: BeautifulSoup = example_div.find(class_='e-example')
                    if example_span:
                        example = {
                            'example': example_span.get_text(),
                            'translation': None,
                        }
                        translation: BeautifulSoup = example_div.find(class_='e-translation')
                        if translation:
                            example['translation'] = translation.get_text()
                        examples.append(example)
            value = {
                'text': li.get_text().strip(),
                'examples': examples
            }
            meaning['values'].append(value)
        process_additional_data(next_sibling, meaning)


def is_part_of_speech_header(header: BeautifulSoup) -> bool:
    next_sibling: BeautifulSoup = header.find_next_sibling()
    while next_sibling and next_sibling.name == 'table':
        next_sibling = next_sibling.find_next_sibling()
    if next_sibling and next_sibling.name == 'p':
        next_sibling = next_sibling.find_next_sibling()
        if next_sibling.name == 'ol':
            return True
    return False


def get_meaning_without_etymology(header: BeautifulSoup) -> [Dict[str, Any]]:
    result = {'etymology': None, 'values': []}
    span: BeautifulSoup = header.find('span')
    if span:
        result['part_of_speech'] = span.get_text().strip().lower()
        next_sibling: BeautifulSoup = header.find_next_sibling()
        while next_sibling.name == 'table':
            next_sibling = next_sibling.find_next_sibling()
        process_meaning_values(next_sibling, result)
    return result


def process_additional_data(after_meaning_values: BeautifulSoup, meaning: Dict[str, Any]) -> None:
    if after_meaning_values is not None and meaning['values']:
        next_sibling = after_meaning_values
        while next_sibling is not None and not is_meaning_switcher(next_sibling):
            process_see_also(next_sibling, meaning)
            process_derived_terms(next_sibling, meaning)
            process_related_terms(next_sibling, meaning)
            process_synonyms(next_sibling, meaning)
            process_antonyms(next_sibling, meaning)
            next_sibling = next_sibling.find_next_sibling()


def process_see_also(after_meaning_values: BeautifulSoup, meaning: Dict[str, Any]) -> None:
    process_by_id(after_meaning_values, meaning, 'See_also')


def process_derived_terms(after_meaning_values: BeautifulSoup, meaning: Dict[str, Any]) -> None:
    process_by_id(after_meaning_values, meaning, 'Derived_terms')


def process_related_terms(after_meaning_values: BeautifulSoup, meaning: Dict[str, Any]) -> None:
    process_by_id(after_meaning_values, meaning, 'Related_terms')


def process_synonyms(after_meaning_values: BeautifulSoup, meaning: Dict[str, Any]) -> None:
    process_by_id(after_meaning_values, meaning, 'Synonyms')


def process_antonyms(after_meaning_values: BeautifulSoup, meaning: Dict[str, Any]) -> None:
    process_by_id(after_meaning_values, meaning, 'Antonyms')


def process_by_id(after_meaning_values: BeautifulSoup, meaning: Dict[str, Any], tag_id: str):
    result = []
    if after_meaning_values.name in ['h3', 'h4', 'h5']:
        h4: BeautifulSoup = after_meaning_values
        span: BeautifulSoup = after_meaning_values.find(id=lambda x: x and x.startswith(tag_id))
        if span:
            ul: BeautifulSoup = h4.find_next_sibling()
            if ul.name == 'ul':
                lis = ul.find_all('li')
                for li in lis:
                    result.append(li.get_text())
    if result:
        meaning[tag_id.lower()] = result


class Scraper:

    def __init__(self, from_language: str = 'en', to_language: str = 'en'):
        self._from_language = languages.get(alpha2=from_language)
        self._to_language = languages.get(alpha2=to_language)

    def _get_url(self, word: str) -> str:
        return f'https://{self._to_language.alpha2}.wiktionary.org/wiki/{word}'

    def scrape(self, word: str) -> Dict[str, Any]:
        root = get_root_element(self._get_url(word))
        label = root.find(id=self._from_language.name)
        response = {'meanings': []}
        if label is not None:
            siblings: List[BeautifulSoup] = label.parent.find_next_siblings(['h3', 'hr'])
            processed_headers = []
            for sibling in siblings:
                if sibling.name == 'hr':
                    break
                else:
                    sibling_text = str(sibling)
                    if sibling_text not in processed_headers:
                        response = process_header(sibling, response, processed_headers)
                    processed_headers.append(sibling_text)
        return response
