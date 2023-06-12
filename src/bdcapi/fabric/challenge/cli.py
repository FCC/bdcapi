import click
from bdcapi.common.cli import (
    common_api_options,
    comment_option,
    verbose_option,
    config_option,
)
from bdcapi.fabric.challenge.api import EntityChallengeAPITask


pass_task = click.make_pass_decorator(EntityChallengeAPITask, ensure=True)


#
# Main options
#


def evidence_file_option(f):
    def callback(ctx, param, value):
        task    =   ctx.ensure_object(EntityChallengeAPITask)
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
        task    =   ctx.ensure_object(EntityChallengeAPITask)
        
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
        task    =   ctx.ensure_object(EntityChallengeAPITask)
        
        task.chg_file   =   value
        
        return value

    return click.argument(
        'challenge_file',
        required=True,
        type=click.Path(exists=True, dir_okay=False),
        callback=callback
    )(f)


#
# Arguments for Bulk Fixed Challenge Certify APIs
#


def certifying_name_argument(f):
    def callback(ctx, param, value):
        task        =   ctx.ensure_object(EntityChallengeAPITask)
        
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
        task        =   ctx.ensure_object(EntityChallengeAPITask)
        
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
        task        =   ctx.ensure_object(EntityChallengeAPITask)
        
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
        task        =   ctx.ensure_object(EntityChallengeAPITask)
        
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
        task        =   ctx.ensure_object(EntityChallengeAPITask)
        
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
    for func in [ evidence_file_option ]:
        f = func(f)
    return f


def certify_response_args_and_opts(f):
    for func in [   certifying_phone_ext_argument, certifying_phone_argument, certifying_email_argument,
                    certifying_title_argument, certifying_name_argument ]:
        f = func(f)
    return f


#
# Click groups
#


@click.group()
@pass_task
def challenge(task):
    pass


#
# Click commands
#


#
# Bulk Withdraw Challenges
#


@challenge.command()
@challenge_file_args_and_opts
@common_api_options
@verbose_option
@pass_task
def withdraw( task, challenge_file, **kwargs ):
    """
    """
    if task.args.get('apitoken_file') is not None:
        task.apitoken       =   task.get_api_token(task.args['apitoken_file'])
    else:
        if len(task.apitoken) != 44:
            task.logger.error('Invalid API token -- value must be a 44-character string')
            raise ValueError
    
    challenge_ids   =   task.get_challenge_ids(challenge_file, task.args['challenge_file_column'])

    chunk_size      =   task.args.get('chunk_size')
    for challenge_id_list in task.chunk_api_calls(challenge_ids, chunk_size):
        rspjson     =   task.fab_withdraw_challenge(challenge_id_list)
        task.logger.debug('API call response:%s', rspjson)


#
#
#