"""
Builder for the web UI for the chat CLI command.
"""

import asyncio
import os
from gradio import ChatInterface, Info
from cli.ui import BaseUiBuilder
from chat.service import SemanticChatService

class ChatUiBuilder(BaseUiBuilder):
    """
    Builds the web UI for the chat CLI command.
    """
    def __init__(self,
                 chat_service: SemanticChatService,
                 debug: bool
        ):
        """
        Initialises an instance of the ChatUiBuilder class.

        Args:
            chat_service (OctopusEnergyChatService): The chat service.
            debug (bool): A value indicating whether more verbose output should be displayed.
        """
        self.chat_service = chat_service
        self.debug = debug
        self.example_chat_queries = self.get_example_chat_queries()

    def build_ui(self):
        """
        Builds the web UI.
        """
        return ChatInterface(self.post_message,
                             examples=self.example_chat_queries,
                             title='Octopus Energy Copilot: Chat',
                             description='An AI assistant to answer questions on your Octopus Energy account and data.')

    async def post_message(self, message, history):
        """
        Posts a message to the chat.

        This function is in the format expected by Gradio for its chat interface.

        Args:
            message (str): The message to post.
            history (list): The chat history.
        """
        for debug_message in await self.chat_service.post_message(message):
            if self.debug:
                Info(debug_message)

        return self.chat_service.chat_history[-1].content

    def get_example_chat_queries(self) -> list[str]:
        """
        Gets example chat queries.
        """
        example_chat_queries_path = f'{os.path.dirname(__file__)}/../../assets/example_chat_queries.txt'
        with open(example_chat_queries_path, 'r', encoding='utf-8') as example_chat_queries_file:
            example_chat_queries_text = example_chat_queries_file.read()
        return example_chat_queries_text.split('\n')
