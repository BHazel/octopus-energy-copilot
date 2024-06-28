"""
Main program entry point.
"""

import click
from cli.account import account_group
from cli.bill import bill_group
from cli.chat import chat
from cli.consumption import consumption_group
from cli.product import product_group

@click.group()
@click.version_option('0.0.1', prog_name='Octopus Energy Copilot CLI')
@click.help_option('-h', '--help')
def main():
    """
    Root command for the Octopus Energy Copilot CLI.
    """

main.add_command(account_group)
main.add_command(bill_group)
main.add_command(consumption_group)
main.add_command(chat)
main.add_command(product_group)

if __name__ == '__main__':
    main()
