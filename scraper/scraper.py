import re
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup
from scraper.language import get_language


def get_html(url: str) -> str:
    response = requests.get(url)
    code = response.status_code
    if code != 200:
        raise FileNotFoundError(f'URL not found with status code {code}: {url}')
    return response.content


def get_root_element(url: str) -> BeautifulSoup:
    html = get_html(url)
    return BeautifulSoup(html, 'html.parser')


def get_pronunciation(header: BeautifulSoup) -> List[Dict[str, Any]]:
    results = []
    if header.find_next_sibling().name == 'ul':
        ul: BeautifulSoup = header.find_next_sibling()
        get_pronunciation_type(ul, results, 'IPA', 'IPA')
        get_pronunciation_type(ul, results, 'Hyphenation', 'Latn')
        process_audio(ul, results)
    return results


def process_audio(list_container: BeautifulSoup, results: List[Dict[str, Any]]):
    audio_tables: List[BeautifulSoup] = list_container.find_all('table', class_='audiotable')
    for audio_table in audio_tables:
        trs: List[BeautifulSoup] = audio_table.find_all('tr')
        for tr in trs:
            td_type: BeautifulSoup = tr.find('td', class_='audiolink')
            td_file: BeautifulSoup = tr.find('td', class_='audiofile')
            if td_type and td_file:
                results.append({
                    'type': td_type.text,
                    'values': [{'type': src['type'], 'value': src['src']} for src in td_file.find_all('source')]
                })
        audio_table.extract()

    audio_divs: List[BeautifulSoup] = list_container.find_all('div', class_='mediaContainer')
    for audio_div in audio_divs:
        results.append({
            'type': 'Audio',
            'values': [{'type': src['type'], 'value': src['src']} for src in audio_div.find_all('source')]
        })


def get_pronunciation_type(ul: BeautifulSoup,
                           results: List[Dict[str, Any]],
                           pronunciation_type: str,
                           css_class: str):
    values = ul.find_all('span', class_=css_class)
    if values:
        results.append({
            'type': pronunciation_type,
            'values': [{'type': pronunciation_type, 'value': span.text} for span in values]
        })
    else:
        a = ul.find('a', title=pronunciation_type)
        if a:
            a_text: str = a.parent.getText()
            if a_text and ':' in a_text:
                results.append({
                    'type': pronunciation_type,
                    'values': [{'type': pronunciation_type, 'value': a_text.split(':')[1].strip()}]
                })


def remove_descendants_with_class(parent: BeautifulSoup, class_to_remove: str):
    hq_toggles: List[BeautifulSoup] = parent.find_all(class_=class_to_remove)
    for hq_toggle in hq_toggles:
        hq_toggle.extract()


def remove_parent_of_descendant_with_class(parent: BeautifulSoup, class_to_remove: str):
    hq_toggle: BeautifulSoup = parent.find(class_=class_to_remove)
    if hq_toggle and hq_toggle.parent:
        hq_toggle.parent.extract()


def find_usage_examples(parent: BeautifulSoup):
    dl: BeautifulSoup = parent.find('dl')
    examples = []
    if dl:
        example_divs: List[BeautifulSoup] = dl.find_all(class_='h-usage-example')
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
            example_div.extract()

        example_dds: List[BeautifulSoup] = dl.find_all('dd')
        for example_dd in example_dds:
            if example_dd.get_text():
                examples.append({
                        'example': example_dd.get_text(),
                        'translation': None,
                    })
        dl.extract()
    return examples


def is_part_of_speech_header(header: BeautifulSoup) -> bool:
    next_sibling: BeautifulSoup = header.find_next_sibling()
    while next_sibling and next_sibling.name in ['table', 'p', 'div', 'pre']:
        next_sibling = next_sibling.find_next_sibling()
    if next_sibling and next_sibling.name in ['ol', 'dl']:
        return True
    return False


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

    def __init__(self, from_language_name: str = 'English', to_language: str = 'en'):
        """
        :param to_language: The 2-character representation of the language we are translating to. For example en, es

        :param from_language_name: Full name of the source language in to_language.
        If we are looking up en to en, this will be "English".
        If we are looking up en to es, this will be "Inglés".
        """
        self._from_language_name = from_language_name
        self._to_language = get_language(alpha2=to_language)

    def _get_url(self, word: str) -> str:
        return f'https://{self._to_language.alpha2}.wiktionary.org/wiki/{word}'

    def scrape(self, word: str) -> Dict[str, Any]:
        root = get_root_element(self._get_url(word))
        label = root.find(id=self._from_language_name)
        response = {'meanings': []}
        if label is not None:
            siblings: List[BeautifulSoup] = label.parent.find_next_siblings(['h2', 'h3', 'hr'])
            processed_headers = []
            for sibling in siblings:
                if sibling.name in ['hr', 'h2']:
                    break
                else:
                    sibling_text = str(sibling)
                    if sibling_text not in processed_headers:
                        response = self._process_header(sibling, response, processed_headers)
                    processed_headers.append(sibling_text)
        return response

    def _process_header(self, header: BeautifulSoup, response: Dict[str, Any], processed_headers) -> Dict[str, Any]:
        if self._is_pronunciation_header(header):
            response['pronunciation'] = get_pronunciation(header)
        elif self._is_etymology_header(header):
            response['meanings'].append(self._get_meaning_with_etymology(header, processed_headers))
        elif is_part_of_speech_header(header):
            response['meanings'].append(self._get_meaning_without_etymology(header))

        return response

    def _is_pronunciation_header(self, header: BeautifulSoup) -> bool:
        if header.find_all('span', text=self._to_language.pronunciation):
            return True
        return False

    def _get_meaning_without_etymology(self, header: BeautifulSoup) -> [Dict[str, Any]]:
        result = {'etymology': None, 'definitions': []}
        spans: List[BeautifulSoup] = header.find_all('span')
        for span in spans:
            if span.get_text().strip() != '':
                result['part_of_speech'] = span.get_text().strip().lower()
                next_sibling: BeautifulSoup = header.find_next_sibling()
                while next_sibling.name == 'table':
                    next_sibling = next_sibling.find_next_sibling()
                self._process_meaning_values(next_sibling, result)
                break
        return result

    def _get_meaning_with_etymology(self, header: BeautifulSoup, processed_headers) -> [Dict[str, Any]]:
        result = {'etymology': None, 'definitions': []}
        next_sibling: BeautifulSoup = header.find_next_sibling()
        # p is etymology details, capture it
        while next_sibling.name == 'p':
            p: BeautifulSoup = header.find_next_sibling()
            etymology = result.get('etymology')
            result['etymology'] = p.get_text().strip() if etymology is None \
                else etymology + '\n' + p.get_text().strip()
            next_sibling = next_sibling.find_next_sibling()
        # Skip pronunciation headers
        while self._is_pronunciation_header(next_sibling) or next_sibling.name == 'ul':
            next_sibling = next_sibling.find_next_sibling()
        # h4 is the header for parts of speech
        if is_part_of_speech_header(next_sibling):
            span: BeautifulSoup = next_sibling.find('span')
            if span:
                result['part_of_speech'] = span.get_text().strip().lower()
            if next_sibling.name == 'h3':
                processed_headers.append(str(next_sibling))
            next_sibling = next_sibling.find_next_sibling()
            self._process_meaning_values(next_sibling, result)
        return result

    def _process_meaning_values(self, word_p: BeautifulSoup, meaning: Dict[str, Any]):
        next_sibling: BeautifulSoup = word_p
        while next_sibling.name in ['p', 'div', 'pre']:
            next_sibling = next_sibling.find_next_sibling()
        if next_sibling.name in ['ol', 'dl']:
            element_tag = 'dd' if next_sibling.name == 'dl' else 'li'
            lis: List[BeautifulSoup] = next_sibling.find_all(element_tag, recursive=False)
            for li in lis:
                remove_descendants_with_class(li, 'HQToggle')
                remove_parent_of_descendant_with_class(li, 'citation-whole')
                examples = find_usage_examples(li)

                value = {
                    'text': li.get_text().strip(),
                    'examples': examples
                }
                meaning['definitions'].append(value)
            self._process_additional_data(next_sibling, meaning)

    def _process_additional_data(self, after_meaning_values: BeautifulSoup, meaning: Dict[str, Any]) -> None:
        if after_meaning_values is not None and meaning['definitions']:
            next_sibling = after_meaning_values
            while next_sibling is not None and not self._is_meaning_switcher(next_sibling):
                process_see_also(next_sibling, meaning)
                process_derived_terms(next_sibling, meaning)
                process_related_terms(next_sibling, meaning)
                process_synonyms(next_sibling, meaning)
                process_antonyms(next_sibling, meaning)
                next_sibling = next_sibling.find_next_sibling()

    def _is_meaning_switcher(self, header: BeautifulSoup):
        return self._is_pronunciation_header(header) \
               or self._is_etymology_header(header) \
               or is_part_of_speech_header(header)

    def _is_etymology_header(self, header: BeautifulSoup) -> bool:
        if header.find_all('span', text=re.compile(self._to_language.etymology + '.*')):
            return True
        return False
