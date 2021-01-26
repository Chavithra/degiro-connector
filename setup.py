from setuptools import setup, find_packages
setup(
    name='degiro-connector',
    version='0.0.4',
    packages=find_packages(),
    install_requires=[
        'wheel',
        'click',
        'grpcio',
        'onetimepass',
        'orjson',
        'protobuf',
        'requests',
        'wrapt',
    ],
    author='Chavithra PARANA',
    author_email='chavithra@gmail.com',
    entry_points={
        'console_scripts': [
            'quotecast = quotecast.applications.cli:cli',
            'trading = trading.applications.cli:cli',
        ],
    }
)