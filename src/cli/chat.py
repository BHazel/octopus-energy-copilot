"""
CLI commands for AI chat.
"""

import os
import click
from colorama import Fore, Style
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from octopus_energy.chat import OctopusEnergyChatService

COPILOT_MSG = 'Copilot'

load_dotenv()

@click.command('chat')
@click.option('--api-key', 'api_key',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_API_KEY'],
              help='The Octopus Energy API key (Not recommended).')
@click.option('-n', '--number', 'number',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_ACCOUNT_NUMBER'],
              help='The account number (Not recommended).')
@click.option('--meter-mpan', 'meter_mpan',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_METER_MPAN'],
              help='The electricity meter MPAN.')
@click.option('--meter-serial', 'meter_serial',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_METER_SERIAL'],
              help='The electricity meter serial number.')
@click.option('--openai-api-key', 'openai_api_key',
              type=click.STRING,
              default=os.environ['OPENAI_API_KEY'],
              help='The Open AI API key (Not recommended).')
@click.option('--model', '-m', 'model',
              type=click.STRING,
              default='gpt-3.5-turbo',
              help='The AI model to power the chat.')
@click.option('--debug', 'debug',
              type=click.BOOL,
              is_flag=True,
              help='Display more verbose output for debugging.')
def chat(api_key: str,
         number: str,
         meter_mpan: str,
         meter_serial: str,
         openai_api_key: str,
         model: str,
         debug: bool
    ):
    """
    Work with Octopus Energy data via natural language chat.
    """
    update_client_credentials(api_key, number, meter_mpan, meter_serial, openai_api_key)
    llm_chat_model = ChatOpenAI(api_key=openai_api_key, model=model)
    chat_service = OctopusEnergyChatService(api_key, None, meter_mpan, meter_serial, llm_chat_model)
    print_chat(COPILOT_MSG, 'Welcome to the Octopus Energy Copilot!')
    print_chat(COPILOT_MSG, f'Open AI Model: {model}', True, debug)

    while True:
        user_input = prompt_chat('User')
        for debug_message in chat_service.post_message(user_input):
            print_chat(COPILOT_MSG, debug_message, True, debug)

        print_chat(COPILOT_MSG, chat_service.chat_history[-1].content)

def update_client_credentials(api_key: str = None,
                              number: str = None,
                              meter_mpan: str = None,
                              meter_serial: str = None,
                              openai_api_key: str = None
    ) -> None:
    """
    Updates the Octopus Energy and Open AI client credentials.

    Args:
        api_key: The Octopus Energy API key.
        number: The Octopus Energy account number.
        meter_mpan: The electricity meter MPAN.
        meter_serial: The electricity meter serial number.
        openai_api_key: The Open AI API key.
    """
    if api_key is not None:
        os.environ['OCTOPUS_ENERGY_API_KEY'] = api_key
    if number is not None:
        os.environ['OCTOPUS_ENERGY_ACCOUNT_NUMBER'] = number
    if meter_mpan is not None:
        os.environ['OCTOPUS_ENERGY_METER_MPAN'] = meter_mpan
    if meter_serial is not None:
        os.environ['OCTOPUS_ENERGY_METER_SERIAL'] = meter_serial
    if openai_api_key is not None:
        os.environ['OPENAI_API_KEY'] = openai_api_key

def prompt_chat(source: str) -> str:
    """
    Prompts a chat message.

    Args:
        source (str): The source of the message.
    """
    return input(f'{Fore.GREEN}{source} >{Fore.RESET} ')

def print_chat(source: str,
               message: str,
               is_debug: bool = False,
               debug_mode: bool = False
) -> None:
    """
    Prints a chat message.

    Args:
        source (str): The source of the message.
        message (str): The message to print.
        is_debug (bool): A value indicating whether the message is for debugging.
        debug_mode (bool): A value indicating whether to display the message for debugging.
    """
    entity_colour = Fore.BLUE if is_debug else Fore.YELLOW
    message_colour = Style.DIM if is_debug else Style.NORMAL

    source = f'{source} (Debug)' if is_debug else source
    if (debug_mode and is_debug) or (not debug_mode and not is_debug):
        print(f'{entity_colour}{source} >{Fore.RESET} {message_colour}{message}{Style.RESET_ALL}')
