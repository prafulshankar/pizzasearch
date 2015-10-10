from setuptools import setup, find_packages


setup(
    name = "pizzasearch",
    version = "0.1dev",
    packages = ['pizza',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description = open('README.txt').read(),
    author = "Praful Shankar",
    author_email = "praful.shankar@berkeley.edu",
    url = "https://github.com/prafulshankar/pizzasearch",
    download_url="https://github.com/prafulshankar/pizzasearch/tarball/0.1dev",
    install_requires = ['piazza-api >= 0.5.1'],
    dependency_links = [
        "https://pypi.python.org/pypi/piazza-api"
    ],
)