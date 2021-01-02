import click
import logging

# pylint: disable=no-value-for-parameter
# pylint: disable=no-member

@click.command()
@click.option(
    '--user-token',
    required=True,
    type=int,
    help='Degiro\'s user token number.'
)
def cli(user_token):
    """ Retrieves a session_id from Degiro Quotecast API."""

    # IMPORTATIONS
    import time
    from datetime import date
    from quotecast.api import API
    from quotecast.pb.quotecast_pb2 import Quotecast

    # SETUP API
    api = API(user_token=user_token)

    api.connect()
    
    click.echo(f'Session id : {api.connection_storage.session_id}')
    
    vwd_id = 360015751
    label_list =[
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ]
    request = Quotecast.Request()
    request.subscriptions[vwd_id].extend(label_list)

    api.subscribe(request=request)

    while True:
        raw_response = api.fetch_data()
        click.echo(raw_response)