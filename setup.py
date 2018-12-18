from setuptools import setup, find_packages

setup(
    name = 'meta',
    version = '2.6.2',
    url = 'https://github.com/joshy/meta.git',
    author = 'Joshy Cyriac',
    author_email = 'j.cyriac@gmail.com',
    description = 'A webinterface to Apache Solr to make a PACS searchable',
    packages = find_packages(),
    install_requires = ['Flask==1.0.2', 'Flask-Assets==0.12', 'jsmin==2.2.2', 'requests>=2.20.0', 'pandas==0.19.2', 'daiquiri==1.5.0'],
)