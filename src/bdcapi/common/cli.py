# -*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path

import click

from bdcapi.common.api import BaseAPITask
from bdcapi.common.config import (
    default_configfile,
    default_tokenfile,
    AppConfig,
)
# from bdcapi.common import Mutex

#
# Main options
#


def username_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        if value:
            task.username   =   value
        return value
    
    return click.option(
        '-u', '--username',
        type=str,
        prompt='BDC username',
        help='BDC Filer API username',
        callback=callback
    )(f)


def apitoken_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        if value:
            if len(value) == 44:
                task.apitoken   =   value
            else:
                raise click.BadParameter('BDC Filer API token must be a valid 44-character JSON web token')
        return value
    
    return click.option(
        '-t', '--apitoken',
        type=str,
        help='BDC Filer API token',
        callback=callback
    )(f)


def frn_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        if value:
            if value.isdigit() and (len(value) <= 10):
                task.frn    =   str(int(value)).zfill(10)
            else:
                raise click.BadParameter('FRN must be an integer or 10-digit zero-padded string')
        return value
    
    return click.option(
        '-f', '--frn',
        type=str,
        help='FRN of BDC Filer entity',
        callback=callback
    )(f)


def comment_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        task.args['comments']   =   value
        return value
    
    return click.option(
        '--comment',
        type=str,
        help='Narrative comment explaining or supporting submission',
        callback=callback
    )(f)


def apitoken_file_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        if not task.apitoken:
            if not (isinstance(value, Path) and value.is_file()):
                value   =   click.prompt(
                                'Path to API token file',
                                type=click.Path(path_type=Path, exists=True),
                                default=task.config.apifile
                            )
            task.apitoken   =   task.get_api_token(value)
        return value
    
    return click.option(
        '-a', '--apitoken-file',
        type=click.Path(path_type=Path),
        help='Plaintext file containing BDC Filer API token',
        callback=callback
    )(f)


def baseurl_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        task.baseurl    =   value
        return value
    
    return click.option(
        '--baseurl',
        type=str,
        default='https://bdc.fcc.gov/',
        help='Base URL for BDC Filer API calls',
        callback=callback
    )(f)


def chunk_size_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        task.args['chunk_size']  =   value
        return value
    
    return click.option(
        '--chunk-size',
        type=click.IntRange(min=1, max=1000),
        default=1000,
        help='Chunk size for processing bulk BDC Filer APIs',
        callback=callback
    )(f)


#
# Common options
#

def clobber_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        task.args['clobber']    =   value
        return value
    
    return click.option(
        '--clobber',
        is_flag=True, default=False,
        help='Overwrite existing output files',
        callback=callback
    )(f)


def dry_run_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        task.args['dry_run']    =   value
        return value
    
    return click.option(
        '--dry-run',
        is_flag=True, default=False,
        help='Conduct dry-run of action',
        callback=callback
    )(f)


def verbose_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        if value:
            sys.tracebacklimit  =   10
            task.set_log_level(logging.DEBUG)
        return value
    
    return click.option(
        '--verbose',
        is_flag=True, default=False,
        help='Toggle for logging verbosity between INFO and DEBUG',
        callback=callback
    )(f)


def config_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(BaseAPITask)
        task.config     =   AppConfig(value, logger=task.logger)
        ctx.default_map =   task.config.default_map()
        return value
    
    return click.option(
        '--config',
        type=click.Path(dir_okay=False),
        default=default_configfile,
        help='YAML file containing BDC Filer API configuration',
        callback=callback
    )(f)

#
# Common decorators
#


def common_options(f):
    for func in [ verbose_option ]:
        f = func(f)
    return f


def common_api_options(f):
    for func in [ username_option, apitoken_option, apitoken_file_option, baseurl_option, chunk_size_option ]:
        f = func(f)
    return f


#
#
#