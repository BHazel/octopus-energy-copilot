"""
CLI commands for products.
"""

from datetime import datetime
import os
import click
from octopus_energy.model import Product, ProductFiltering
from . import create_json_output, OCTOPUS_ENERGY_REPOSITORY, update_client_credentials

@click.group('product')
def product_group():
    """
    Commands for energy product information.
    """

@product_group.command('list')
@click.option('--api-key', 'api_key',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_API_KEY'],
              help='The Octopus Energy API key (Not recommended).')
@click.option('-v', '--variable', 'is_variable',
              is_flag=True,
              default=False,
              help='Filter products by whether they are variable.')
@click.option('-g', '--green', 'is_green',
              is_flag=True,
              default=False,
              help='Filter products by whether they are green.')
@click.option('-t', '--tracker', 'is_tracker',
              is_flag=True,
              default=False,
              help='Filter products by whether they are tracker.')
@click.option('-p', '--prepay', 'is_prepay',
              is_flag=True,
              default=False,
              help='Filter products by whether they are prepay.')
@click.option('-b', '--business', 'is_business',
              is_flag=True,
              default=False,
              help='Filter products by whether they are for business.')
@click.option('-a', '--at', 'available_at',
              type=click.DateTime(),
              help='Filter products by whether they are available on the specific date.')
@click.option('-q', '--query', 'query',
              type=click.STRING,
              default=None,
              help='The JMESPath query to filter and structure the output.')
def list_products(api_key: str,
                  is_variable: bool,
                  is_green: bool,
                  is_tracker: bool,
                  is_prepay: bool,
                  is_business: bool,
                  available_at: datetime,
                  query: str):
    """
    List products.
    """
    update_client_credentials(api_key=api_key)

    filtering: ProductFiltering = ProductFiltering.DEFAULT
    if is_variable:
        filtering = ProductFiltering.VARIABLE
    if is_green:
        filtering = filtering | ProductFiltering.GREEN
    if is_tracker:
        filtering = filtering | ProductFiltering.TRACKER
    if is_prepay:
        filtering = filtering | ProductFiltering.PREPAY
    if is_business:
        filtering = filtering | ProductFiltering.BUSINESS

    products: list[Product] = OCTOPUS_ENERGY_REPOSITORY.get_products(available_at, filtering)

    output = create_json_output(products, query)
    print(output)
