"""
CLI commands for working with energy bills.
"""

import os
import click
from dotenv import load_dotenv
from gradio import File, Interface, Textbox
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from bill.extraction import BillExtractor
from bill.model import EnergyBill
from cli import create_json_output

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
              help='Use a web user interface for the chat.  Any file argument will be ignored.')
def read_bill(openai_api_key: str,
              model: str,
              query: str,
              file: str,
              ui: bool
    ):
    """
    Reads an energy bill from a file.
    """
    llm_chat_model: BaseChatModel = ChatOpenAI(api_key=openai_api_key, model=model)
    bill_extractor: BillExtractor = BillExtractor(llm_chat_model)

    if ui:
        use_web_ui(bill_extractor, query)
    else:
        use_cli(bill_extractor, file, query)

def use_web_ui(bill_extractor: BillExtractor, query: str):
    """
    Uses a web UI for the bill extraction.
    """
    def extract_bill_information(bill_file: str, query: str):
        """
        Extracts bill information.
        """
        bill: EnergyBill = bill_extractor.extract_bill_information(bill_file)
        output = create_json_output(bill, query)
        return output

    interface = Interface(extract_bill_information,
                          inputs=[
                              File(label='Bill File'),
                              Textbox(label='JMESPath Query')
                          ],
                          outputs='json')
    interface.launch()

def use_cli(bill_extractor: BillExtractor, bill_file: str, query: str):
    """
    Uses a CLI interface for the bill extraction.
    """
    if bill_file is None:
        print('You must provide a bill file.')
        exit(1)

    bill: EnergyBill = bill_extractor.extract_bill_information(bill_file)
    output = create_json_output(bill, query)
    print(output)
