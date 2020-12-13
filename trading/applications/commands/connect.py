import click
import logging

# pylint: disable=no-value-for-parameter

@click.command()
@click.option(
    '--int-account',
    required=True,
    type=int,
    help='Degiro\'s intAccount number.'
)
@click.option(
    '--username',
    required=True,
    type=str,
    help='Degiro\'s username.'
)
@click.option(
    '--password',
    required=True,
    type=str,
    help='Degiro\'s password.'
)
@click.option(
    '--log-level',
    default='INFO',
    type=click.Choice(logging._nameToLevel),
    help='Desired level of logging.'
)
@click.option(
    '--log-directory',
    required=False,
    type=click.Path(dir_okay=True),
    help='The choosen log dir.'
)
def cli(
    username:str,
    password:str,
    int_account:int,
    log_level:str,
    log_directory:str=None
):
    """ Retrieves a session_id from Degiro Quotecast API."""

    from trading.api import API
    from trading.pb.trading_pb2 import Credentials

    credentials = Credentials(
        int_account=int_account,
        username=username,
        password=password
    )
    api = API(credentials=credentials)

    api.connect()

    click.secho('Connection done !', bg='blue')

    click.secho(
        f'Session id : {api.connection_storage.session_id}',
        bg='blue'
    )