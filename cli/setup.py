"""
Setup script for the cli package.
"""

import os
from setuptools import setup

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

setup(
    name='cli',
    version='0.1.0',
    author='Benedict W. Hazel',
    description='CLI for working with Octopus Energy and generic energy data and energy bills.',
    entry_points={
        'console_scripts': [
            'oec=cli.main:main',
        ],
    },
    include_package_data=True,
    install_requires=[
        'click',
        'colorama',
        'gradio',
        'jmespath',
        'jsonpickle',
        'langchain',
        'langchain-openai',
        'Pint',
        'python-dotenv',
        f'bill @ file://{PROJECT_ROOT}/../bill',
        f'chat @ file://{PROJECT_ROOT}/../chat',
    ]
)
