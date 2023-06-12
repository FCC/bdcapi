# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import requests
import click

from bdcapi import __pkg_root__

#
# Common exceptions
#


class ClobberError(Exception):

    def __init__(self, value='clobber caught'):
        self.value  =   value


    def __str__(self):
        return repr(self.value)



class TaskError(Exception):

    def __init__(self, value='task error caught'):
        self.value  =   value


    def __str__(self):
        return repr(self.value)


#
# Common methods
#

#
# Initialization helper methods
#

def init_basic_logger(  logformat='%(asctime)s -- %(levelname)s - %(message)s', dateformat='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO, **kwargs ):
    """
    """
    import logging

    logging.basicConfig(
        format=logformat,
        datefmt=dateformat,
        level=level,
        **kwargs
    )

    return logging.getLogger(__pkg_root__)


def set_log_level( level, logger=None ):
    """
    Sets current log level based upon string or integer level argument
    """
    import logging

    if not isinstance(logger, logging.Logger):
        logger      =   logging.getLogger(__pkg_root__)

    levels      =   [ 'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' ]

    if isinstance(level, str) and level.upper() in levels:
        level   =   getattr(logging, level.upper())
    if not isinstance(level, int):
        level   =   logging.INFO
    
    logger.setLevel(level)


#
# Override requests.Session to handle retries
#

class APISession(requests.Session):
    
    def __init__(self):
        """
        """
        from collections import OrderedDict
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry

        retry_strategy  =   Retry(
                                total=3,
                                backoff_factor=10,
                                status_forcelist=[429, 503]
                            )

        adapter         =   HTTPAdapter(max_retries=retry_strategy)

        super().__init__()
        
        self.mount('https://', adapter)
        self.mount('http://', adapter)

        assert_status_hook      =   lambda response, *args, **kwargs: response.raise_for_status()
        self.hooks['response']  =   [assert_status_hook]

#
# Override click.Option for mutual exclusivity
#


# class OptionPromptNull(click.Option):
#     _value_key = '_default_val'

#     def __init__(self, *args, **kwargs):
#         self.default_option = kwargs.pop('default_option', None)
#         super(OptionPromptNull, self).__init__(*args, **kwargs)

#     def get_default(self, ctx, **kwargs):
#         if not hasattr(self, self._value_key):
#             if self.default_option is None:
#                 default = super(OptionPromptNull, self).get_default(ctx, **kwargs)
#             else:
#                 arg = ctx.params[self.default_option]
#                 default = self.type_cast_value(ctx, self.default(arg))
#             setattr(self, self._value_key, default)
#         return getattr(self, self._value_key)

#     def prompt_for_value(self, ctx):
#         default = self.get_default(ctx)

#         # only prompt if the default value is None
#         if default is None:
#             return super(OptionPromptNull, self).prompt_for_value(ctx)

#         return default


# class Mutex(click.Option):
#     def __init__(self, *args, **kwargs):
#         self.not_required_if: list = kwargs.pop("not_required_if")

#         assert self.not_required_if, "'not_required_if' parameter required"
#         kwargs["help"] = (kwargs.get("help", "") + "Option is mutually exclusive with " + ", ".join(self.not_required_if) + ".").strip()
#         super(Mutex, self).__init__(*args, **kwargs)

    
#     def handle_parse_result(self, ctx, opts, args):
#         current_opt: bool = self.consume_value(ctx, opts)
        
#         for other_param in ctx.command.get_params(ctx):
#             if other_param is self:
#                 continue
#             print('current opt:%s -- param:%s' % ( self.human_readable_name, other_param.human_readable_name ))
#             if other_param.human_readable_name in self.not_required_if:
#                 other_opt: bool = other_param.consume_value(ctx, opts)
#                 print('current opt:%s -- other_opt:%s' % ( self.human_readable_name, other_opt ))
#                 if other_opt:
#                     if current_opt:
#                         raise click.UsageError(
#                             "Illegal usage: '" + str(self.name)
#                             + "' is mutually exclusive with "
#                             + str(other_param.human_readable_name) + "."
#                         )
#                     else:
#                         self.prompt = None
#                         self.required = None
        
#         return super(Mutex, self).handle_parse_result(ctx, opts, args)


# class FileContentOverrideOption(click.Option):
#     def __init__(self, *args, **kwargs):
#         self.override: str = kwargs.pop("override")

#         assert self.override, "'override' parameter required"
#         kwargs["help"] = (kwargs.get("help", "") + "Option overrides " + self.override + ".").strip()
#         super(FileContentOverrideOption, self).__init__(*args, **kwargs)

    
#     def handle_parse_result(self, ctx, opts, args):
#         current_opt: bool = self.consume_value(ctx, opts)
        
#         for other_param in ctx.command.get_params(ctx):
#             if other_param is self:
#                 continue
#             print('current opt:%s -- param:%s' % ( self.human_readable_name, other_param.human_readable_name ))
#             if other_param.human_readable_name == self.override:
#                 other_param.default     =   
#                 other_opt: bool = other_param.consume_value(ctx, opts)
#                 print('current opt:%s -- other_opt:%s' % ( self.human_readable_name, other_opt ))
#                 if other_opt:
#                     if current_opt:
#                         raise click.UsageError(
#                             "Illegal usage: '" + str(self.name)
#                             + "' is mutually exclusive with "
#                             + str(other_param.human_readable_name) + "."
#                         )
#                     else:
#                         self.prompt = None
#                         self.required = None
        
#         return super(Mutex, self).handle_parse_result(ctx, opts, args)

#
#
#