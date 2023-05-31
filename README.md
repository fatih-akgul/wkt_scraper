# Wiktionary Scraper
Wiktionary Scraper is a basic scraper implementation to get word data from Wiktionary for a given word and language.  

## Installation
You can install the Wiktionary Scraper from [PyPI](https://pypi.org/project/wkt_scraper/):
    
    pip install wkt_scraper

In python code, to look up the word "complicated" from English to English:

    from scraper import Scraper
    response = Scraper('en', 'en').scrape('complicated')

Currently only English and Turkish are supported. 
Supporting more languages will require additional work and testing. 
