# -*- coding: utf-8 -*-

import logging

from bdcapi.common.helpers import (
    init_basic_logger,
    set_log_level,
    APISession,
)
from bdcapi.common.config import AppConfig

#
# Base API Task
#


class BaseAPITask(object):

    def __init__(self):
        """
        """
        self.baseurl    =   None
        
        self.username   =   None
        self.apitoken   =   None

        self.args       =   {   'clobber':      False,
                                'dry_run':      False    }
        
        self.json       =   {}

        self.logger     =   init_basic_logger()
        self.config     =   None


    def build_headers(self, content_type='application/json', **kwargs):
        """
        """
        headers     =   {   'username':     self.username,
                            'hash_value':   self.apitoken,
                            'content_type': content_type,
                            **kwargs                        }

        return headers


    def perform_api_call(   self, method, apipath, username, apitoken, content_type='application/json',
                            params=None, data=None, json=None, files=None, **kwargs ):
        """
        """
        from urllib.parse import urljoin
        import requests

        url         =   urljoin(self.baseurl, apipath)
        headers     =   self.build_headers(username=username, apitoken=apitoken, content_type=content_type)

        with APISession() as session:
            try:
                response    =   session.request(
                                    method, url, headers=headers,
                                    data=data, params=params, json=json,
                                    files=files
                                )
                return response.json()
            except requests.exceptions.HTTPError as err:
                self.logger.error(
                    'HTTP %s response when making %s request for URL:%s', err.response.status_code, method.upper(), url
                )
                try:
                    self.logger.error('JSON error response:%s', err.response.json())
                except requests.exceptions.JSONDecodeError:
                    self.logger.error('Error response:%s', err.response)
                raise
            except requests.exceptions.JSONDecodeError as err:
                self.logger.error(
                    'Unexpected content for HTTP %s response when making %s request for urL:%s -- expected JSON',
                    err.response.status_code, method.upper(), url
                )
                raise
    
    
    def get_api_token(self, apifile):
        """
        """
        from pathlib import Path

        if hasattr(apifile, 'read'):
            # apifile appears to be a file pointer
            token       =   apifile.read()
        else:
            # assume apifile is a path to a valid file
            assert Path(apifile).is_file(), 'API token file does not exist or is not a valid file (file:%s)' % apifile
            
            with open(apifile, 'r') as fp:
                token       =   fp.read()

        return token


    def chunk_api_calls( self, items, chunk_size, rate_limit=2):
        """
        """
        import datetime as dt
        import math
        import time

        max_size        =   len(items)
        chunk_size      =   1000

        for i in range(0, max_size, chunk_size):
            self.logger.info('Processing calls to BDC API endpoint -- %s / %s', i, max_size)
            reqtime     =   dt.datetime.now()

            yield items[i:(i + chunk_size)]
            
            sleep_duration  =   math.ceil((60 / rate_limit) - (dt.datetime.now() - reqtime).total_seconds())

            if (i + chunk_size) < max_size and sleep_duration > 0:
                self.logger.debug('Waiting %s seconds to comply with rate limit ...', int(sleep_duration))
                time.sleep(sleep_duration)
    

    def set_log_level( self, level=logging.INFO ):
        """
        """
        set_log_level(level, self.logger)

#
#
#