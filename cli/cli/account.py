"""
CLI commands for working with an account.
"""

import os
import click
from octopus_energy.model import Account
from . import create_json_output, OCTOPUS_ENERGY_REPOSITORY, update_client_credentials

@click.group('account')
def account_group():
    """
    Commands for working with your account.
    """

@account_group.command('get')
@click.option('--api-key', 'api_key',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_API_KEY'],
              help='The Octopus Energy API key (Not recommended).')
@click.option('-n', '--number', 'number',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_ACCOUNT_NUMBER'],
              help='The account number (Not recommended).')
@click.option('-q', '--query', 'query',
              type=click.STRING,
              default=None,
              help='The JMESPath query to filter and structure the output.')
def get_account(api_key: str,
                number: str,
                query: str
    ):
    """
    Gets account details.
    """
    update_client_credentials(api_key=api_key,
                              number=number)

    account: Account = OCTOPUS_ENERGY_REPOSITORY.get_account()
    output = create_json_output(account, query)

    print(output)
