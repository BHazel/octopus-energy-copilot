"""
CLI commands for AI chat.
"""

import os
import click
from colorama import Fore, Style
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from cli.ui.chat import ChatUiBuilder
from chat.service import ChatService

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
@click.option('--ui', 'ui',
              type=click.BOOL,
              is_flag=True,
              help='Use a web user interface for the chat.')
@click.option('-o', '--open', 'open_in_browser',
              type=click.BOOL,
              is_flag=True,
              help='Open the UI in the default web browser.  Ignored if not using a web user interface.')
def chat(api_key: str,
         number: str,
         meter_mpan: str,
         meter_serial: str,
         openai_api_key: str,
         model: str,
         debug: bool,
         ui: bool,
         open_in_browser: bool
    ):
    """
    Work with Octopus Energy data via natural language chat.
    """
    update_client_credentials(api_key, number, meter_mpan, meter_serial, openai_api_key)
    llm_chat_model = ChatOpenAI(api_key=openai_api_key, model=model)
    chat_service = ChatService(llm_chat_model)
    print_chat(COPILOT_MSG, 'Welcome to the Octopus Energy Copilot!')
    print_chat(COPILOT_MSG, f'Open AI Model: {model}', True, debug)

    if ui:
        use_web_ui(chat_service, debug, open_in_browser)
    else:
        use_cli(chat_service, debug)

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

def use_web_ui(chat_service: ChatService,
               debug: bool,
               open_in_browser: bool
    ) -> None:
    """
    Uses a web UI for the chat.

    Args:
        chat_service (OctopusEnergyChatService): The chat service.
        debug (bool): A value indicating whether more verbose output should be displayed.
    """
    chat_interface_builder = ChatUiBuilder(chat_service, debug)
    interface = chat_interface_builder.build_ui()
    interface.launch(inbrowser=open_in_browser)

def use_cli(chat_service: ChatService, debug: bool) -> bool:
    """
    Uses a CLI interface for the chat.

    Args:
        chat_service (OctopusEnergyChatService): The chat service.
        debug (bool): A value indicating whether more verbose output should be displayed.
    """
    while True:
        user_input = prompt_chat('User')
        for debug_message in chat_service.post_message(user_input):
            print_chat(COPILOT_MSG, debug_message, True, debug)

        print_chat(COPILOT_MSG, chat_service.chat_history[-1].content)

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
