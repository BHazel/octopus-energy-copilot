# Octopus Energy Copilot

Tools and AI for working with data from Octopus Energy.

## Technologies

* Python
* LangChain

## Getting Started

The Copilot is designed as a CLI application.  For a list of the main options and commands run from the `src` directory:

```bash
python main.py --help
```

### Configuration

To interact with the Octopus Energy API you need to set your API key, meter MPAN and serial number as environment variables as outlined below:

Environment Variable | Description
-|-
`OCTOPUS_ENERGY_API_KEY` | The Octopus Energy API Key
`OCTOPUS_ENERGY_METER_MPAN` | The Electricity Meter MPAN
`OCTOPUS_ENERGY_METER_SERIAL` | The Electricity Meter Serial Number

These can be configured via standard OS settings or by creating a `.env` file in the `src` directory.  Instructions on the latter can be found on the [python-dotenv](https://pypi.org/project/python-dotenv/) site.

To interact via the `chat` command you also need to set the following environment variables:

Environment Variable | Description
-|-
`OPENAI_API_KEY` | The Open AI API Key