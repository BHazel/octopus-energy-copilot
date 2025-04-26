# Octopus Energy Copilot

Tools and AI for working with data from Octopus Energy, energy bills and energy units.

## Technologies

* Python
* LangChain
* MCP

## Concepts

The Copilot has been designed as a collection of standard Python reusable packages for use in front-end applications:

Package | Description
-|-
`bill` | Works with and extracts data from energy bills.
`chat` | Chat infrastructure for working with Octopus Energy and generic energy data.
`energy` | Energy data units and operations.
`octopus_energy` | Infrastructure and models for working with the Octopus Energy API and data.

A CLI, using the packages, is included in the `cli` directory.

## Getting Started with the CLI

Although it is optional, it is highly recommended to use a virtual environment.  In fact, the included MCP server configuration expects one in the `./.venv` folder.  A GNU Make target is included to create the virtual environment and set up a `.env` file:

```bash
make init
```

The CLI is also packaged as a standard Python package and can be built and installed from within the `cli` directory.  By default the CLI build and installation is run in _editable_ mode.

The simplest installation is to use GNU Make by running:

```bash
make install
```

Alternatively, each step can be run individually, which is how the `Makefile` is written under the hood:

```bash
pip install build           # Install build dependencies.
pip install --editable .    # Install CLI dependencies.
python -m build             # Build and install CLI.
```

For a non-editable build append `RELEASE=1` to the `make` command or remove `--editable` when installing the CLI dependencies.

Once built the CLI can be run with the `oec` command.  To get a list of the available commands, run:

```bash
oec --help
```

### Configuration

To interact with the Octopus Energy API you need to set your API key, meter MPAN, serial number and account number as environment variables as outlined below:

Environment Variable | Description
-|-
`OCTOPUS_ENERGY_ACCOUNT_NUMBER` | The Octopus Energy Account Number
`OCTOPUS_ENERGY_API_KEY` | The Octopus Energy API Key
`OCTOPUS_ENERGY_METER_MPAN` | The Electricity Meter MPAN
`OCTOPUS_ENERGY_METER_SERIAL` | The Electricity Meter Serial Number

These can be configured via standard OS settings or by creating a `.env` file in the `cli` directory.  Instructions on the latter can be found on the [python-dotenv](https://pypi.org/project/python-dotenv/) site.  These can also be provided via CLI flags, however, this is not recommended.

To interact via the `chat` command you also need to set the following environment variables:

Environment Variable | Description
-|-
`OPENAI_API_KEY` | The Open AI API Key
`OPENAI_ORGANISATION_ID` | The Open AI Organisation Key