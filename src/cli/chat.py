"""
CLI commands for AI chat.
"""

import asyncio
import os
import click
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.planners.function_calling_stepwise_planner import (
    FunctionCallingStepwisePlanner
)
from octopus_energy.plugins.consumption import ConsumptionPlugin

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
@click.option('--openai-org-id', 'openai_org_id',
              type=click.STRING,
              default=os.environ['OPENAI_ORGANISATION_ID'],
              help='The Open AI organisation ID (Not recommended).')
@click.option('--model', '-m', 'model',
              type=click.STRING,
              default='gpt-3.5-turbo',
              help='The AI model to chat with.')
def chat(api_key: str,
         meter_mpan: str,
         meter_serial: str,
         openai_api_key: str,
         openai_org_id: str,
         model: str
    ):
    """
    Work with Octopus Energy data via natural language chat.
    """
    kernel = Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            api_key=openai_api_key,
            org_id=openai_org_id,
            ai_model_id=model,
            service_id='default'
        )
    )

    kernel.add_plugin(ConsumptionPlugin(api_key, meter_mpan, meter_serial), 'ConsumptionPlugin')
    planner = FunctionCallingStepwisePlanner(service_id='default')

    while True:
        user_input = input('User > ')
        result = asyncio.run(planner.invoke(kernel, user_input))
        print(f'Copilot > {result.final_answer}')
