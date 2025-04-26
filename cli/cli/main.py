"""
Main program entry point.
"""

import click
from .account import account_group
from .bill import bill_group
from .chat import chat
from .consumption import consumption_group
from .convert import convert_group
from .agent import agent_group
from .product import product_group

@click.group()
@click.version_option('0.1.0', prog_name='Octopus Energy Copilot CLI')
@click.help_option('-h', '--help')
def main():
    """
    Root command for the Octopus Energy Copilot CLI.
    """

main.add_command(account_group)
main.add_command(agent_group)
main.add_command(bill_group)
main.add_command(consumption_group)
main.add_command(chat)
main.add_command(convert_group)
main.add_command(product_group)

if __name__ == '__main__':
    main()
