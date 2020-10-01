from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='behavior-analysis',
    version='0.1.0',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Luiz Tauffer',
    author_email='luiz@taufferconsulting.com',
    # url='https://github.com/Tauffer-Consulting/',
    packages=find_packages(),
    package_data={'': ['']},
    include_package_data=True,
    install_requires=[
        'pandas', 'numpy', 'Flask', 'Flask-SQLAlchemy',
        'dash', 'dash_bootstrap_components', 'dash-canvas', 'pandas-profiling'
    ]
)
