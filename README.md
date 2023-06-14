# Wiktionary Scraper
Wiktionary Scraper is a basic scraper implementation to get word data from Wiktionary for a given word and language.  

## Installation
You can install the Wiktionary Scraper from [PyPI](https://pypi.org/project/wkt_scraper/):
    
    pip install wkt_scraper

In python code, to look up the word "street" from English to Spanish:

    from scraper import scrape
    response = scrape('en', 'es', 'street')

Currently only English, Spanish and Turkish are supported. 
Supporting more languages will require additional work and testing. 
