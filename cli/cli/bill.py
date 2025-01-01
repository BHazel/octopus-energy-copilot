"""
CLI commands for working with energy bills.
"""

import os
import sys
import click
from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from bill.extraction import BillExtractor
from bill.model import EnergyBill
from . import create_json_output
from .ui.bill import BillUiBuilder

load_dotenv()

@click.group('bill')
def bill_group():
    """
    Commands for working with energy bills.
    """

@bill_group.command('read')
@click.option('--openai-api-key', 'openai_api_key',
              type=click.STRING,
              default=os.environ['OPENAI_API_KEY'],
              help='The Open AI API key (Not recommended).')
@click.option('--model', '-m', 'model',
              type=click.STRING,
              default='gpt-3.5-turbo',
              help='The AI model to power the chat.')
@click.option('-f', '--file', 'file',
                type=click.STRING,
                default=None,
                help='The energy bill filename to read.')
@click.option('-q', '--query', 'query',
              type=click.STRING,
              default=None,
              help='The JMESPath query to filter and structure the output.')
@click.option('--ui', 'ui',
              type=click.BOOL,
              is_flag=True,
              help='Use a web user interface to extract bill data.  Any file argument will be ignored.')
@click.option('-o', '--open', 'open_in_browser',
              type=click.BOOL,
              is_flag=True,
              help='Open the UI in the default web browser.  Ignored if not using a web user interface.')
def read_bill(openai_api_key: str,
              model: str,
              query: str,
              file: str,
              ui: bool,
              open_in_browser: bool
    ):
    """
    Reads an energy bill from a file.
    """
    llm_chat_model: BaseChatModel = ChatOpenAI(api_key=openai_api_key, model=model)
    bill_extractor: BillExtractor = BillExtractor(llm_chat_model)

    if ui:
        use_web_ui(bill_extractor, query, open_in_browser)
    else:
        use_cli(bill_extractor, file, query)

def use_web_ui(bill_extractor: BillExtractor, query: str, open_in_browser: bool):
    """
    Uses a web UI for the bill extraction.
    """
    bill_ui_builder = BillUiBuilder(bill_extractor, query)
    interface = bill_ui_builder.build_ui()
    interface.launch(inbrowser=open_in_browser)

def use_cli(bill_extractor: BillExtractor, bill_file: str, query: str):
    """
    Uses a CLI interface for the bill extraction.
    """
    if bill_file is None:
        print('You must provide a bill file.')
        sys.exit(1)

    bill: EnergyBill = bill_extractor.extract_bill_information(bill_file)
    output = create_json_output(bill, query)
    print(output)
