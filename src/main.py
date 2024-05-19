"""
Main program entry point.
"""

import click
from cli.chat import chat
from cli.consumption import consumption_group

@click.group()
@click.version_option('0.0.1', prog_name='Octopus Energy Copilot CLI')
@click.help_option('-h', '--help')
def main():
    """
    Root command for the Octopus Energy Copilot CLI.
    """

main.add_command(consumption_group)
main.add_command(chat)

if __name__ == '__main__':
    main()
