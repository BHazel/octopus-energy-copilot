"""
CLI commands for working with an account.
"""

import os
import click
from dotenv import load_dotenv
import jsonpickle
from octopus_energy.client import OctopusEnergyClient
from octopus_energy.model import Account
from octopus_energy.repository import OctopusEnergyRepository

load_dotenv()

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
def get_account(api_key: str,
                number: str
    ):
    """
    Gets account details.
    """
    repository: OctopusEnergyRepository = OctopusEnergyRepository(
        OctopusEnergyClient(
            api_key,
            number,
            None,
            None))

    account: Account = repository.get_account()
    print(jsonpickle.encode(account, indent=True))
