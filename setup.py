from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    author='Chavithra PARANA',
    author_email='chavithra@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'quotecast = quotecast.applications.cli:cli',
            'trading = trading.applications.cli:cli',
        ],
    },
    extras_requires={
        'tests':[
            'pytest',
        ],
    },
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
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='degiro-connector',
    packages=find_packages(),
    python_requires='>=3.7',
    url='https://github.com/chavithra/degiro-connector',
    version='0.0.4',
)