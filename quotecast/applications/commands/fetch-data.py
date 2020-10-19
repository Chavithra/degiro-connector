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
    from quotecast.pb.quotecast_pb2 import (
        Action,
        SubscriptionRequest
    )

    # SETUP API
    api = API(user_token=user_token)

    api.connection_storage.connect()
    
    click.echo(f'Session id : {api.connection_storage.session_id}')
    
    product_id = 360015751
    label_list =[
        'LastDate',
        'LastTime',
        'LastPrice',
        'LastVolume',
    ]
    subscription_request = SubscriptionRequest(
        action=Action.SUBSCRIBE,
        product_id=product_id,
        label_list=label_list
    )

    api.subscribe(subscription_request=subscription_request)

    while True:
        raw_response = api.fetch_data()
        click.echo(raw_response)