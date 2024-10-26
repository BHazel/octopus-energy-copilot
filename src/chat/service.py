"""
A service to work with Octopus Energy and other data and functions via AI chat.
"""

from datetime import datetime
import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments
import xmltodict
from chat.plugins.account import AccountPlugin
from chat.plugins.consumption import ConsumptionPlugin
from chat.plugins.conversion import ConversionPlugin

class SemanticChatService:
    """
    Works with Octopus Energy and other data and functions via AI chat.
    """
    def __init__(self,
                 chat_client: ChatCompletionClientBase
        ):
        self.chat_client = chat_client
        self.initialise()

    def initialise(self) -> None:
        self.kernel = Kernel()
        self.kernel.add_service(self.chat_client)

        self.kernel.add_plugin(AccountPlugin(), plugin_name='Account')
        self.kernel.add_plugin(ConsumptionPlugin(), plugin_name='Consumption')
        self.kernel.add_plugin(ConversionPlugin(), plugin_name='Conversion')

        self.execution_settings = OpenAIChatPromptExecutionSettings()
        self.execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

        main_chat_prompt_path = f'{os.path.dirname(__file__)}/../assets/main_chat_prompt.txt'
        with open(main_chat_prompt_path, 'r', encoding='utf-8') as main_chat_prompt_file:
            self.main_chat_prompt = main_chat_prompt_file.read()

        self.chat_history = ChatHistory()
        self.chat_history.add_system_message(self.main_chat_prompt)
        self.chat_history.add_assistant_message(f'The date today is {datetime.now()}')

    async def post_message(self, message: str):
        self.chat_history.add_user_message(message)
        ai_response = await self.chat_client.get_chat_message_content(
            chat_history=self.chat_history,
            settings=self.execution_settings,
            kernel=self.kernel,
            arguments=KernelArguments()
        )

        self.chat_history.add_message(ai_response)
        yield str(self.chat_history)
