"""
Setup script for the bill package.
"""

from setuptools import setup

setup(
    name='bill',
    version='0.1.0',
    author='Benedict W. Hazel',
    description='Works with and extracts data from energy bills.',
    include_package_data=True,
    install_requires=[
        'langchain',
        'pypdf'
    ]
)
