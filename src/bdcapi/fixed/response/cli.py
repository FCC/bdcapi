import click
from bdcapi.common.cli import (
    common_api_options,
    comment_option,
    verbose_option,
    config_option,
    frn_option,
)
from bdcapi.fixed.response.api import ProviderResponseAPITask
from bdcapi import __pkg_root__


pass_task = click.make_pass_decorator(ProviderResponseAPITask, ensure=True)


#
# Main options
#


def evidence_id_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(ProviderResponseAPITask)
        if value:
            if value.isdigit():
                task.args['evidence_id']    =   value
            else:
                raise click.BadParameter('Evidence ID must be a numeric string')
        return value
    
    return click.option(
        '--evidence-id',
        type=str,
        help='File ID for previously-uploaded Evidence of Supporting Document file supporting submission',
        callback=callback
    )(f)


def evidence_file_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(ProviderResponseAPITask)
        if value:
            task.args['evidence_file']  =   value
        return value
    
    return click.option(
        '--evidence-file',
        type=click.Path(exists=True, dir_okay=False),
        help='Evidence or Supporting Document file supporting submission',
        callback=callback
    )(f)


def challenge_file_column_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(ProviderResponseAPITask)
        task.args['challenge_file_column']  =   value
        return value
    
    return click.option(
        '--challenge-file-columm',
        type=str,
        default='challenge_id',
        help='Column in CSV or Excel Challenge File containing challenge IDs',
        callback=callback
    )(f)


#
# Common arguments
#


def challenge_file_argument(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(ProviderResponseAPITask)
        task.chg_file   =   value
        return value

    return click.argument(
        'challenge_file',
        required=True,
        type=click.Path(exists=True, dir_okay=False),
        callback=callback
    )(f)


#
# Arguments for Provider Fixed Challenge Initial & Final Response APIs
#


def response_argument(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(ProviderResponseAPITask)
        task.args['response']   =   value
        return value
    
    return click.argument( 
        'response',
        required=True,
        type=click.Choice([ 'Dispute', 'Concede', 'Semi-concede' ], case_sensitive=False),
        callback=callback
    )(f)


#
# Arguments for Provider Fixed Challenge Final Response API
#


def resolution_code_argument(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        if value:
            task.args['resolution_outcome_code']    =   int(value)
        elif task.args['response'] == 'Dispute':
            raise click.BadParameter('Resolution Code argument required when provider fixed challenge final response is "Dispute"')
        return value
    
    return click.argument( 
        'resolution_code',
        required=False,
        type=click.Choice([ '1', '2', '3', '4', '5', '6', '7', '8', '99' ]),
        callback=callback
    )(f)


def challenger_concurrence_argument(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        if value:
            task.args['challenger_concurrence']     =   value
        elif task.args['response'] == 'Dispute':
            raise click.BadParameter('Challenger Concurrence argument required when provider fixed challenge final response is "Dispute"')
        return value
    
    return click.argument( 
        'challenger_concurrence',
        required=False,
        type=click.Choice([ 'Yes', 'No', 'Unable to reach' ], case_sensitive=False),
        callback=callback
    )(f)


#
# Arguments for Provider Fixed Challenge Certify APIs
#


def certify_update_type_argument(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        task.json['certify_update_type']    =   value
        return value
    
    return click.argument( 
        'certify_update_type',
        required=True,
        type=click.Choice([ 'Remove', 'Update' ], case_sensitive=False),
        callback=callback
    )(f)


def certify_update_technology_option(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        if value:
            task.json['certify_update_technology']  =   int(value)
        elif task.json['certify_update_type'] == 'Update':
            raise click.BadParameter('Certify Update Technology argument required when Certify Update Type is "Update"')
        return value
    
    return click.option( 
        '--certify-update-technology',
        type=click.Choice([ '10', '40', '50', '60', '61', '70', '71', '72', '0' ]),
        help='Technology to which to update records when certifying challenges (NOTE: required when Certify Update Type is "Update")',
        callback=callback
    )(f)


def certify_update_download_option(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        if value:
            task.json['certify_update_download']    =   value
        elif task.json['certify_update_type'] == 'Update':
            raise click.BadParameter('Certify Update Download argument required when Certify Update Type is "Update"')
        return value
    
    return click.option( 
        '--certify-update-download',
        required=False,
        type=click.IntRange(min=0, max=10000),
        help='Download speed to which to update records when certifying challenges (NOTE: required when Certify Update Type is "Update")',
        callback=callback
    )(f)


def certify_update_upload_option(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        if value:
            task.json['certify_update_upload']      =   value
        elif task.json['certify_update_type'] == 'Update':
            raise click.BadParameter('Certify Update Upload argument required when Certify Update Type is "Update"')
        return value
    
    return click.option( 
        '--certify-update-upload',
        required=False,
        type=click.IntRange(min=0, max=10000),
        help='Upload speed to which to update records when certifying challenges (NOTE: required when Certify Update Type is "Update")',
        callback=callback
    )(f)


def certifying_name_argument(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        task.json['certifying_name']    =   value
        return value
    
    return click.argument( 
        'certifying_name',
        required=True,
        type=str,
        callback=callback
    )(f)


def certifying_title_argument(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        task.json['certifying_title']   =   value
        return value
    
    return click.argument( 
        'certifying_title',
        required=True,
        type=str,
        callback=callback
    )(f)


def certifying_email_argument(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        task.json['certifying_email']   =   value
        return value
    
    return click.argument( 
        'certifying_email',
        required=True,
        type=str,
        callback=callback
    )(f)



def certifying_phone_argument(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        task.json['certifying_phone']   =   value
        return value
    
    return click.argument( 
        'certifying_phone',
        required=True,
        type=str,
        callback=callback
    )(f)


def certifying_phone_ext_argument(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(ProviderResponseAPITask)
        if value:
            task.json['certifying_phone_ext']   =   value
        return value
    
    return click.argument( 
        'certifying_phone_ext',
        required=False,
        type=str,
        callback=callback
    )(f)


#
# Common decorators
#


def challenge_file_args_and_opts(f):
    for func in [ challenge_file_column_option, challenge_file_argument ]:
        f = func(f)
    return f


def evidence_options(f):
    for func in [ frn_option, evidence_file_option, evidence_id_option ]:
        f = func(f)
    return f


def final_response_args_and_opts(f):
    for func in [ challenger_concurrence_argument, resolution_code_argument ]:
        f = func(f)
    return f


def certify_response_args_and_opts(f):
    for func in [   certifying_phone_ext_argument, certifying_phone_argument, certifying_email_argument,
                    certifying_title_argument, certifying_name_argument,
                    certify_update_upload_option, certify_update_download_option,
                    certify_update_technology_option, certify_update_type_argument ]:
        f = func(f)
    return f


#
# Click groups
#


@click.group()
@pass_task
def response(task):
    pass


#
# Click commands
#


#
# Bulk Submit Initial Response
#


@response.command()
@verbose_option
@config_option
@common_api_options
@comment_option
@evidence_options
@response_argument
@challenge_file_args_and_opts
@pass_task
def submit_bulk_initial_response( task, response, challenge_file, **kwargs ):
    """
    """
    if response == 'Concede':
        task.json['response_type']              =   'Accept'
        task.json['response_type_semiconcede']  =   'false'

        task.args['response_type_code']         =   1
    elif response == 'Semi-concede':
        task.json['response_type']              =   'Accept'
        task.json['response_type_semiconcede']  =   'true'

        task.args['response_type_code']         =   1
    elif response == 'Dispute':
        assert any(task.args[option] is not None for option in [ 'evidence_file', 'evidence_file_id' ])
        task.json['response_type']              =   'Reject'
        task.json['response_type_semiconcede']  =   None

        task.args['response_type_code']         =   2
    else:
        raise ValueError('Invalid response type:%s' % response)
    
    if task.args.get('comments') is not None:
        task.json['response_comments']      =   task.args['comments']
    
    if task.args.get('evidence_file') is not None:
        if task.frn is None:
            task.frn    =   click.prompt(
                                'Enter FRN of responding provider',
                                type=str,
                                value_proc=lambda x: str(int(x)).zfill(10)
                            )

        rspjson     =   task.upload_bulk_document(task.args['evidence_file'])
        rspdict     =   next(r for r in rspjson['data'])

        task.json['response_file_id']   =   rspdict['file_id']
    elif task.args.get('evidence_file_id') is not None:
        task.json['response_file_id']   =   task.args['evidence_file_id']
    else:
        task.json['response_file_id']   =   None
    
    challenge_ids   =   task.get_challenge_ids(challenge_file, task.args['challenge_file_column'])

    chunk_size      =   task.args.get('chunk_size')
    for challenge_id_list in task.chunk_api_calls(challenge_ids, chunk_size):
        rspjson     =   task.submit_bulk_initial_response(challenge_id_list)
        task.logger.debug('API call response:%s', rspjson)


#
# Bulk Submit Final Response
#


@response.command()
@verbose_option
@config_option
@common_api_options
@comment_option
@evidence_options
@response_argument
@challenge_file_args_and_opts
@final_response_args_and_opts
@pass_task
def submit_bulk_final_response( task, response, challenge_file, **kwargs ):
    """
    """
    if response == 'Concede':
        task.json['final_response_type']                =   'Accept'
        task.json['final_response_type_semiconcede']    =   'false'

        task.args['response_type_code']                 =   3
    elif response == 'Semi-concede':
        task.json['final_response_type']                =   'Accept'
        task.json['final_response_type_semiconcede']    =   'true'

        task.args['response_type_code']                 =   3
    elif response == 'Dispute':
        assert all(task.args.get(option) is not None for option in [ 'resolution_outcome_code', 'challenger_concurrence' ])
        task.json['final_response_type']                =   'Reject'
        task.json['final_response_type_semiconcede']    =   None
        
        task.args['response_type_code']                 =   4
        
        task.json['resolution_outcome_code']            =   task.args['resolution_outcome_code']
        task.json['challenger_concurrence']             =   task.args['challenger_concurrence']
    else:
        raise ValueError('Invalid response type:%s' % response)
    
    if task.args.get('comments') is not None:
        task.json['final_response_comments']    =   task.args['comments']
    
    if task.args.get('evidence_file') is not None:
        if task.frn is None:
            task.frn    =   click.prompt(
                                'Enter FRN of responding provider',
                                type=str,
                                value_proc=lambda x: str(int(x)).zfill(10)
                            )

        rspjson     =   task.upload_bulk_document(task.args['evidence_file'])
        rspdict     =   next(r for r in rspjson['data'])

        task.json['final_response_file_id'] =   rspdict['file_id']
    elif task.args.get('evidence_file_id') is not None:
        task.json['final_response_file_id'] =   task.args['evidence_file_id']
    else:
        task.json['final_response_file_id'] =   None
    
    challenge_ids   =   task.get_challenge_ids(challenge_file, task.args['challenge_file_column'])

    chunk_size      =   task.args.get('chunk_size')

    for challenge_id_list in task.chunk_api_calls(challenge_ids, chunk_size):
        rspjson     =   task.submit_bulk_final_response(challenge_id_list)
        task.logger.debug('API call response:%s', rspjson)


#
# Bulk Revert Initial Response
#


@response.command()
@verbose_option
@config_option
@common_api_options
@challenge_file_args_and_opts
@pass_task
def revert_bulk_initial_response(task, challenge_file, **kwargs):
    """
    """
    challenge_ids   =   task.get_challenge_ids(challenge_file, task.args['challenge_file_column'])

    chunk_size      =   task.args.get('chunk_size')

    for challenge_id_list in task.chunk_api_calls(challenge_ids, chunk_size):
        rspjson     =   task.revert_bulk_initial_response(challenge_id_list)
        task.logger.debug('API call response:%s', rspjson)
    

#
# Bulk Revert Final Response
#


@response.command()
@verbose_option
@config_option
@common_api_options
@challenge_file_args_and_opts
@pass_task
def revert_bulk_final_response(task, challenge_file, **kwargs):
    """
    """
    challenge_ids   =   task.get_challenge_ids(challenge_file, task.args['challenge_file_column'])

    chunk_size      =   task.args.get('chunk_size')

    for challenge_id_list in task.chunk_api_calls(challenge_ids, chunk_size):
        rspjson     =   task.revert_bulk_final_response(challenge_id_list)
        task.logger.debug('API call response:%s', rspjson)


#
# Bulk Certify Response
#


@response.command()
@verbose_option
@config_option
@common_api_options
@comment_option
@challenge_file_args_and_opts
@certify_response_args_and_opts
@pass_task
def certify_bulk_response( task, challenge_file, **kwargs ):
    """
    """
    challenge_ids   =   task.get_challenge_ids(challenge_file, task.args['challenge_file_column'])

    chunk_size      =   task.args.get('chunk_size')
    
    for challenge_id_list in task.chunk_api_calls(challenge_ids, chunk_size):
        rspjson     =   task.certify_bulk_response(challenge_id_list)
        task.logger.debug('API call response:%s', rspjson)


#
#
#