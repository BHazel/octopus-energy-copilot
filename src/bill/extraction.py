"""
A class to extract information from energy bills.
"""

import os
import json
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from pypdf import PdfReader

from bill.model import EnergyBill

class BillExtractor:
    """
    Extracts information from energy bills.
    """
    def __init__(self,
                 chat_model: BaseChatModel
        ):
        """
        Initialises an instance of the BillExtractor class.

        Args:
            chat_model (BaseChatModel): The chat model to use.
        """
        self.chat_model = chat_model

        self.initialise()

    def initialise(self) -> None:
        """
        Initialises the chat infrastructure.
        """
        bill_extractor_prompt_path = f'{os.path.dirname(__file__)}/../assets/bill_extractor_prompt.txt'
        with open(bill_extractor_prompt_path, 'r', encoding='utf-8') as bill_extractor_prompt_file:
            self.bill_extractor_prompt = bill_extractor_prompt_file.read()

        self.chat_history = [SystemMessage(self.bill_extractor_prompt)]

    def extract_bill_information(self, bill_file: str) -> EnergyBill:
        """
        Extract information from a bill file.

        Args:
            bill_file (str): The bill filename.
        """
        bill_text = self.extract_bill_text(bill_file)
        self.chat_history.append(HumanMessage(bill_text))
        ai_response = self.chat_model.invoke(self.chat_history)
        energy_bill_data = json.loads(ai_response.content)
        energy_bill = EnergyBill(**energy_bill_data)
        return energy_bill

    def extract_bill_text(self, bill_file: str) -> str:
        """
        Extracts the text from a bill file.

        Args:
            bill_file (str): The bill filename.
        """
        pdf_reader = PdfReader(bill_file)
        bill_pages = [f'PAGE START\n{page.extract_text()}\nPAGE END' for page in pdf_reader.pages]
        bill_text = '\n'.join(bill_pages)
        return bill_text
