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
    extras_require={
        'tests': [
            'pytest',
        ],
        'lint': [
            'flake8',
        ],
    },
    install_requires=[
        'grpcio',
        'onetimepass',
        'orjson',
        'pandas',
        'protobuf',
        'requests',
        'wheel',
        'wrapt',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='degiro-connector',
    packages=find_packages(include=["degiro_connector*"]),
    python_requires='>=3.6',
    url='https://github.com/chavithra/degiro-connector',
    version='1.0.2',
)
