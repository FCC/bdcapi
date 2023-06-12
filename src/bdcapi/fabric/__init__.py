# -*- coding: utf-8 -*-

import click
from bdcapi.common.api import BaseAPITask
# from .challenge import challenge

pass_task = click.make_pass_decorator(BaseAPITask, ensure=True)

@click.group()
@pass_task
def fabric(task):
    pass

# fabric.add_command(challenge)


#
#
#