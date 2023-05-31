import re
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup, PageElement, ResultSet, Tag, NavigableString
from scraper.language import get_language, language_names


def get_html(url: str) -> str:
    response = requests.get(url)
    code = response.status_code
    if code != 200:
        raise FileNotFoundError(f'URL not found with status code {code}: {url}')
    return response.content.decode('utf-8')


def get_root_element(url: str) -> BeautifulSoup:
    html = get_html(url)
    return BeautifulSoup(html, 'html.parser')


def get_pronunciation(header: PageElement) -> List[Dict[str, Any]]:
    results = []
    ul: Tag = header.find_next_sibling()
    if ul.name == 'ul' or ul.name == 'dl':
        get_ipa(ul, results)
        get_pronunciation_type(ul, results, 'Hyphenation', 'Latn')
        process_audio(ul, results)
    return results


def process_audio(list_container: PageElement, results: List[Dict[str, Any]]):
    audio_tables: ResultSet[PageElement] = list_container.find_all('table', class_='audiotable')
    for audio_table in audio_tables:
        trs: ResultSet[PageElement] = audio_table.find_all('tr')
        for tr in trs:
            td_type: PageElement = tr.find_next('td', class_='audiolink')
            td_file: PageElement = tr.find_next('td', class_='audiofile')
            if td_type and td_file:
                results.append({
                    'type': td_type.text,
                    'values': [{
                        'type': src.attrs['type'],
                        'value': src.attrs['src']
                    } for src in td_file.find_all('source')]
                })
        audio_table.extract()

    audio_divs: List[PageElement] = list_container.find_all('div', class_='mediaContainer')
    for audio_div in audio_divs:
        results.append({
            'type': 'Audio',
            'values': [{
                'type': src.attrs['type'].text,
                'value': src.attrs['src'].text
            } for src in audio_div.find_all('source')]
        })


def get_ipa(ul: PageElement, results: List[Dict[str, any]]):
    value_spans: ResultSet[Tag] = ul.find_all('span', class_='IPA')
    if value_spans:
        values = []
        for value_span in value_spans:
            type_span = value_span.find_previous_sibling('span', class_='ib-content qualifier-content')
            type_text = 'IPA'
            if type_span:
                type_text = type_span.text
            values.append({'type': type_text, 'value': value_span.text})

        results.append({
            'type': 'IPA',
            'values': values
        })
    else:
        a = ul.find_next('a', title='IPA')
        if a:
            a_text: str = a.parent.getText()
            if a_text and ':' in a_text:
                results.append({
                    'type': 'IPA',
                    'values': [{'type': 'IPA', 'value': a_text.split(':')[1].strip()}]
                })


def get_pronunciation_type(ul: PageElement,
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
        a = ul.find_next('a', title=pronunciation_type)
        if a:
            a_text: str = a.parent.getText()
            if a_text and ':' in a_text:
                results.append({
                    'type': pronunciation_type,
                    'values': [{'type': pronunciation_type, 'value': a_text.split(':')[1].strip()}]
                })


def remove_descendants_with_class(parent: PageElement, class_to_remove: str):
    hq_toggles: ResultSet[PageElement] = parent.find_all(class_=class_to_remove)
    for hq_toggle in hq_toggles:
        hq_toggle.extract()


def remove_parent_of_descendant_with_class(parent: PageElement, class_to_remove: str):
    hq_toggles = parent.find_all(class_=class_to_remove)
    for hq_toggle in hq_toggles:
        if hq_toggle and hq_toggle.parent:
            hq_toggle.parent.extract()


def find_usage_examples(parent: PageElement) -> List[Dict[str, Any]]:
    dl: Tag = parent.find('dl')
    examples = []
    if dl:
        example_divs: List[Tag] = dl.find_all(class_='h-usage-example')
        for example_div in example_divs:
            example_span: Tag = example_div.find(class_='e-example')
            if example_span:
                example = {
                    'example': example_span.get_text(),
                    'translation': None,
                }
                translation: Tag = example_div.find(class_='e-translation')
                if translation:
                    example['translation'] = translation.get_text()
                examples.append(example)
            example_div.extract()

        example_dds: ResultSet[Tag] = dl.find_all('dd', recursive=False)
        for example_dd in example_dds:
            if example_dd.get_text():
                example = {
                    'example': None,
                    'translation': None,
                }
                translation_dd: Tag = example_dd.find('dd')
                if translation_dd and translation_dd.get_text():
                    example['translation'] = translation_dd.get_text().strip()
                    translation_dd.extract()
                example['example'] = example_dd.get_text().strip()
                examples.append(example)
        dl.extract()
    return examples


def is_part_of_speech_header(header: PageElement) -> bool:
    next_sibling: Tag = header.find_next_sibling()
    while next_sibling and next_sibling.name in ['table', 'p', 'div', 'pre', 'figure']:
        next_sibling = next_sibling.find_next_sibling()
    if next_sibling and next_sibling.name in ['ol', 'dl']:
        return True
    return False


def process_by_id(after_meaning_values: PageElement,
                  meaning: Dict[str, Any],
                  response_field: str,
                  tag_id: str):
    result = []
    if after_meaning_values.name in ['h3', 'h4', 'h5']:
        h4: PageElement = after_meaning_values
        span: Tag = after_meaning_values.find(id=lambda x: x and x.startswith(tag_id))
        if span:
            ul: Tag = h4.find_next_sibling()
            if ul.name == 'ul':
                lis = ul.find_all('li')
                for li in lis:
                    result.append(li.get_text())
    if result:
        meaning[response_field] = result


class Scraper:

    def __init__(self, from_language: str = 'en', to_language: str = 'en'):
        """
        :param from_language: The 2-character representation of the input language (en, tr etc.)
        :param to_language: The 2-character representation of the language we are translating to (en, tr etc.)
        If we are looking up en to en, this will be "English".
        If we are looking up en to tr, this will be "İngilizce".
        """
        self._from_language_name = language_names[to_language][from_language]
        self._from_language = get_language(alpha2=from_language)
        self._to_language = get_language(alpha2=to_language)

        # Key is the name of field in response. Value is the HTML element ID on the Wiktionary page
        self._additional_data = {
            'see_also': 'See_also',
            'related_terms': 'Related_terms',
            'synonyms': 'Synonyms',
            'antonyms': 'Antonyms',
            'proverbs': self._to_language.proverbs,
            'derived_terms': self._to_language.derived_terms,
        }

    def scrape(self, word: str) -> Dict[str, Any]:
        root = get_root_element(self._get_url(word))
        self._remove_other_languages(root)
        label = root.find(id=self._from_language_name)
        response = {
            'word': word,
            'from_language': self._from_language.alpha2,
            'to_language': self._to_language.alpha2,
            'meanings': []
        }
        if label is not None:
            siblings: ResultSet[PageElement] = label.parent.find_next_siblings(['h2', 'h3', 'hr'])
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

    def _remove_other_languages(self, root: PageElement):
        languages: ResultSet[Tag] = root.find_all(name='h2')
        for language in languages:
            language_container: Tag = language.find(id=self._from_language_name)
            if language_container is None:
                # Remove until next language h2
                siblings = language.find_next_siblings()
                language.extract()
                for sibling in siblings:
                    if sibling.name == 'h2':
                        break
                    sibling.extract()

    def _get_url(self, word: str) -> str:
        return f'https://{self._to_language.alpha2}.wiktionary.org/wiki/{word}'

    def _process_header(self, header: PageElement, response: Dict[str, Any], processed_headers) -> Dict[str, Any]:
        if self._is_pronunciation_header(header):
            response['pronunciation'] = get_pronunciation(header)
        elif self._is_etymology_header(header):
            response['meanings'].append(self._get_meaning_with_etymology(header, processed_headers))
        elif is_part_of_speech_header(header):
            response['meanings'].append(self._get_meaning_without_etymology(header))

        return response

    def _is_pronunciation_header(self, header: PageElement) -> bool:
        if header.find_all('span', string=self._to_language.pronunciation):
            return True
        return False

    def _get_meaning_without_etymology(self, header: PageElement) -> [Dict[str, Any]]:
        result = {'etymology': None, 'definitions': []}
        spans: ResultSet[Tag] = header.find_all('span')
        for span in spans:
            if span.get_text().strip() != '':
                result['part_of_speech'] = span.get_text().strip().lower()
                next_sibling: Tag = header.find_next_sibling()
                while next_sibling.name == 'table':
                    next_sibling = next_sibling.find_next_sibling()
                self._process_meaning_values(next_sibling, result)
                break
        return result

    def _get_meaning_with_etymology(self, header: PageElement, processed_headers) -> [Dict[str, Any]]:
        result = {'etymology': None, 'definitions': []}
        next_sibling: Tag = header.find_next_sibling()
        # p is etymology details, capture it
        while next_sibling.name == 'p':
            p: NavigableString = header.find_next_sibling()
            etymology = result.get('etymology')
            result['etymology'] = p.get_text().strip() if etymology is None \
                else etymology + '\n' + p.get_text().strip()
            next_sibling = next_sibling.find_next_sibling()
        # Skip pronunciation headers
        while self._is_pronunciation_header(next_sibling) or next_sibling.name == 'ul':
            next_sibling = next_sibling.find_next_sibling()
        # h4 is the header for parts of speech
        if is_part_of_speech_header(next_sibling):
            span: NavigableString = next_sibling.find('span')
            if span:
                result['part_of_speech'] = span.get_text().strip().lower()
            if next_sibling.name == 'h3':
                processed_headers.append(str(next_sibling))
            next_sibling = next_sibling.find_next_sibling()
            self._process_meaning_values(next_sibling, result)
        return result

    def _process_meaning_values(self, word_p: PageElement, meaning: Dict[str, Any]):
        next_sibling: PageElement = word_p
        if next_sibling.name == 'p':
            meaning['metadata'] = next_sibling.get_text().strip()
        if next_sibling.name in ['p', 'div', 'pre', 'figure']:
            next_sibling = next_sibling.find_next_sibling(name=['ol', 'dl'])
        if next_sibling.name in ['ol', 'dl']:
            # element_tag = 'dd' if next_sibling.name == 'dl' else 'li'
            lis: ResultSet[PageElement] = next_sibling.find_all(name=['dd', 'li'], recursive=False)
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

    def _process_additional_data(self, after_meaning_values: PageElement, meaning: Dict[str, Any]) -> None:
        if after_meaning_values is not None and meaning['definitions']:
            next_sibling = after_meaning_values
            while next_sibling is not None and not self._is_meaning_switcher(next_sibling):
                for response_field, html_id in self._additional_data.items():
                    process_by_id(next_sibling, meaning, response_field, html_id)

                next_sibling = next_sibling.find_next_sibling()

    def _is_meaning_switcher(self, header: PageElement):
        return self._is_pronunciation_header(header) \
               or self._is_etymology_header(header) \
               or is_part_of_speech_header(header)

    def _is_etymology_header(self, header: PageElement) -> bool:
        if header.find_all('span', string=re.compile(self._to_language.etymology + '.*')):
            return True
        return False
