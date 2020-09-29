from setuptools import setup, find_packages
setup(
    name='degiro-connector',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'wrapt',
        'wheel',
        'grpcio',
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