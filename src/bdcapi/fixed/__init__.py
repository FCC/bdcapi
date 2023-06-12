# -*- coding: utf-8 -*-

import click
from bdcapi.common.api import BaseAPITask
from bdcapi.fixed.response import response
from bdcapi.fixed.challenge import challenge
from bdcapi import __pkg_root__

pass_task = click.make_pass_decorator(BaseAPITask, ensure=True)

@click.group()
@pass_task
def fixed(task):
    pass

fixed.add_command(response)
fixed.add_command(challenge)


#
#
#