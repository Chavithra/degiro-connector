from setuptools import setup, find_packages
setup(
    author='Chavithra PARANA',
    author_email='chavithra@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3-Clause",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'quotecast = quotecast.applications.cli:cli',
            'trading = trading.applications.cli:cli',
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
    name='degiro-connector',
    packages=find_packages(),
    python_requires='>=3.7',
    extras_requires={
        'tests':[
            'pytest',
        ],
    },
    version='0.0.4',
)