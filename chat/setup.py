"""
Setup script for the chat package.
"""

import os
from setuptools import setup

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

setup(
    name='chat',
    version='0.1.0',
    author='Benedict W. Hazel',
    description='Chat infrastructure for working with Octopus Energy and generic energy data.',
    include_package_data=True,
    install_requires=[
        'jsonpickle',
        'langchain',
        'Pint',
        'python-dotenv',
        f'energy @ file://{PROJECT_ROOT}/../energy',
        f'octopus_energy @ file://{PROJECT_ROOT}/../octopus_energy'
    ]
)
