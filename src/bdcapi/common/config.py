# -*- coding: utf-8 -*-

from pathlib import Path

import click

from bdcapi.common.helpers import (
    init_basic_logger,
)
from bdcapi import __pkg_root__

#
# App Config
#

default_basepath    =   Path( click.get_app_dir(__pkg_root__, force_posix=True) )
default_configfile  =   Path( default_basepath, 'config.yml' )
default_tokenfile   =   Path( default_basepath, 'apitoken.key' )


class AppConfig(object):

    def __init__(self, cfgfile=default_configfile, apifile=default_tokenfile, logger=init_basic_logger()):
        """
        """
        import logging
        import yaml
        from pathlib import Path

        try:
            from importlib.resources import files
        except ImportError:
            from importlib_resources import files

        self.logger     =   logger

        # Load defaults
        with files(__pkg_root__).joinpath('pkg_data').joinpath('defaults.yml') as fp:
            if fp.is_file():
                self.defaults   =   yaml.safe_load(fp.read_text())
            else:
                self.logger.error('Default configuration file not found (path:%s)', fp)
                self.defaults   =   dict()
        
        self.cfgfile    =   Path( cfgfile )

        if self.cfgfile.is_file():
            self.logger.debug('Found configuration file (path:%s)', self.cfgfile)
            self.config     =   yaml.safe_load(self.cfgfile.read_text())
        else:
            self.logger.debug('No configuration file found (path:%s)', self.cfgfile)
            self.config     =   self.defaults
        
        self.apifile    =   Path( self.config.get('authentication', {}).get('apitoken_file') or apifile )


    def write_config(self, config, cfgfile=None, clobber=False):
        """
        """
        import stat
        import yaml

        if cfgfile is None:
            cfgfile     =   self.cfgfile

        cfgdir      =   cfgfile.parent
        if not cfgdir.is_dir():
            # Default permissions for cfgdir is RWX for owner / group and none for other
            umask       =   (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP)

            self.logger.debug('Creating configuration directory (path:%s umask:%s)', cfgdir, oct(umask))
            cfgdir.mkdir(mode=umask)
        
        if cfgfile.is_file() and clobber is False:
            self.logger.error('Configuration file already exists and clobber is False (path:%s)', cfgfile)
        else:
            self.logger.debug('Writing configuration file (path:%s)', cfgfile)
            with open(cfgfile, 'w') as fp:
                yaml.dump(config, fp, default_flow_style=False, sort_keys=False)
        

    def write_tokenfile(self, token, apifile=None, clobber=False):
        """
        """
        import stat

        if apifile is None:
            apifile     =   self.apifile
        
        apidir      =   apifile.parent
        if not apidir.is_dir():
            # Default permissions for cfgdir is RWX for owner / group and none for other
            umask       =   (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP)

            self.logger.debug('Creating API token directory (path:%s umask:%s)', apidir, oct(umask))
            apidir.mkdir(mode=umask)
        
        if apifile.is_file() and clobber is False:
            self.logger.error('API token file already exists and clobber is False (path:%s)', apifile)
        else:
            self.logger.debug('Writing API token file (path:%s)', apifile)
            with open(apifile, 'w') as fp:
                fp.write(token)
    

    def generate_config(self):
        """
        """
        import click

        config  =   self.config

        config['baseurl']   =   click.prompt(
                                    'BDC base URL',
                                    type=str,
                                    default=config.get('baseurl')
                                )

        # Define authentication items
        config['authentication']                =   config.get('authentication', {})

        config['authentication']['username']    =   click.prompt(
                                                        'BDC username',
                                                        type=str,
                                                        default=config['authentication'].get('username')
                                                    )
        config['authentication']['apitoken']    =   click.prompt(
                                                        'API token string',
                                                        type=str,
                                                        default=config['authentication'].get('apitoken')
                                                    )
        
        # Define common items
        config['common']                            =   config.get('common', {})
        config['common']['challenge_file_column']   =   click.prompt(
                                                            'CSV column header in challenge file(s) containing challenge ID',
                                                            type=str,
                                                            default=config['common'].get('challenge_file_column')
                                                        )
        config['common']['frn']                     =   click.prompt(
                                                            'Primary FRN (optional)',
                                                            value_proc=lambda x: str(int(x)).zfill(10) if x else None,
                                                            default=config['common'].get('frn') or ''
                                                        )
        
        # Define contact items
        # TODO
        #
        config['common']['certifier']       =   config.get('contacts', {}).get('certifier', {})

        # Define fixed challenge items
        config['fixed']                     =   config.get('fixed', {})

        config['fixed']['challenge']        =   config['common']
        config['fixed']['response']         =   config['common']

        use_tokenfile   =   click.confirm(
                                'Store API token in separate API token file',
                                prompt_suffix='? ',
                                default=True
                            )
        
        if use_tokenfile:
            apifile     =   click.prompt(
                                'Path in which to store API token file',
                                type=click.Path(path_type=Path),
                                default=self.apifile
                            )
            
            if apifile.exists():
                clobber =   click.confirm(
                                'API token file already exists. Overwrite',
                                prompt_suffix='? ',
                                default=False
                            )
            else:
                clobber =   False

            self.write_tokenfile(
                config['authentication']['apitoken'],
                apifile=config['authentication']['apitoken_file'],
                clobber=clobber
            )

            config['authentication']['apitoken_file']   =   str(apifile)
            config['authentication']['apitoken']        =   None
        else:
            config['authentication']['apitoken_file']   =   None
        
        cfgfile     =   click.prompt(
                            'Path in which to store configuration file',
                            type=click.Path(path_type=Path),
                            default=self.cfgfile
                        )

        if cfgfile.exists():
            clobber =   click.confirm(
                            'Configuration file already exists. Overwrite',
                            prompt_suffix='? ',
                            default=False
                        )
        else:
            clobber =   False
        
        self.write_config(
            config,
            cfgfile=cfgfile,
            clobber=clobber
        )
    

    def default_map(self):
        """
        """
        mapdict     =   {
            'fixed':    {
                'response': {
                    'submit-bulk-initial-response': {},
                    'submit-bulk-final-response':   {},
                    'revert-bulk-initial-response': {},
                    'revert-bulk-final-response':   {},
                    'certify-bulk-response':    {
                        'certifying_name':      self.config.get('fixed', {}).get('response', {}).get('certifier', {}).get('name'),
                        'certifying_title':     self.config.get('fixed', {}).get('response', {}).get('certifier', {}).get('title'),
                        'certifying_email':     self.config.get('fixed', {}).get('response', {}).get('certifier', {}).get('email'),
                        'certifying_phone':     self.config.get('fixed', {}).get('response', {}).get('certifier', {}).get('phone'),
                        'certifying_phone_ext': self.config.get('fixed', {}).get('response', {}).get('certifier', {}).get('extension'),
                    },
                    'challenge_file_column':    self.config.get('fixed', {}).get('response', {}).get('challenge_file_column'),
                    'frn':                      self.config.get('fixed', {}).get('response', {}).get('frn'),
                },
                'challenge': {
                    'withdraw':                 {},
                    'challenge_file_column':    self.config.get('fixed', {}).get('challenge', {}).get('challenge_file_column'),
                    'frn':                      self.config.get('fixed', {}).get('challenge', {}).get('frn'),
                },
            },
            'fabric':   {
                'challenge': {
                    'withdraw':     {},
                },
            },
            'username':         self.config.get('authentication', {}).get('username'),
            'apitoken':         self.config.get('authentication', {}).get('apitoken'),
            'apitoken_file':    self.config.get('authentication', {}).get('apitoken_file'),
            'baseurl':          self.config.get('baseurl'),
            'verbose':          self.config.get('verbose'),
        }

        return mapdict


#
#
#