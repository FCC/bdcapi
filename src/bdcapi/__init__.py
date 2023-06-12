# -*- coding: utf-8 -*-

__version__     =   '1.0.0'
__pkg_root__    =   __package__ or 'bdcapi'

import sys
import click

from bdcapi.common.cli import (
    config_option,
    verbose_option,
)
from bdcapi.common.api import BaseAPITask
from bdcapi.fixed import fixed
# from bdcapi.fabric import fabric


sys.tracebacklimit  =   0


#
# CLI Commands
#


CONTEXT_SETTINGS    =   dict(
                            help_option_names=[ '-h', '--help' ],
                            token_normalize_func=lambda x: x.lower(),
                        )

pass_task = click.make_pass_decorator(BaseAPITask, ensure=True)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.version_option(sys.version, '--python-version', prog_name='Python')
def cli(**kwargs):
    pass


#
# Generate Config File
#


@cli.command()
@config_option
@verbose_option
@pass_task
def initialize( task, **kwargs ):
    """
    """
    task.config.generate_config()


cli.add_command(fixed)
# cli.add_command(fabric)


if __name__ == '__main__':
    cli()