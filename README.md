# BDCAPI

## Introduction

BDCAPI is a proof-of-concept tool released by the [Federal Communications Commission](https://www.fcc.gov/) ("FCC") that allows users of the [Broadband Data Collection](https://bdc.fcc.gov/) ("BDC") system to interface via the BDC's Application Programming Interface ("API") endpoints. Currently, API endpoints are available for filers to manage Bulk Fixed Challenge submissions and for service provider filers to manage the Provider Fixed Challenge Response workflows. As additional API endpoints are made available, the BDCAPI tool will be updated to support these new endpoints.

For additional information on how to use the BDC Filer Interface system's API endpoints, please review the [BDC Filer Interface API documentation](https://us-fcc.app.box.com/v/bdc-fixed-response-api-spec) and the associated [BDC Filer Interface Swagger specification](https://us-fcc.app.box.com/v/bdc-fixed-response-api-swagger).

Additional information about the BDC program is available on the FCC's [Broadband Data Collection webpage](https://www.fcc.gov/BroadbandData).

## Installing

BDCAPI is a command-line script that supports Python 3.8 or higher.

Install and update using pip:

```console
pip install git+https://github.com/jonathanmccormack/bdcapi
```

## Usage

### Command-line

```console
Usage: bdcapi CATEGORY SUBCATEGORY COMMAND [options] [parameters]

The following top-level command categories are supported:
    initialize                      Initialize BDCAPI to generate configuration file
    fixed                           API endpoints for managing fixed challenge data

The following subcategories are supported within the "fixed" category:
    response                        API endpoints for managing provider fixed challenge responses
    challenge                       API endpoints for managing bulk fixed challenge submissions

The following commands are supported within the "fixed" category and "response" subcategory:
    submit-bulk-initial-response    Submit fixed challenge initial responses in bulk
    submit-bulk-final-response      Submit fixed challenge final responses in bulk
    revert-bulk-initial-response    Revert fixed challenge initial responses in bulk
    revert-bulk-final-response      Revert fixed challenge final responses in bulk
    certify-bulk-response           Certify to conceded or upheld fixed challenge in bulk

The following commands are supported within the "fixed" category and "challenge" subcategory:
    withdraw                        Withdraw accepted fixed challenges in bulk

Optional Parameters:
    -u, --username              Use specified username for API authentication
    -a, --api-token             Use specified token string for API authentication
    -b, --base-url              Override default base URL for API endpoints
        --clobber               Overwrite existing output file (if applicable)
        --verbose               Increase verbosity to DEBUG level
    -h, --help                  Show this usage message and quit
        --version               Show version information about this script
```

### Supported API Endpoints

There are currently 5 supported API endpoints using this script:

* Provider Fixed Challenge Response
  * Submit Bulk Initial Response
  * Submit Bulk Final Response
  * Revert Bulk initial Response
  * Revert Bulk Final Response
  * Certify Bulk Response
* Bulk Fixed Challenge
  * Withdraw

### Configuration

Out of the box, BDCAPI looks for a configuration YAML file named `config.yml` within a subfolder in the user's home directory.  This folder varies by platform, but by default is located at `~/.bdcapi/` on macOS and Linux platforms or `%LOCALAPPDATA%\bdcapi\` on Windows (e.g., `C:\Users\jane.doe\AppData\Local\bdcapi\`), and may be overridden with the `--config` option.

BDCAPI also looks for an API token key named `apitoken.key`, within this same subfolder, which may be overridden using the `--apitoken-file` option.  Alternatively, users may specify the appropriate API token hash value via the `--api-token` option rather than identifying a key file.

BDCAPI users may use a default configuration YAML file located in `bdcapi/src/pkg_data/defaults.yml` as the basis for the `config.yml` file, or else users may run the `initialize` command to write a configuration YAML and API token file to disk.

Commands have additional options and required arguments, which users can view by running `bdcapi CATEGORY SUBCATEGORY COMMAND --help` from the command line.