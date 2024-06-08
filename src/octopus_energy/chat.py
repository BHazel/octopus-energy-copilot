"""
A service to work with Octopus Energy data via AI chat.
"""

from datetime import datetime
import os
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from octopus_energy.tools import tools

class OctopusEnergyChatService:
    """
    Works with Octopus Energy data via AI chat.
    """
    def __init__(self,
                 api_key: str,
                 account_number: str,
                 meter_mpan: str,
                 meter_serial: str,
                 chat_model: BaseChatModel
    ):
        """
        Initializes the Octopus Energy chat.

        Args:
            api_key: The Octopus Energy API key.
            account_number: The account number.
            meter_mpan: The electricity meter MPAN.
            meter_serial: The electricity meter serial number.
            chat_model: The Open AI model.
        """
        self.api_key = api_key
        self.meter_mpan = meter_mpan
        self.meter_serial = meter_serial
        self.account_number = account_number
        self.chat_model = chat_model

        self.initialise()

    def initialise(self) -> None:
        """
        Initialises the chat infrastructure.
        """
        self.runnable_chat = self.chat_model.bind_tools(tools().values())
        main_chat_prompt_path = f'{os.path.dirname(__file__)}/../assets/main_chat_prompt.txt'
        with open(main_chat_prompt_path, 'r', encoding='utf-8') as main_chat_prompt_file:
            self.main_chat_prompt = main_chat_prompt_file.read()

        self.chat_history = [SystemMessage(self.main_chat_prompt)]
        self.chat_history.append(HumanMessage(f'The date today is {datetime.now()}'))

    def post_message(self, message: str):
        """
        Posts a message to the chat.

        Args:
            message: The message to post.
        """
        self.chat_history.append(HumanMessage(message))
        ai_response = self.runnable_chat.invoke(self.chat_history)
        self.chat_history.append(ai_response)
        yield f'Tool Calls: {ai_response.tool_calls}'

        for tool_call in ai_response.tool_calls:
            selected_tool = tools()[tool_call['name']]
            tool_output = selected_tool.invoke(tool_call['args'])
            yield f'Tool {tool_call['name']} Output: {tool_output}'
            self.chat_history.append(ToolMessage(tool_output, tool_call_id=tool_call['id']))

        ai_response = self.runnable_chat.invoke(self.chat_history)
        self.chat_history.append(ai_response)
