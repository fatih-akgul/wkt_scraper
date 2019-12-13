import pathlib
from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


# This call to setup() does all the work
setup(
    name='wkt_scraper',
    version='1.0.0',
    description='Parse word information from Wiktionary',
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords='wiktionary scraper parser',
    author='Fatih Akgul',
    author_email='akguls@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=(
        find_packages(exclude=('tests',)),
    ),
    include_package_data=True,
    url='https://github.com/fatih-akgul/wkt_scraper',
    install_requires=['bs'],  # TODO: update requirements
)
