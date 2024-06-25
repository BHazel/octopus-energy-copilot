"""
Builder for the web UI for the bill CLI command.
"""

from gradio import Blocks, File, Interface, Textbox
from bill.extraction import BillExtractor
from bill.model import EnergyBill
from cli import create_json_output
from cli.ui import BaseUiBuilder

class BillUiBuilder(BaseUiBuilder):
    """
    Builds the web UI for the bill CLI command.
    """
    def __init__(self,
                 bill_extractor: BillExtractor,
                 query: str = None):
        """
        Initialises an instance of the BillUiBuilder class.

        Args:
            bill_extractor: BillExtractor: The bill extractor.
            query: str: The JMESPath query.
                Defaults to None.
        """
        self.bill_extractor = bill_extractor
        self.query = query

    def build_ui(self) -> Blocks:
        """
        Builds the web UI.
        """
        return Interface(self.extract_bill_information,
                         title='Octopus Energy Copilot: Extract Bill Information',
                         description='Extracts information from an energy bill.',
                         inputs=[
                             File(label='Bill File'),
                             Textbox(label='JMESPath Query', value=self.query)
                         ],
                         outputs='json')

    def extract_bill_information(self, bill_file: str, query: str):
        """
        Extracts bill information.

        Args:
            bill_file: str: The bill file.
            query: str: The JMESPath query.
        """
        bill: EnergyBill = self.bill_extractor.extract_bill_information(bill_file)
        output = create_json_output(bill, query)
        return output
