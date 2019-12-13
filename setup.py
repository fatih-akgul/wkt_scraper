from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


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
    packages=('scraper', ),
    include_package_data=True,
    url='https://github.com/fatih-akgul/wkt_scraper',
    install_requires=['bs4', 'requests', 'iso-639'],
)
