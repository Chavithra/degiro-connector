import click
import logging

# pylint: disable=no-value-for-parameter

@click.command()
@click.option(
    '--log-directory',
    required=False,
    type=click.Path(dir_okay=True),
    help='The choosen log dir.'
)
@click.option(
    '--log-level',
    default='FATAL',
    type=click.Choice(logging._nameToLevel),
    help='Desired level of logging.'
)
@click.option(
    '--user-token',
    required=True,
    type=int,
    help='Degiro\'s user token number.'
)
def cli(log_level:str, user_token:int, log_directory:str=None):
    """ Retrieves a session_id from Degiro Quotecast API."""

    from datetime import date
    from quotecast.api import API
    from quotecast.pb.quotecast_pb2 import Credentials
    
    # Setup logs
    log_level = logging.getLevelName(log_level)
    if not log_directory is None:
        filename = '%s/quotecast_log_%s.txt' % (log_directory, date.today().strftime('%Y_%m_%d'))
        filename = filename.strip('"').strip("'")
        logging.basicConfig(filename=filename, level=log_level)
    else:
        logging.basicConfig(level=log_level)

    # Setup objects used by the services
    api = API(credentials=Credentials(user_token=user_token))

    api.connection_storage.connect()
    
    click.echo(f'Session id : {api.connection_storage.session_id}')