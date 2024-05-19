"""
CLI commands for AI chat.
"""

import os
import click
from colorama import Fore, Style
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from octopus_energy.tools import tools

COPILOT_MSG = 'Copilot'

load_dotenv()

@click.command('chat')
@click.option('--api-key', 'api_key',
              type=click.STRING,
              default=os.environ['OCTOPUS_ENERGY_API_KEY'],
              help='The Octopus Energy API key (Not recommended).')
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
         meter_mpan: str,
         meter_serial: str,
         openai_api_key: str,
         model: str,
         debug: bool
    ):
    """
    Work with Octopus Energy data via natural language chat.

    Args:
        api_key (str): The Octopus Energy API key.
        meter_mpan (str): The electricity meter MPAN.
        meter_serial (str): The electricity meter serial number.
        openai_api_key (str): The Open AI API key.
        model (str): The AI model to power the chat.
        debug (bool): A value indicating whether to display more verbose output for debugging.
    """
    update_client_credentials(api_key, meter_mpan, meter_serial, openai_api_key)

    llm_chat = ChatOpenAI(api_key=openai_api_key, model=model)
    tool_functions = tools().values()
    chat_with_tools = llm_chat.bind_tools(tool_functions)
    main_chat_prompt = """
        You are a helpful AI assistant to answer questions about energy consumption data
        for an Octopus Energy customer.  Using the chat history context and data provided
        in JSON format answer the questions provided.  If you do not know the answer,
        please say so.  If you need more details from the customer, please ask for them.
    """
    chat_history = [SystemMessage(main_chat_prompt)]
    print_chat(COPILOT_MSG, 'Welcome to the Octopus Energy Copilot!')
    print_chat(COPILOT_MSG, f'Open AI Model: {model}', True, debug)

    while True:
        user_input = prompt_chat('User')
        chat_history.append(HumanMessage(user_input))
        ai_response = chat_with_tools.invoke(user_input)
        chat_history.append(ai_response)
        print_chat(COPILOT_MSG, f' Tool Calls: {ai_response.tool_calls}', True, debug)

        for tool_call in ai_response.tool_calls:
            selected_tool = tools()[tool_call['name']]
            tool_output = selected_tool.invoke(tool_call['args'])
            print_chat(COPILOT_MSG, f'Tool {tool_call['name']} Output: {tool_output}', True, debug)
            chat_history.append(ToolMessage(tool_output, tool_call_id=tool_call['id']))

        ai_response = llm_chat.invoke(chat_history)
        chat_history.append(ai_response)
        print_chat(COPILOT_MSG, ai_response.content)

def update_client_credentials(api_key: str = None,
                              meter_mpan: str = None,
                              meter_serial: str = None,
                              openai_api_key: str = None
    ) -> None:
    """
    Updates the Octopus Energy and Open AI client credentials.

    Args:
        api_key: The Octopus Energy API key.
        meter_mpan: The electricity meter MPAN.
        meter_serial: The electricity meter serial number.
        openai_api_key: The Open AI API key.
    """
    if api_key is not None:
        os.environ['OCTOPUS_ENERGY_API_KEY'] = api_key
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
